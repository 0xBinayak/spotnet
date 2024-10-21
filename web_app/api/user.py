from fastapi import APIRouter, Request
from web_app.db.crud import UserDBConnector
from web_app.api.serializers.transaction import UpdateUserContractRequest
from web_app.api.serializers.user import CheckUserResponse, UpdateUserContractResponse, GetUserContractAddressResponse 

router = APIRouter()  # Initialize the router

user_db = UserDBConnector()


@router.get("/api/get-user-contract", tags=["User Operations"], summary="Get user's contract status", response_description="Returns 0 if the user is None or if the contract is not deployed. Returns the transaction hash if the contract is deployed.")
async def get_user_contract(wallet_id: str) -> str:
    """
    This endpoint retrieves the contract status of a user.
    
    ### Parameters:
    - **wallet_id**: User's wallet ID
    
    ### Returns:
    User's contract status, 0 if not found, else returns the transaction hash
    """
    
    user = user_db.get_user_by_wallet_id(wallet_id)
    if user is None or not user.is_contract_deployed:
        return ""
    else:
        return user.contract_address


@router.get("/api/check-user", tags=["User Operations"], summary="Check if user exists and contract status", response_model=CheckUserResponse, response_description="Returns whether the user's contract is deployed.")
async def check_user(request: Request, wallet_id: str) -> CheckUserResponse:
    """
    This endpoint checks if the user exists, or adds the user to the database if they don't exist, 
    and checks whether their contract is deployed. 
    
    ### Parameters:
    - **wallet_id**: The wallet ID of the user.
    
    ### Returns:
    The contract deployment status
    """
    
    user = user_db.get_user_by_wallet_id(wallet_id)
    if user and not user.is_contract_deployed:
        return {"is_contract_deployed": False}
    elif not user:
        user_db.create_user(wallet_id)
        return {"is_contract_deployed": False}
    else:
        return {"is_contract_deployed": True}


@router.post("/api/update-user-contract", tags=["User Operations"], summary="Update the user's contract", response_model=UpdateUserContractResponse, response_description="Returns if the contract is updated and deployed.")
async def update_user_contract(data: UpdateUserContractRequest) ->  UpdateUserContractResponse:
    """
    This endpoint updates the user's contract.
    
    ### Parameters:
    - **wallet_id**: The wallet ID of the user.
    - **contract_address**: The contract address being deployed.
    
    ### Returns:
    The contract deployment status
    """

    user = user_db.get_user_by_wallet_id(data.wallet_id)
    if user:
        user_db.update_user_contract(user, data.contract_address)
        return {"is_contract_deployed": True}
    else:
        return {"is_contract_deployed": False}


@router.get("/api/get-user-contract-address", tags=["User Operations"], summary="Get user's contract address", response_model=GetUserContractAddressResponse, response_description="Returns the contract address of the user or None if not deployed.")
async def get_user_contract_address(wallet_id: str) -> GetUserContractAddressResponse:
    """
    This endpoint retrieves the contract address of a user.
    
    ### Parameters:
    - **wallet_id**: User's wallet ID
    
    ### Returns:
    The contract address or None if it does not exists.
    """

    contract_address = user_db.get_contract_address_by_wallet_id(wallet_id)
    if contract_address:
        return {"contract_address": contract_address}
    else:
        return {"contract_address": None}
