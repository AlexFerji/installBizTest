from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    username: str = Field(..., min_length=3, max_length=20, description="Логин от 3 до 20 знаков")
    hashed_password: str = Field(..., min_length=4, max_length=20, description="Пароль от 4 до 20 символов")


class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    hashed_password: str = Field(..., min_length=4, max_length=20, description="Пароль, от 4 до 20 знаков")