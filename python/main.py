import os
import aiosqlite
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import Response
from pydantic import BaseModel, Field
from typing import List, Optional

# --- Pydantic Schemas (openapi.yaml 기반) ---
class Post(BaseModel):
    id: str
    username: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=2000)
    createdAt: str
    updatedAt: str
    likesCount: int
    commentsCount: int

class Comment(BaseModel):
    id: str
    postId: str
    username: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=1000)
    createdAt: str
    updatedAt: str

class NewPostRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=2000)

class UpdatePostRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=2000)

class NewCommentRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=1000)

class UpdateCommentRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=1000)

class LikeRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)

class LikeResponse(BaseModel):
    postId: str
    username: str
    likedAt: str

class ErrorModel(BaseModel):
    error: str
    message: str
    details: Optional[List[str]] = None

# --- DB 초기화 ---
DB_PATH = os.path.join(os.path.dirname(__file__), "sns_api.db")
CREATE_POSTS = """
CREATE TABLE IF NOT EXISTS posts (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""
CREATE_COMMENTS = """
CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    post_id TEXT NOT NULL,
    username TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE
);
"""
CREATE_LIKES = """
CREATE TABLE IF NOT EXISTS likes (
    post_id TEXT NOT NULL,
    username TEXT NOT NULL,
    liked_at TEXT NOT NULL,
    PRIMARY KEY(post_id, username),
    FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE
);
"""
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_POSTS)
        await db.execute(CREATE_COMMENTS)
        await db.execute(CREATE_LIKES)
        await db.commit()

# --- FastAPI 앱 생성 및 CORS 설정 ---
app = FastAPI(
    title="Simple Social Media API",
    description="A basic Social Networking Service (SNS) API that allows users to create, retrieve, update, and delete posts; add comments; and like/unlike posts.",
    version="1.0.0",
    contact={"name": "Contoso Product Team", "email": "support@contoso.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url
    )

@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi():
    with open(os.path.join(os.path.dirname(__file__), "..", "openapi.yaml"), "r") as f:
        return Response(content=f.read(), media_type="application/json")
