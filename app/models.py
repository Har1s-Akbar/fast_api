from sqlalchemy import Boolean, Integer, String, Column, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW( )'))
    users_posts_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")

class User(Base):
    __tablename__ = 'users'

    id= Column(Integer, primary_key=True, nullable=False)
    mail= Column(String, nullable=False, unique=True)
    password= Column(String, nullable=False)
    created_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))

class Vote(Base):
    __tablename__ = "votes"
    posts_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    