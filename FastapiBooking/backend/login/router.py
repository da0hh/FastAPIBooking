from fastapi import APIRouter, Depends, HTTPException

from login.schemas import LoginRead, LoginInAcc, SignUp, ChangePassword, ChangeUsername, DeleteAccount
from login.models import Login

from database import get_db
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

@router.post("/sign-up", response_model=LoginRead)
async def sign_up(payload: SignUp, db: AsyncSession = Depends(get_db)):
    condition = await db.scalar(select(Login).where(Login.username == payload.username))

    if condition:
        raise HTTPException(status_code=409, detail="User with this username is already exist")

    hashed_password = pwd_context.hash(payload.password)
    new_account = Login(
        username=payload.username,
        hashed_password=hashed_password,
        date_registration=datetime.now()
    )

    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)

    return new_account

async def _get_account_or_404(username: str, db: AsyncSession) -> Login:
    account = await db.scalar(select(Login).where(Login.username == username))
    if account is None:
        raise HTTPException(status_code=404, detail="User not found")
    return account

@router.post("/check-account/{username}", response_model=LoginRead)
async def check_account_name(username: str, db: AsyncSession = Depends(get_db)):
    return await _get_account_or_404(username, db)

def verify_password(plain: str, acc: Login):
    if not pwd_context.verify(plain, acc.hashed_password):
        raise HTTPException(status_code=403, detail="Invalid password")

@router.post("/enter-in-acc", response_model=LoginRead)
async def login_in_acc(payload: LoginInAcc, db: AsyncSession = Depends(get_db)):
    account = await check_account_name(payload.username, db)
    verify_password(payload.password, account)

    return account

@router.post("/change-name/{username}", response_model=LoginRead)
async def edit_account_name(new_username: ChangeUsername, account: LoginInAcc, db: AsyncSession = Depends(get_db)):
    valid_account = await check_account_name(account.username, db)
    verify_password(account.password, valid_account)

    check_valid_new_name = await db.scalar(select(Login).where(Login.username == new_username.new_username))
    if check_valid_new_name:
        raise HTTPException(status_code=403, detail="User with this username is already exist")

    valid_account.username = new_username.new_username

    await db.commit()
    await db.refresh(valid_account)

    return valid_account

@router.post("/change-pass/{username}", response_model=LoginRead)
async def edit_account_password(new_pass: ChangePassword, account: LoginInAcc, db: AsyncSession = Depends(get_db)):
    valid_acc = await check_account_name(account.username, db)
    verify_password(account.password, valid_acc)

    valid_acc.hashed_password = pwd_context.hash(new_pass.new_password)

    await db.commit()
    await db.refresh(valid_acc)

    return valid_acc

@router.delete("/delete-acc/{user_id}")
async def delete_account(payload: DeleteAccount, db: AsyncSession = Depends(get_db)):
    acc = await db.get(Login, payload.user_id)

    if acc is None:
        raise HTTPException(detail="User does not exist", status_code=403)

    if not pwd_context.verify(str(payload.password), acc.hashed_password):
        raise HTTPException(detail="Invalid password", status_code=403)

    await db.delete(acc)
    await db.commit()

    return {"ok": True}