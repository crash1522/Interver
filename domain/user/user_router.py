from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from starlette.config import Config

from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context

config = Config('.env')
ACCESS_TOKEN_EXPIRE_MINUTES = int(config('ACCESS_TOKEN_EXPIRE_MINUTES'))
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

router = APIRouter(
    prefix="/api/user",
)


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userid: str = payload.get("sub")
        if userid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user(db, userid=userid)
        if user is None:
            raise credentials_exception
        return user


# 유저를 생성합니다. (회원가입)
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db=db, user_create=_user_create)

@router.post("/create/is_duplcate")
def is_duplcate(request: user_schema.UserIdRequest, db: Session = Depends(get_db)):
    userid = request.userid
    user = user_crud.get_user(db, userid=userid)
    if user:
        return {"message": "이미 존재하는 아이디입니다."}
    else:
        return {"message": "사용 가능한 아이디입니다."}

# 로그인
@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):

    # check user and password
    user = user_crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호를 잘못 입력했습니다.\n입력하신 내용을 다시 확인해주세요.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    payload = {
        "sub": user.userid,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "userid": user.userid
    }


"""
# 유저를 삭제합니다. (회원탈퇴)
@router.post("/withdrawal", status_code=status.HTTP_204_NO_CONTENT)
def user_delete(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    records = user_crud.get_records_by_userid(db=db, userid=current_user.userid)
    for record in records:
        delete_record(db=db, db_record=record)
    user_crud.delete_user(db=db, userid=current_user.userid)
"""

"""
test codes
"""
@router.get("/users/{userid}/skills")
def read_user_skills(userid: str, db: Session = Depends(get_db)):
    skills = user_crud.get_skills(db, userid)
    return {"skills": skills}


@router.get("/users/{userid}/field")
def read_user_field(userid: str, db: Session = Depends(get_db)):
    field = user_crud.get_field(db, userid)
    return {"field": field}


@router.get("/users/{userid}/username")
def read_user_username(userid: str, db: Session = Depends(get_db)):
    username = user_crud.get_username(db, userid)
    return {"username": username}


@router.get("/users/{userid}/{new_username}/set_user_username")
def set_user_username(userid: str, new_username,db: Session = Depends(get_db)):
    username = user_crud.set_username(db, userid, new_username)
    return {"username": username}


@router.get("/users/{userid}/{new_skill_name}/add_user_skill")
def add_user_skill(userid: str, new_skill_name: str, db: Session = Depends(get_db)):
    new_skill = user_crud.add_skill_to_user(db, userid, new_skill_name)
    return {"new_skill": new_skill}


@router.get("/users/{userid}/{to_delete_skill_name}/delete_user_skill")
def delete_user_skill(userid: str, to_delete_skill_name: str, db: Session = Depends(get_db)):
    user_crud.delete_skill_from_user(db, userid, to_delete_skill_name)
    