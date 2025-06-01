import uuid
from datetime import datetime
from typing import List, Optional, Annotated
import uuid

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, relationship, declarative_base


# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./sns_api.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False  # Set to True for debugging
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database initialization will happen in startup event


# Database Models
class PostDB(Base):
    __tablename__ = "posts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), nullable=False)
    content = Column(String(2000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    comments = relationship("CommentDB", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("LikeDB", back_populates="post", cascade="all, delete-orphan")


class CommentDB(Base):
    __tablename__ = "comments"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    post_id = Column(String, ForeignKey("posts.id"), nullable=False)
    username = Column(String(50), nullable=False)
    content = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    post = relationship("PostDB", back_populates="comments")


class LikeDB(Base):
    __tablename__ = "likes"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    post_id = Column(String, ForeignKey("posts.id"), nullable=False)
    username = Column(String(50), nullable=False)
    liked_at = Column(DateTime, default=datetime.utcnow)
    
    post = relationship("PostDB", back_populates="likes")


# Pydantic Models (Request/Response schemas)
class NewPostRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=2000)


class UpdatePostRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=2000)


class Post(BaseModel):
    id: str
    username: str
    content: str
    createdAt: datetime = Field(alias="created_at", serialization_alias="createdAt")
    updatedAt: datetime = Field(alias="updated_at", serialization_alias="updatedAt")
    likesCount: int
    commentsCount: int
    
    class Config:
        populate_by_name = True
        from_attributes = True


class NewCommentRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=1000)


class UpdateCommentRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=1000)


class Comment(BaseModel):
    id: str
    postId: str = Field(alias="post_id", serialization_alias="postId")
    username: str
    content: str
    createdAt: datetime = Field(alias="created_at", serialization_alias="createdAt")
    updatedAt: datetime = Field(alias="updated_at", serialization_alias="updatedAt")
    
    class Config:
        populate_by_name = True
        from_attributes = True


class LikeRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)


class LikeResponse(BaseModel):
    postId: str = Field(serialization_alias="postId")
    username: str
    likedAt: datetime = Field(serialization_alias="likedAt")
    
    class Config:
        populate_by_name = True


class Error(BaseModel):
    error: str
    message: str
    details: Optional[List[str]] = None


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]


# FastAPI app
app = FastAPI(
    title="Simple Social Media API",
    description="A basic Social Networking Service (SNS) API that allows users to create, retrieve, update, and delete posts; add comments; and like/unlike posts.",
    version="1.0.0",
    contact={
        "name": "Contoso Product Team",
        "email": "support@contoso.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    servers=[
        {"url": "http://localhost:8000", "description": "Local development server"}
    ]
)

# Add CORS middleware to allow requests from everywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


# Helper functions
def get_post_counts(db: Session, post: PostDB) -> tuple[int, int]:
    likes_count = db.query(LikeDB).filter(LikeDB.post_id == post.id).count()
    comments_count = db.query(CommentDB).filter(CommentDB.post_id == post.id).count()
    return likes_count, comments_count


def post_to_response(db: Session, post: PostDB) -> Post:
    likes_count, comments_count = get_post_counts(db, post)
    return Post(
        id=post.id,
        username=post.username,
        content=post.content,
        createdAt=post.created_at,
        updatedAt=post.updated_at,
        likesCount=likes_count,
        commentsCount=comments_count
    )


# Routes - Posts
@app.get("/api/posts", response_model=List[Post], tags=["Posts"])
def get_posts(db: SessionDep):
    """List all posts"""
    posts = db.query(PostDB).order_by(PostDB.created_at.desc()).all()
    return [post_to_response(db, post) for post in posts]


@app.post("/api/posts", response_model=Post, status_code=201, tags=["Posts"])
def create_post(post_data: NewPostRequest, db: SessionDep):
    """Create a new post"""
    post = PostDB(
        id=str(uuid.uuid4()),
        username=post_data.username,
        content=post_data.content
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post_to_response(db, post)


@app.get("/api/posts/{post_id}", response_model=Post, tags=["Posts"])
def get_post_by_id(post_id: str, db: SessionDep):
    """Get a specific post"""
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"error": "NOT_FOUND", "message": "The requested resource was not found"}
        )
    return post_to_response(db, post)


@app.patch("/api/posts/{post_id}", response_model=Post, tags=["Posts"])
def update_post(post_id: str, post_data: UpdatePostRequest, db: SessionDep):
    """Update a post"""
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"error": "NOT_FOUND", "message": "The requested resource was not found"}
        )
    
    post.username = post_data.username
    post.content = post_data.content
    post.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(post)
    return post_to_response(db, post)


@app.delete("/api/posts/{post_id}", status_code=204, tags=["Posts"])
def delete_post(post_id: str, db: SessionDep):
    """Delete a post"""
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"error": "NOT_FOUND", "message": "The requested resource was not found"}
        )
    
    db.delete(post)
    db.commit()


# Routes - Comments
@app.get("/api/posts/{post_id}/comments", response_model=List[Comment], tags=["Comments"])
def get_comments_by_post_id(post_id: str, db: SessionDep):
    """List comments for a post"""
    # Check if post exists
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"error": "NOT_FOUND", "message": "The requested resource was not found"}
        )
    
    comments = db.query(CommentDB).filter(CommentDB.post_id == post_id).order_by(CommentDB.created_at.asc()).all()
    return [Comment.model_validate(comment) for comment in comments]


@app.post("/api/posts/{post_id}/comments", response_model=Comment, status_code=201, tags=["Comments"])
def create_comment(post_id: str, comment_data: NewCommentRequest, db: SessionDep):
    """Create a comment"""
    # Check if post exists
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"error": "NOT_FOUND", "message": "The requested resource was not found"}
        )
    
    comment = CommentDB(
        id=str(uuid.uuid4()),
        post_id=post_id,
        username=comment_data.username,
        content=comment_data.content
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return Comment.model_validate(comment)


@app.get("/api/posts/{post_id}/comments/{comment_id}", response_model=Comment, tags=["Comments"])
def get_comment_by_id(post_id: str, comment_id: str, db: SessionDep):
    """Get a specific comment"""
    # Check if post exists
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"error": "NOT_FOUND", "message": "The requested resource was not found"}
        )
    
    comment = db.query(CommentDB).filter(
        CommentDB.id == comment_id,
        CommentDB.post_id == post_id
    ).first()
    if not comment:
        raise HTTPException(
            status_code=404,
            detail={"error": "NOT_FOUND", "message": "The requested resource was not found"}
        )
    
    return Comment.model_validate(comment)


@app.patch("/api/posts/{post_id}/comments/{comment_id}", response_model=Comment, tags=["Comments"])
def update_comment(post_id: str, comment_id: str, comment_data: UpdateCommentRequest, db: SessionDep):
    """Update a comment"""
    # Check if post exists
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"error": "NOT_FOUND", "message": "The requested resource was not found"}
        )
    
    comment = db.query(CommentDB).filter(
        CommentDB.id == comment_id,
        CommentDB.post_id == post_id
    ).first()
    if not comment:
        raise HTTPException(
            status_code=404,
            detail={"error": "NOT_FOUND", "message": "The requested resource was not found"}
        )
    
    comment.username = comment_data.username
    comment.content = comment_data.content
    comment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(comment)
    return Comment.model_validate(comment)


@app.delete("/api/posts/{post_id}/comments/{comment_id}", status_code=204, tags=["Comments"])
def delete_comment(post_id: str, comment_id: str, db: SessionDep):
    """Delete a comment"""
    # Check if post exists
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"error": "NOT_FOUND", "message": "The requested resource was not found"}
        )
    
    comment = db.query(CommentDB).filter(
        CommentDB.id == comment_id,
        CommentDB.post_id == post_id
    ).first()
    if not comment:
        raise HTTPException(
            status_code=404,
            detail={"error": "NOT_FOUND", "message": "The requested resource was not found"}
        )
    
    db.delete(comment)
    db.commit()


# Routes - Likes
@app.post("/api/posts/{post_id}/likes", response_model=LikeResponse, status_code=201, tags=["Likes"])
def like_post(post_id: str, like_data: LikeRequest, db: SessionDep):
    """Like a post"""
    # Check if post exists
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"error": "NOT_FOUND", "message": "The requested resource was not found"}
        )
    
    # Check if user already liked this post
    existing_like = db.query(LikeDB).filter(
        LikeDB.post_id == post_id,
        LikeDB.username == like_data.username
    ).first()
    
    if existing_like:
        raise HTTPException(
            status_code=400,
            detail={"error": "VALIDATION_ERROR", "message": "User has already liked this post"}
        )
    
    like = LikeDB(
        id=str(uuid.uuid4()),
        post_id=post_id,
        username=like_data.username
    )
    db.add(like)
    db.commit()
    db.refresh(like)
    
    return LikeResponse(
        postId=like.post_id,
        username=like.username,
        likedAt=like.liked_at
    )


@app.delete("/api/posts/{post_id}/likes", status_code=204, tags=["Likes"])
def unlike_post(post_id: str, db: SessionDep):
    """Unlike a post"""
    # Check if post exists
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"error": "NOT_FOUND", "message": "The requested resource was not found"}
        )
    
    # For simplicity, we'll delete all likes for this post
    # In a real app, you'd need authentication to know which user to unlike
    likes = db.query(LikeDB).filter(LikeDB.post_id == post_id).all()
    if not likes:
        raise HTTPException(
            status_code=404,
            detail={"error": "NOT_FOUND", "message": "No likes found for this post"}
        )
    
    for like in likes:
        db.delete(like)
    db.commit()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
