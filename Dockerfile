# 베이스 이미지로 ubuntu:22.04 사용
FROM ubuntu:22.04

ENV SECRET_KEY=4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03c
ENV ACCESS_TOKEN_EXPIRE_MINUTES=1440
ENV SQLALCHEMY_DATABASE_URL=sqlite:///./myapi.db
ENV SQLALCHEMY_DATABASE_URL_ASYNC=sqlite+aiosqlite:///./test.db
# 기본 패키지들 설치 및 Python 3 설치
RUN apt update
#RUN apt install -y git
#RUN apt install -y curl
RUN apt install -y python3-pip

ADD . /app

# 8000번 포트 개방 (FastAPI 웹 애플리케이션을 8000번 포트에서 띄움)
EXPOSE 8000

# 작업 디렉토리로 이동
WORKDIR /app

# 작업 디렉토리에 있는 requirements.txt로 패키지 설치
RUN pip install -r requirements.txt

# 컨테이너에서 실행될 명령어.
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]