from fastapi import APIRouter, HTTPException, status
from starlette.responses import Response

from src.auth.services import get_password_hash, Users, create_access_token, authenticate_user
from src.auth.shemas import UserRegister, UserAuth


user_router = APIRouter(tags=['Auth'])

# Регистрация пользователя
@user_router.post("/register/")
async def register_user(user_data: UserRegister) -> dict:
    user = await Users.get_user(email=user_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Пользователь уже существует')
    user_dict = user_data.dict()
    user_dict['hashed_password'] = get_password_hash(user_data.hashed_password)
    await Users.add(**user_dict)
    return {'message': f'Вы успешно зарегистрированы!'}

# Аутентификация пользователя
@user_router.post("/login/")
async def auth_user(response: Response, user_data: UserAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.hashed_password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}