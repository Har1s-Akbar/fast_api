from sqlalchemy import Boolean, Integer, String, Column
from .database import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')