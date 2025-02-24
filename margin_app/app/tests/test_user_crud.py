"""
This is the test module for the UserCRUD class.
"""

import uuid
import pytest
from decimal import Decimal
from sqlalchemy.exc import IntegrityError
from app.crud.user import UserCRUD


@pytest.fixture
def user_crud() -> UserCRUD:
    """Create instance of UserCRUD"""
    return UserCRUD()


async def test_test_connection(user_crud: UserCRUD) -> None:
    """
    Positive test for test_connection method.
    """
    result = await user_crud.test_connection()
    assert "PostgreSQL version:" in result
#----------------------------------------------------------------------------------

async def test_create_user_happy_path(user_crud: UserCRUD) -> None:
    """
    Happy Path for create_user method
    """
    user = await user_crud.create_user(wallet_id = "wallet_123")
    assert user.wallet_id == "wallet_123"
    assert user.id is not None # Ensure the user has a valid id


async def test_create_user_empty_wallet_id(user_crud: UserCRUD) -> None:
    """
    Negative test for create_user method: empty wallet_id.
    """
    with pytest.raises(ValueError, match="wallet_id cannot be empty"):
        await user_crud.create_user(wallet_id = None) 

async def test_create_user_duplicate_wallet_id(user_crud: UserCRUD) -> None:
    """
    Negative test for create_user method: duplicate wallet_id
    """
    await user_crud.create_user(wallet_id = "wallet_123")
    with pytest.raises(IntegrityError, match="duplicate key value violates unique constraint"):
        await user_crud.create_user(wallet_id = "wallet_123")
#----------------------------------------------------------------------------------

async def test_update_user_happy_path(user_crud: UserCRUD) -> None:
    """
    Happy path for update_user method
    """
    user = await user_crud.create_user(wallet_id = "wallet_123")
    updated_user = await user_crud.update_user(user.id, wallet_id = "wallet_456")
    assert updated_user.wallet_id == "wallet_456"


async def test_update_user_non_existent(user_crud: UserCRUD) -> None:
    """
    Negative test for update_user method: non-existent user
    """
    non_existent_id = uuid.uuid4()
    result = await user_crud.update_user(non_existent_id, wallet_id = "wallet_456")
    assert result is None

async def test_delete_user_happy_path(user_crud: UserCRUD) -> None:
    """
    Positive test for delete_user method.
    """
    user = await user_crud.create_user(wallet_id = "wallet_123")
    await user_crud.delete_user(user.id)
    deleted_user = user_crud.get_user(user.id)
    assert deleted_user is None



def test_delete_user_non_existent(user_crud: UserCRUD) -> None:
    """
    Negative test for delete_user method: non-existent user
    """
    non_existent_id = uuid.uuid4()
    with pytest.raises(ValueError, match="User does not exist"):
        user_crud.delete_user(non_existent_id)
#----------------------------------------------------------------------------------

def test_add_deposit_happy_path(user_crud: UserCRUD) -> None:
    """
    Positive test for add_deposit method
    """
    user = user_crud.create_user(wallet_id = "wallet_123")
    deposit = user_crud.add_deposit(user.id, amount=Decimal("100.00"))
    assert deposit.user_id == user.id
    assert deposit.amount == Decimal("100.00")



def test_add_deposit_non_existent_user(user_crud: UserCRUD) -> None:
    """
    Negative test for add_deposit method: Non-existent user
    """
    non_existent_id = uuid.uuid4()
    with pytest.raises(ValueError, match="User {non_existent_id} does not exist"):
        user_crud.add_deposit(non_existent_id, amount=Decimal("100.00"))

def test_add_deposit_invalid_amount(user_crud: UserCRUD) -> None:
    """
    Negative test for add_deposit method: Invalid amount
    """
    user = user_crud.create_user(wallet_id = "wallet_123")
    with pytest.raises(ValueError, match="Amount must be greater than zero"):
        user_crud.add_deposit(user.id, amount=Decimal("0.00"))
#----------------------------------------------------------------------------------
def test_add_margin_position_happy_path(user_crud: UserCRUD) -> None:
    """
    Positive test for add_margin position method.
    """
    user = user_crud.create_user(wallet_id = "wallet_123")
    margin_position = user_crud.add_margin_position(
        user.id, size=Decimal("100.00"), leverage=5)
    assert margin_position.user_id == user.id
    assert margin_position.size == Decimal("100.00")
    assert margin_position.leverage == 5

def test_add_margin_position_non_existent_user(user_crud: UserCRUD) -> None:
    """
    Negative test for add_margin_position method: Non-existent User
    """
    non_existent_id = uuid.uuid4()
    with pytest.raises(ValueError, match="User {non_existent_id} does not exist"):
        user_crud.add_margin_position(
            non_existent_id, size=Decimal("100.00"), leverage=5)

def test_add_margin_position_invalid_size(user_crud: UserCRUD) -> None:
    """
    Negative test for add_margin_position method: Invalid size
    """
    user = user_crud.create_user(wallet_id = "wallet_123")
    with pytest.raises(ValueError, match="Leverage must be greater than zero"):
        user_crud.add_margin_position(user.id, size=Decimal("0.00"), leverage=5)

def test_add_margin_position_invalid_leverage(user_crud: UserCRUD) -> None:
    """
    Negative test for add_margin_position method: Invalid leverage
    """
    user = user_crud.create_user(wallet_id = "wallet_123")
    with pytest.raises(ValueError, match="Leverage must be greater than zero"):
        user_crud.add_margin_position(user.id, size=Decimal("10.00"), leverage=0)
