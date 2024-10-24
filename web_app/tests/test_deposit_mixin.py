import pytest

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

from web_app.contract_tools.mixins.deposit import DepositMixin


class TestDepositMixin:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "deposit_token, amount, multiplier, wallet_id, borrowing_token",
        [
            (
                "STRK",
                "100_000",
                2,
                "0x27994c503bd8c32525fbdaf9d398bdd4e86757988c64581b055a06c5955ea49",
                "STRK",
            ),
            (
                "USDC",
                "3333.3",
                4,
                "0x27994c503bd8c32525fbdaf9d398bdd4e86757988c64581b055a06c5955ea49",
                "ETH",
            ),
            (
                "",
                "0",
                0,
                "invalid_wallet_id",
                "",
            ),
        ],
    )
    @patch(
        target="web_app.contract_tools.mixins.deposit.CLIENT.get_loop_liquidity_data",
        new_callable=AsyncMock,
    )
    @patch("web_app.contract_tools.mixins.deposit.TokenParams.get_token_address")
    async def test_get_transaction_data(
        self,
        mock_get_token_address: MagicMock,
        mock_get_loop_liquidity_data: AsyncMock,
        deposit_token: str,
        amount: str,
        multiplier: int,
        wallet_id: str,
        borrowing_token: str,
    ) -> None:
        expected_transaction_data = {
            "caller": wallet_id,
            "pool_price": "mocked_pool_price",
            "pool_key": "mocked_pool_key",
            "deposit_data": "mockeddeposit_data",
        }

        mock_get_token_address.side_effect = lambda token: f"mocked_address_for_{token}"
        mock_get_loop_liquidity_data.return_value = expected_transaction_data

        transaction_data = await DepositMixin.get_transaction_data(
            deposit_token, amount, multiplier, wallet_id, borrowing_token
        )

        mock_get_token_address.assert_any_call(deposit_token)

        mock_get_loop_liquidity_data.assert_called_once_with(
            f"mocked_address_for_{deposit_token}",
            int(Decimal(amount) * Decimal(10**18)),
            multiplier,
            wallet_id,
            borrowing_token,
        )

        assert transaction_data == expected_transaction_data

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "supply_token",
        ["STRK", "ETH", "USDC", None, 3.14, {}],
    )
    @patch(
        target="web_app.contract_tools.mixins.deposit.CLIENT.get_repay_data",
        new_callable=AsyncMock,
    )
    @patch("web_app.contract_tools.mixins.deposit.TokenParams.get_token_address")
    async def test_get_repay_data(
        self,
        mock_get_token_address: MagicMock,
        mock_get_repay_data: AsyncMock,
        supply_token: str,
    ) -> None:
        mock_get_token_address.side_effect = lambda token: f"mocked_address_for_{token}"

        expected_repay_data = {
            "supply_token": mock_get_token_address(supply_token),
            "debt_token": mock_get_token_address("USDC"),
            "supply_price": "mocked_supply_price",
            "debt_price": "mocked_debt_price",
            "pool_key": "mocked_pool_key",
        }

        mock_get_repay_data.return_value = {
            "supply_price": expected_repay_data["supply_price"],
            "debt_price": expected_repay_data["debt_price"],
            "pool_key": expected_repay_data["pool_key"],
        }

        repay_data = await DepositMixin.get_repay_data(supply_token)

        mock_get_token_address.assert_any_call(supply_token)
        mock_get_token_address.assert_any_call("USDC")

        assert repay_data == expected_repay_data
