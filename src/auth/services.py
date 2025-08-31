from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from jose import jwt
from datetime import datetime, timedelta, timezone


from src.database import async_session_maker
from src.config import get_auth_data
from src.auth.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # контекст для хэширования паролей


# Создание хэша пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Проверка пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Создание токена jwt
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt





class Users:
    model = User

    # Проверка нет ли такого пользователя в базе
    @classmethod
    async def get_user(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    # Добавление нового пользователя
    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance


# Сверка с базой данных
async def authenticate_user(email: EmailStr, password: str):
    user = await Users.get_user(email=email)
    if not user or verify_password(plain_password=password, hashed_password=user.hashed_password) is False:
        return None
    return user