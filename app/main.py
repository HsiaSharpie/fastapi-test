from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from fastapi.params import Body

from . import models
from .database import engine
from .routers import post, user, auth, vote

from .config import settings

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


app.middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
