  ## 가상 환경 생성:

- Windows: python -m venv myapi
- Mac/Linux: python3 -m venv myapi
  
myapi는 생성할 가상 환경의 이름입니다. 이름은 자유롭게 지정할 수 있습니다.
## 가상 환경 활성화:
- Windows: cd C:\venvs\myapi\Scripts
- activate
<br>

- Mac/Linux:
- source myapi/bin/activate
  
활성화하면 커맨드 라인 프롬프트에 가상 환경의 이름이 표시됩니다.
## 가상 환경 비활성화:
- 어느 환경에서나: deactivate
  
가상 환경을 벗어나면 커맨드 라인 프롬프트에 가상 환경 이름이 사라집니다.

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
