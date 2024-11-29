"""
Test cases for delete object
"""

import pytest
from unittest.mock import MagicMock, patch
from web_app.db.models import User
from web_app.db.crud import UserDBConnector, DBConnector


@pytest.fixture
def mock_db_connector():
    """
    Fixture to create a mock database connector.
    """
    return MagicMock()


@pytest.fixture
def user_db(mock_db_connector):
    """
    Fixture to create a UserDBConnector instance with mocked dependencies.
    """
    with patch('web_app.db.crud.UserDBConnector.get_object_by_field', 
               new_callable=MagicMock) as mock_get:
        mock_get.side_effect = mock_db_connector.get_object_by_field
        connector = UserDBConnector(mock_db_connector)
        yield connector


def test_get_user_by_wallet_id_success(user_db, mock_db_connector):
    """
    Test successful retrieval of user by wallet ID.
    """
    wallet_id = "0x123456789"
    expected_user = User(
        id=1,
        wallet_id=wallet_id,
    )

    mock_db_connector.get_object_by_field.return_value = expected_user

    result = user_db.get_user_by_wallet_id(wallet_id)

    assert result == expected_user
    mock_db_connector.get_object_by_field.assert_called_once_with(
        User,
        "wallet_id",
        wallet_id
    )


def test_get_user_by_wallet_id_not_found(user_db, mock_db_connector):
    """
    Test when user is not found by wallet ID.
    """
    wallet_id = "0x987654321"
    mock_db_connector.get_object_by_field.return_value = None

    result = user_db.get_user_by_wallet_id(wallet_id)

    assert result is None
    mock_db_connector.get_object_by_field.assert_called_once_with(
        User,
        "wallet_id",
        wallet_id
    )


def test_get_user_by_wallet_id_empty_wallet_id(user_db, mock_db_connector):
    """
    Test behavior when empty wallet ID is provided.
    """
    wallet_id = ""
    mock_db_connector.get_object_by_field.return_value = None

    result = user_db.get_user_by_wallet_id(wallet_id)

    assert result is None
    mock_db_connector.get_object_by_field.assert_called_once_with(
        User,
        "wallet_id",
        wallet_id
    )


def test_delete_user_success(user_db, mock_db_connector):
    """
    Test the successful deletion of a user.
    """
    wallet_id = "0x123456789"
    user_to_delete = User(id=1, wallet_id=wallet_id)

    mock_db_connector.get_object_by_field.return_value = user_to_delete

    mock_db_connector.delete_object.return_value = None

    user_db.delete_user_by_wallet_id(wallet_id)

    mock_db_connector.delete_object.assert_called_once_with(user_to_delete)


def test_delete_user_not_found(user_db, mock_db_connector):
    """
    Test behavior when user is not found for deletion.
    """
    wallet_id = "0x987654321"
    mock_db_connector.get_object_by_field.return_value = None

    user_db.delete_user_by_wallet_id(wallet_id)

    mock_db_connector.delete_object.assert_not_called()


def test_delete_user_error_handling(user_db, mock_db_connector):
    """
    Test the error handling when an error occurs while deleting the user.
    """
    wallet_id = "0x123456789"
    user_to_delete = User(id=1, wallet_id=wallet_id)

    mock_db_connector.get_object_by_field.return_value = user_to_delete

    mock_db_connector.delete_object.side_effect = Exception("Database error")

    with pytest.raises(Exception):
        user_db.delete_user_by_wallet_id(wallet_id)

    # Ensure delete_object was called
    mock_db_connector.delete_object.assert_called_once_with(user_to_delete)


def test_get_unique_users_count(mock_user_db_connector):
    """Test getting count of unique users."""
    mock_user_db_connector.get_unique_users_count.return_value = 5

    result = mock_user_db_connector.get_unique_users_count()

    assert result == 5
