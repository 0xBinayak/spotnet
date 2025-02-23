import pytest
import pytest_asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import DBConnector
from app.models.base import BaseModel
from sqlalchemy import Column, String

pytestmark = pytest.mark.asyncio

# Sample model for testing
class TestModel(BaseModel):
    __tablename__ = "test_model"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)

@pytest_asyncio.fixture
async def db_connector():
    db = DBConnector()
    async with db.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)  # ✅ FIXED

    try:
        yield db
    finally:
        async with db.engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)  # ✅ FIXED


@pytest_asyncio.fixture
async def test_object(db_connector):
    obj = TestModel(name="Test Object")
    obj = await db_connector.write_to_db(obj)
    return obj

async def test_write_to_db(db_connector):
    obj = TestModel(name="New Object")
    saved_obj = await db_connector.write_to_db(obj)
    assert saved_obj.id is not None
    assert saved_obj.name == "New Object"

async def test_get_object(db_connector, test_object):
    fetched_obj = await db_connector.get_object(TestModel, test_object.id)
    assert fetched_obj is not None
    assert fetched_obj.id == test_object.id
    assert fetched_obj.name == "Test Object"

async def test_get_object_by_field(db_connector, test_object):
    fetched_obj = await db_connector.get_object_by_field(TestModel, "name", "Test Object")
    assert fetched_obj is not None
    assert fetched_obj.name == "Test Object"

async def test_delete_object_by_id(db_connector, test_object):
    await db_connector.delete_object_by_id(TestModel, test_object.id)
    fetched_obj = await db_connector.get_object(TestModel, test_object.id)
    assert fetched_obj is None

async def test_delete_object(db_connector):
    obj = TestModel(name="To be deleted")
    obj = await db_connector.write_to_db(obj)
    await db_connector.delete_object(obj)
    fetched_obj = await db_connector.get_object(TestModel, obj.id)
    assert fetched_obj is None

# Negative test cases
async def test_get_nonexistent_object(db_connector):
    non_existing_id = str(uuid.uuid4())
    obj = await db_connector.get_object(TestModel, non_existing_id)
    assert obj is None

async def test_get_object_by_invalid_field(db_connector):
    with pytest.raises(AttributeError):
        await db_connector.get_object_by_field(TestModel, "non_existing_field", "value")

async def test_delete_nonexistent_object(db_connector):
    non_existing_id = str(uuid.uuid4())
    await db_connector.delete_object_by_id(TestModel, non_existing_id)  # Should not raise an error

async def test_write_invalid_object(db_connector):
    with pytest.raises(Exception):
        await db_connector.write_to_db(None)
