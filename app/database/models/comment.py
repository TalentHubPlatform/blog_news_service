from sqlalchemy import Column, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database.models.base import BaseModel


class Comment(BaseModel):
    __tablename__ = "comments"
    __table_args__ = {'extend_existing': True}

    content = Column(Text, nullable=False)

    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False, index=True)
    author_id = Column(Integer, nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True, index=True)

    is_approved = Column(Boolean, default=True)

    post = relationship("Post", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")

    def __repr__(self):
        return f"<Comment(id={self.id}, post_id={self.post_id}, author_id={self.author_id})>"