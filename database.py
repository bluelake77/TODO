import os

import cx_Oracle
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

# tnsnames.ora 가 위치한 디렉터리를 TNS_ADMIN 으로 설정
# .env 에 TNS_ADMIN 이 있으면 그 값을 우선 사용
TNS_ADMIN = os.getenv(
    "TNS_ADMIN",
    r"C:\Oracle\product\11.2.0\client\network\admin",
)
os.environ["TNS_ADMIN"] = TNS_ADMIN

# Oracle Thick 모드: 설치된 Oracle 19c 클라이언트 라이브러리를 직접 사용
ORACLE_CLIENT_LIB = os.getenv(
    "ORACLE_CLIENT_LIB",
    r"C:\Oracle\product\11.2.0\client\BIN",
)
try:
    cx_Oracle.init_oracle_client(lib_dir=ORACLE_CLIENT_LIB)
except cx_Oracle.ProgrammingError as exc:
    # uvicorn reload or repeated imports can initialize Oracle client more than once
    if "already been initialized" not in str(exc):
        raise

# oracle+cx_oracle://계정:비밀번호@TNS별칭
# TNS 별칭(DEV)은 tnsnames.ora 의 항목명과 일치해야 함
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "oracle+cx_oracle://username:password@DEV",
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,       # 기본 커넥션 풀 크기
    max_overflow=20,    # 풀 초과 시 추가로 허용할 커넥션 수
    pool_pre_ping=True, # 끊어진 커넥션 자동 감지 후 재연결
    pool_recycle=1800,  # 30분마다 커넥션 재생성 (방화벽 세션 만료 방지)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
