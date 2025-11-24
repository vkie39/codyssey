#데이터베이스 연결 설정과 세션 생성기를 만드는 파일
"""
create_engine으로  SQLite 데이터베이스에 연결(파일 이름:test.db)
connent_args={'check_same_thread':False}
SessionLocal 은 데이터베이스 세션 객체를 생성하는 함수로, 이걸 통해 쿼리를 수행
Base는 ORM 모델들이 상속받는 베이스 클래스, 이걸 기준으로 테이블이 생성됨

core 데이터베이스 정의
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///./test.db'

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, pool_pre_ping=True)

# 세션 구성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 기본 클래스
Base = declarative_base()
