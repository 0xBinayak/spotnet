SPOTNET_DEPLOYED_CONTRACT = (
    "0x05685d6b0b493c7c939d65c175305b893870cacad780842c79a611ad9122815f"
)

"""
Script to verify if a position was liquidated in zkLend.

This script checks the event logs of the zkLend contract to determine
if a specific position was liquidated.
"""

import asyncio
import logging

from starknet_py.net.full_node_client import FullNodeClient

# Load environment variables
node_url = "https://starknet-mainnet.public.blastapi.io/rpc/v0_7"
ZKLEND_CONTRACT_ADDRESS = (
    "0x05685d6b0b493c7c939d65c175305b893870cacad780842c79a611ad9122815f"
)

# Initialize the StarkNet client
client = FullNodeClient(node_url=node_url)

LIQUIDATION_KEY_OUTPUT = [
    1004689575290523089480265033644810625213175352109340690572687136992269442551
]

LIQUIDATION_SELECTOR = (
    "0x238a25785a13ab3138feb8f8f517e5a21a377cc1ad47809e9fd5e76daf01df7"
)

FROM_BLOCK = 101302
CHUNK_SIZE = 150

logging.basicConfig(
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def check_liquidation_proof(user_address):
    """
    Check if a specific user's position was liquidated in the zkLend protocol.

    This function fetches liquidation events from the zkLend market contract and checks
    if the specified user address has been liquidated. It logs the details of
    the liquidation event if found.

    Args:
        user_address (str): The address of the user whose liquidation status is to be checked.

    Returns:
        None: This function does not return a value; it logs the results directly.
    """

    # Fetch liquidation events
    events_chunk = await client.get_events(
        from_block_number=FROM_BLOCK,
        to_block_number="latest",
        follow_continuation_token=True,
        chunk_size=CHUNK_SIZE,
        keys=[[LIQUIDATION_SELECTOR]],
    )

    # Access the events attribute of the EventsChunk object,
    events = events_chunk.events

    liquid_results = []

    # Analyze events for the specific user
    for event in events:
        logger.info(f"Event Data: {event}")
        logger.info(f"Event Data: {event.data}")

        # Unpack event.data object
        # sample at https://starkscan.co/event/0x0204f9e81102c2e2f1af181e9a931580da5fa9a80abd21e15116a6175e00b736_10
        # Liquidation(liquidator,user,debt_token,debt_raw_amount,debt_face_amount,collateral_token,collateral_amount)

        liquidator = event.data[0]
        user = event.data[1]
        debt_token = event.data[2]
        debt_raw_amount = event.data[3]
        debt_face_amount = event.data[4]
        collateral_token = event.data[5]
        collateral_amount = event.data[6]

        if user in (
            "0x065d2b906c64630c29ede47405bb80cf100c7b0599753fde097055d9f6dabe7c",
            2878494537264244414183093173870516889243601958323233894338514877938199608956,
            int(user_address, base=16),
        ):

            liquid_results.append(
                (
                    user,
                    debt_face_amount,
                    collateral_amount,
                )
            )

            # Log the details of the liquidation
            logger.info(
                f"Liquidation Event: {liquidator} liquidated {user_address}'s position."
            )
            logger.info(f"Debt Token: {debt_token}, Amount: {debt_raw_amount}")
            logger.info(
                f"Collateral Token: {collateral_token}, Amount: {collateral_amount}"
            )

    # Log all liquidation results after processing all events
    if liquid_results:
        print("Liquidation Results:", liquid_results)
    else:
        print(f"No liquidation events found for user {user_address}.")


if __name__ == "__main__":
    asyncio.run(check_liquidation_proof(SPOTNET_DEPLOYED_CONTRACT))
