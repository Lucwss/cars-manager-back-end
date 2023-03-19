from fastapi import APIRouter, Path
from src.enums.account_type import AccountType

account_router = APIRouter()


@account_router.get('/account/{acc_type}/{months}')
async def account(acc_type: AccountType, months: int = Path(..., ge=3, le=12)):
    return {
        "message": "Account created",
        "account_type": acc_type,
        "months": months
    }