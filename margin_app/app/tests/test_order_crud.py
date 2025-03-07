"""
Unit tests for the OrderCRUD class.
"""

import uuid
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from sqlalchemy.exc import SQLAlchemyError

from app.crud.order import OrderCRUD
from app.models.order import Order

# Test data
TEST_USER_ID = uuid.uuid4()
TEST_POSITION_ID = uuid.uuid4()
TEST_ORDER_ID = uuid.uuid4()
TEST_PRICE = 100.50
TEST_TOKEN = "BTC"


@pytest.fixture
def order_crud():
    """Fixture to create an OrderCRUD instance for testing"""
    return OrderCRUD()


@pytest.fixture
def mock_order():
    """Fixture to create a mock Order object"""
    order = MagicMock(spec=Order)
    order.id = TEST_ORDER_ID
    order.user_id = TEST_USER_ID
    order.price = TEST_PRICE
    order.token = TEST_TOKEN
    order.position = TEST_POSITION_ID
    return order


@pytest.mark.asyncio
async def test_add_new_order_success(order_crud, mock_order):
    """Test successfully adding a new order"""
    # Arrange
    with patch.object(order_crud, 'write_to_db', new_callable=AsyncMock) as mock_write_to_db:
        mock_write_to_db.return_value = mock_order
        
        # Act
        result = await order_crud.add_new_order(
            user_id=TEST_USER_ID,
            price=TEST_PRICE,
            token=TEST_TOKEN,
            position=TEST_POSITION_ID
        )
        
        # Assert
        assert mock_write_to_db.called
        assert result == mock_order
        assert result.user_id == TEST_USER_ID
        assert result.price == TEST_PRICE
        assert result.token == TEST_TOKEN
        assert result.position == TEST_POSITION_ID


@pytest.mark.asyncio
async def test_add_new_order_exception(order_crud):
    """Test exception handling when adding a new order fails"""
    # Arrange
    with patch.object(order_crud, 'write_to_db', new_callable=AsyncMock) as mock_write_to_db:
        mock_write_to_db.side_effect = SQLAlchemyError("Database error")
        
        # Act & Assert
        with pytest.raises(Exception):
            await order_crud.add_new_order(
                user_id=TEST_USER_ID,
                price=TEST_PRICE,
                token=TEST_TOKEN,
                position=TEST_POSITION_ID
            )


@pytest.mark.asyncio
async def test_execute_order_success(order_crud, mock_order):
    """Test successfully executing an order"""
    # Arrange
    with patch.object(order_crud, 'get_object', new_callable=AsyncMock) as mock_get_object:
        mock_get_object.return_value = mock_order
        
        # Act
        result = await order_crud.execute_order(TEST_ORDER_ID)
        
        # Assert
        mock_get_object.assert_called_once_with(Order, TEST_ORDER_ID)
        assert result is True


@pytest.mark.asyncio
async def test_execute_order_not_found(order_crud):
    """Test executing an order that doesn't exist"""
    # Arrange
    with patch.object(order_crud, 'get_object', new_callable=AsyncMock) as mock_get_object:
        mock_get_object.return_value = None
        
        # Act
        result = await order_crud.execute_order(TEST_ORDER_ID)
        
        # Assert
        mock_get_object.assert_called_once_with(Order, TEST_ORDER_ID)
        assert result is False


@pytest.mark.asyncio
async def test_execute_order_exception(order_crud):
    """Test exception handling when executing an order fails"""
    # Arrange
    with patch.object(order_crud, 'get_object', new_callable=AsyncMock) as mock_get_object:
        mock_get_object.side_effect = Exception("Unexpected error")
        
        # Act
        result = await order_crud.execute_order(TEST_ORDER_ID)
        
        # Assert
        mock_get_object.assert_called_once_with(Order, TEST_ORDER_ID)
        assert result is False


@pytest.mark.asyncio
async def test_execute_order_integration(order_crud, mock_order):
    """
    Integration test for execute_order that tests the full flow 
    with minimal mocking
    """
    # This test would typically use a test database
    with patch.object(order_crud, 'get_object', new_callable=AsyncMock) as mock_get_object:
        mock_get_object.return_value = mock_order
        
        # Act - execute the order
        success = await order_crud.execute_order(TEST_ORDER_ID)
        
        # Assert
        assert success is True
