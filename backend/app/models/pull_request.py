from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class PullRequest(Base):
    __tablename__ = "pull_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    
    # 建立与PullRequestRisk的关系
    risks = relationship("PullRequestRisk", back_populates="pull_request")

class PullRequestRisk(Base):
    __tablename__ = "pull_request_risks"
    
    id = Column(Integer, primary_key=True, index=True)
    pr_id = Column(Integer, ForeignKey("pull_requests.id"), nullable=False)
    score = Column(Float, nullable=False)
    level = Column(String, nullable=False)
    details = Column(JSON, nullable=False)
    
    # 建立与PullRequest的关系
    pull_request = relationship("PullRequest", back_populates="risks")