import logging
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import expression as sql
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.base import BaseModel
from app.engine.postgresdb import Base
from app.schema.index import UserCreate, UserUpdate

logger = logging.getLogger(__name__)


class User(Base, BaseModel):
    __tablename__ = "users"

    name: Mapped[str]
    email: Mapped[str]
    hashed_password: Mapped[str]
    is_deleted: Mapped[bool] = mapped_column(default=False)

    @classmethod
    async def create(cls: "type[User]", db: AsyncSession, **kwargs: UserCreate) -> "User":
        """
        Creates a new user in the database.

        Args:
            cls (type[User]): The class object representing the User model.
            db (AsyncSession): The asynchronous session object for interacting with the database.
            **kwargs (UserCreate): The keyword arguments representing the user's attributes.

        Returns:
            User
        """

        print(f"Creating user: {kwargs}")
        # query = sql.insert(cls).values(**kwargs)
        user = cls(name=kwargs["name"], email=kwargs["email"], hashed_password=kwargs["hashed_password"])
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @classmethod
    async def update(cls: "type[User]", db: AsyncSession, id: int, **kwargs: UserUpdate) -> "User":
        """
        Updates a user in the database with the given ID and keyword arguments.

        Args:
            cls (type[User]): The class object representing the User model.
            db (AsyncSession): The asynchronous session object for interacting with the database.
            id (int): The ID of the user to update.
            **kwargs (UserUpdate): The keyword arguments representing the user's attributes to update.

        Returns:
            User
        """

        query = sql.update(cls).where(cls.id == id).values(**kwargs).execution_options(synchronize_session="fetch")
        results = await db.execute(query)
        user = results.fetchone()
        await db.commit()
        return user

    @classmethod
    async def get(cls: "type[User]", db: AsyncSession, email: str) -> "User":
        """
        Retrieves a user from the database based on their email.

        Args:
            cls (type[User]): The class object representing the User model.
            db (AsyncSession): The asynchronous session object for interacting with the database.
            email (str): The email of the user to retrieve.

        Returns:
            User
        """

        logging.info(f"Getting user: {email}")
        query = sql.select(cls).where(cls.email == email)
        logging.info(f"Query: {query}")
        users = await db.scalars(query)
        logging.info(f"Users: {users}")
        return users.first()

    @classmethod
    async def delete(cls: "type[User]", db: AsyncSession, email: str) -> "User":
        """
        Deletes a user from the database based on their email.

        Args:
            cls (type[User]): The class object representing the User model.
            db (AsyncSession): The asynchronous session object for interacting with the database.
            email (str): The email of the user to delete.

        Returns:
            User
        """
        query = (
            sql.update(cls)
            .where(cls.email == email)
            .values(is_deleted=True)
            .execution_options(synchronize_session="fetch")
        )
        result = await db.execute(query)
        user = result.fetchone()
        await db.commit()
        return user
