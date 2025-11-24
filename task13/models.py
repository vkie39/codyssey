from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base
#Base 클래스를 상송받아 questions 테이블과 매핑됨
"""
{컬럼 구성
id:
subject: 질문 제목
content: 질문내용, 긴 문자열
create_date: 작성일시: 기본값 현재시각으로 사용
}
"""
class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    content = Column(Text)
    create_date = Column(DateTime, default=func.now())

    def __repr__(self):
        return f'<Question {self.id}: {self.subject}>'
