from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.api import user_router
app = FastAPI(
    title="installBizTest"
)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "ws://http//localhost:8000",
    "ws://http//localhost:8080",
    "ws://http//localhost:3000",
    'ws://http//127.0.0.1:8000',

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)