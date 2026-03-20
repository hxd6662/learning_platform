import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

MAX_RETRY_TIME = 20

Base = declarative_base()

def get_mysql_url() -> str:
    host = os.getenv("MYSQL_HOST", "localhost")
    port = os.getenv("MYSQL_PORT", "3306")
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "learning_platform")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4"

_engine = None
_SessionLocal = None

def _create_engine_with_retry():
    url = get_mysql_url()
    if not url:
        logger.error("MySQL configuration is not set")
        raise ValueError("MySQL configuration is not set")
    
    size = 100
    overflow = 100
    recycle = 1800
    timeout = 30
    
    engine = create_engine(
        url,
        pool_size=size,
        max_overflow=overflow,
        pool_pre_ping=True,
        pool_recycle=recycle,
        pool_timeout=timeout,
        echo=False
    )
    
    start_time = time.time()
    last_error = None
    while time.time() - start_time < MAX_RETRY_TIME:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return engine
        except OperationalError as e:
            last_error = e
            elapsed = time.time() - start_time
            logger.warning(f"MySQL connection failed, retrying... (elapsed: {elapsed:.1f}s)")
            time.sleep(min(1, MAX_RETRY_TIME - elapsed))
    
    logger.error(f"MySQL connection failed after {MAX_RETRY_TIME}s: {last_error}")
    raise last_error

def get_engine():
    global _engine
    if _engine is None:
        _engine = _create_engine_with_retry()
    return _engine

def get_sessionmaker():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal

def get_session():
    return get_sessionmaker()()

def init_db():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

__all__ = [
    "Base",
    "get_mysql_url",
    "get_engine",
    "get_sessionmaker",
    "get_session",
    "init_db",
]
