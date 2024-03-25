# 베이스 이미지로 ubuntu:22.04 사용
FROM ubuntu:22.04

# 기본 패키지들 설치 및 Python 3 설치
RUN apt update
#RUN apt install -y git
#RUN apt install -y curl
RUN apt install -y python3-pip

ADD . /api

# 8000번 포트 개방 (FastAPI 웹 애플리케이션을 8000번 포트에서 띄움)
EXPOSE 8000

# 작업 디렉토리로 이동
WORKDIR /api

# 작업 디렉토리에 있는 requirements.txt로 패키지 설치
RUN pip install -r requirements.txt

# 컨테이너에서 실행될 명령어.
CMD [ "/bin/bash" ]
