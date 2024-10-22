import pytest

from unittest.mock import MagicMock

from web_app.db.crud import DBConnector, UserDBConnector, PositionDBConnector


@pytest.fixture(scope="function")
def mock_db_connector(mocker):
    mock_db_connector = mocker.patch("web_app.db.crud.DBConnector", autospec=True)

    mock_db_connector.write_to_db = MagicMock(return_value=None)
    mock_db_connector.get_object = MagicMock(return_value=None)
    mock_db_connector.get_object_by_field = MagicMock(return_value=None)
    mock_db_connector.delete_object = MagicMock(return_value=None)

    yield mock_db_connector


@pytest.fixture(scope="function")
def mock_user_db_connector(mocker):
    mock_user_db_connector = mocker.patch(
        "web_app.db.crud.UserDBConnector", autospec=True
    )

    mock_user_db_connector.get_user_by_wallet_id = MagicMock(return_value=None)
    mock_user_db_connector.get_contract_address_by_wallet_id = MagicMock(
        return_value=None
    )
    mock_user_db_connector.create_user = MagicMock(return_value=None)
    mock_user_db_connector.update_user_contract = MagicMock(return_value=None)

    yield mock_user_db_connector


@pytest.fixture(scope="function")
def mock_position_db_connector(mocker):
    mock_position_db_connector = mocker.patch(
        "web_app.db.crud.PositionDBConnector", autospec=True
    )

    mock_position_db_connector.get_positions_by_wallet_id = MagicMock(return_value=[])
    mock_position_db_connector.create_position = MagicMock(return_value=None)
    mock_position_db_connector.get_position_id_by_wallet_id = MagicMock(
        return_value=None
    )
    mock_position_db_connector.update_position = MagicMock(return_value=None)
    mock_position_db_connector.delete_position = MagicMock(return_value=None)
    mock_position_db_connector.close_position = MagicMock(return_value=None)
    mock_position_db_connector.open_position = MagicMock(return_value=None)

    yield mock_position_db_connector
