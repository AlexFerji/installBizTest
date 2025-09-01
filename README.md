Клонировать репозиторий - https://github.com/AlexFerji/installBizTest.git
Создать виртуальное окружение
Версия Python 3.12
Установить зависимости - pip install -r requirements.txt
добавить файл .env с данными: 
  DB_HOST=localhost
  DB_PORT=5432
  DB_NAME=Ваша БД
  DB_USER=Ваш пользователь
  DB_PASSWORD=Ваш пароль
  SECRET_KEY=Ваш секретный ключ
  ALGORITHM=HS256

  применить миграции - alembic upgrade head

  Документация - http://127.0.0.1:8000/docs
