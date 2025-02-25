import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Forzar variables de entorno si deseas
os.environ["DATABASE_URL"] = "mysql+pymysql://root:1234@localhost:3306/ads_db"
os.environ["DATABASE_POOL_SIZE"] = "5"

from src.main.python.config.DatabasesConfig import get_db
from src.main.python.models import Base  # Unificado en models/__init__.py
from src.main.python.models.Ad import Ad
from src.main.python.Application import app

# Crea un motor de pruebas
engine = create_engine(os.environ["DATABASE_URL"])
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea tablas en la base de datos de test (solo si no existen)
Base.metadata.create_all(bind=engine)

def override_get_db():
    """
    Sobrescribe la dependencia de DB para usar TestingSessionLocal.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Reemplaza la función get_db original con la de pruebas
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def clear_ads():
    """
    Limpia la tabla 'ad' antes y después de cada test.
    """
    db = TestingSessionLocal()
    db.query(Ad).delete()
    db.commit()
    db.close()
    yield
    db = TestingSessionLocal()
    db.query(Ad).delete()
    db.commit()
    db.close()

def test_create_ad():
    """
    Test para crear un Ad (POST /ads/)
    """
    payload = {
        "advertiser_id": "advert_123",
        "content": "This is a new ad content",
        "start_date": "2025-03-01T09:00:00",
        "end_date": "2025-03-10T18:00:00"
    }
    response = client.post("/ads/", json=payload)
    assert response.status_code == 200  # Respuesta exitosa
    data = response.json()
    assert data["advertiser_id"] == "advert_123"
    assert data["content"] == "This is a new ad content"
    assert "ad_id" in data

def test_get_ad_by_id():
    """
    Test para obtener un Ad por su ID (GET /ads/{ad_id})
    """
    # Inserta un Ad en la BD
    db = TestingSessionLocal()
    new_ad = Ad(
        advertiser_id="test_user",
        content="Some interesting ad",
        start_date=datetime(2025, 3, 1, 9, 0, 0),
        end_date=datetime(2025, 3, 10, 18, 0, 0)
    )
    db.add(new_ad)
    db.commit()
    db.refresh(new_ad)
    db.close()

    # Llamamos al endpoint GET /ads/{ad_id}
    response = client.get(f"/ads/{new_ad.ad_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["advertiser_id"] == "test_user"
    assert data["content"] == "Some interesting ad"
    assert data["ad_id"] == new_ad.ad_id

def test_list_ads():
    """
    Test para listar todos los Ads (GET /ads/)
    """
    db = TestingSessionLocal()
    ad1 = Ad(
        advertiser_id="userA",
        content="Ad content A",
        start_date=datetime(2025, 3, 1, 9, 0, 0)
    )
    ad2 = Ad(
        advertiser_id="userB",
        content="Ad content B",
        start_date=datetime(2025, 3, 2, 10, 0, 0)
    )
    db.add(ad1)
    db.add(ad2)
    db.commit()
    db.refresh(ad1)
    db.refresh(ad2)
    db.close()

    response = client.get("/ads/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    ad_ids = {item["ad_id"] for item in data}
    assert ad1.ad_id in ad_ids
    assert ad2.ad_id in ad_ids

def test_update_ad():
    """
    Test para actualizar un Ad (PUT /ads/{ad_id})
    """
    db = TestingSessionLocal()
    old_ad = Ad(
        advertiser_id="old_user",
        content="Old content",
    )
    db.add(old_ad)
    db.commit()
    db.refresh(old_ad)
    db.close()

    # Actualizamos
    payload = {
        "advertiser_id": "updated_user",
        "content": "Updated content"
    }
    response = client.put(f"/ads/{old_ad.ad_id}", json=payload)
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["advertiser_id"] == "updated_user"
    assert updated_data["content"] == "Updated content"

def test_delete_ad():
    """
    Test para eliminar un Ad (DELETE /ads/{ad_id})
    """
    db = TestingSessionLocal()
    temp_ad = Ad(
        advertiser_id="delete_user",
        content="Temp content"
    )
    db.add(temp_ad)
    db.commit()
    db.refresh(temp_ad)
    db.close()

    # Verificamos que existe
    response_get = client.get(f"/ads/{temp_ad.ad_id}")
    assert response_get.status_code == 200

    # DELETE
    response_del = client.delete(f"/ads/{temp_ad.ad_id}")
    assert response_del.status_code == 204

    # Verificar que ya no existe
    response_get_again = client.get(f"/ads/{temp_ad.ad_id}")
    assert response_get_again.status_code == 404
