import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.engine.postgresdb import get_db_session
from app.schema.index import UserCreate, User as UserSchema, UserResponse, UserUpdate
from app.model.user import User as UserModel


user_router = r = APIRouter(prefix="/api/v1/users", tags=["users"])
logger = logging.getLogger(__name__)


@r.post(
    "/",
    response_model=UserResponse,
    responses={
        200: {"description": "New user created"},
        400: {"description": "Bad request"},
        409: {"description": "Conflict"},
        500: {"description": "Internal server error"},
    },
)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db_session)):
    try:
        db_user = await UserModel.get(db, email=user.email)
        if db_user and not db_user.is_deleted:
            raise HTTPException(status_code=409, detail="User already exists")

        await UserModel.create(db, **user.model_dump())
        user = await UserModel.get(db, email=user.email)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@r.get(
    "/{email}",
    response_model=UserResponse,
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_user(email: str, db: AsyncSession = Depends(get_db_session)):
    user = await UserModel.get(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@r.put(
    "/{email}",
    response_model=UserResponse,
    responses={
        200: {"description": "User updated"},
        404: {"description": "User not found"},
        500: {"description": "Internal server error"},
    },
)
async def update_user(email: str, user_payload: UserUpdate, db: AsyncSession = Depends(get_db_session)):
    try:
        user = await UserModel.get(db, email=email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await UserModel.update(db, id=user.id, **user_payload.model_dump())
        user = await UserModel.get(db, email=email)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@r.delete(
    "/{email}",
    response_model=UserResponse,
    responses={
        200: {"description": "User deleted"},
        404: {"description": "User not found"},
        500: {"description": "Internal server error"},
    },
)
async def delete_user(email: str, db: AsyncSession = Depends(get_db_session)):
    user = await UserModel.get(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await UserModel.delete(db, email=email)
    user = await UserModel.get(db, email=email)
    return user
