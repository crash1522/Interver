## 종속성 설치
* pip3 install -r requirements.txt
## FastAPI 서버 실행
* uvicorn main:app --reload


## alembic
* alembic init migrations
* alembic revision --autogenerate
* alembic upgrade head

## docker
docker compose up
