from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

# 1. 数据库配置 (使用 SQLite 本地文件，方便测试)
SQLALCHEMY_DATABASE_URL = "sqlite:///./drone_ai_service.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# 2. 定义数据库模型

class SessionModel(Base):
    """会话表：记录用户的 session_id"""
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # 关系：一个会话对应多条消息
    messages = relationship("MessageModel", back_populates="session")


class MessageModel(Base):
    """消息表：记录具体的对话内容"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.session_id"), nullable=False)
    role = Column(String, nullable=False)  # 'user' 或 'assistant'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # 关系：属于某个会话
    session = relationship("SessionModel", back_populates="messages")


# ================= 新增：知识库数据模型 =================
class KnowledgeModel(Base):
    """知识库表：存储无人机销售/售后问答数据"""
    __tablename__ = 'knowledge_base'

    id = Column(Integer, primary_key=True, index=True)  # 知识条目ID
    question = Column(String(255), nullable=False)  # 用户可能问的问题
    answer = Column(Text, nullable=False)  # 专业的标准回答
    category = Column(String(50), default="通用")  # 分类：如 "销售"、"售后维修"、"飞行政策"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # 创建时间

    def __repr__(self):
        return f"<Knowledge(question='{self.question}', category='{self.category}')>"


# =========================================================


# 3. 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()