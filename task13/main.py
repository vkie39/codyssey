#문제5 데이터베이스를 또…

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Question, Base

# fastapi: 웹 프레임워크
# 프런트를 구성해서 백엔드를 테스트하는게 낫다
# uvicorn: FastAPI 서버 실행
# sqlalchemy : ORM
# alembic DB 마이그레이션 도구
# 동기 비동기 관련
# 데이터베이스와 테이블 생성
# 만약 앱 시작 시 테이블이 없으면 생성(Alembic 마이그레이션과 병행이 가능함.)
# domain에 추가해야 함
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 데이터베이스 세션을 얻는 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 질문 작성 엔드포인트
@app.post("/question/")
def create_question(subject: str, content: str, db: Session = Depends(get_db)):
    db_question = Question(subject=subject, content=content)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

# 모든 질문 조회 엔드포인트
@app.get("/question/")
def get_question(db: Session = Depends(get_db)):
    return db.query(Question).all()

# 특정 질문 조회 엔드포인트
@app.get("/question/{question_id}")
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question
