from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/api/common",
)
templates = Jinja2Templates(directory="templates")

@router.get("/service", response_class=HTMLResponse)
async def get_service(request: Request):
    return templates.TemplateResponse("service.html", {"request": request})


@router.get("/mypage", response_class=HTMLResponse)
async def get_mypage(request: Request):
    return templates.TemplateResponse("mypage.html", {"request": request})


@router.get("/record", response_class=HTMLResponse)
async def get_record(request: Request):
    return templates.TemplateResponse("record.html", {"request": request})


@router.get("/sign_up", response_class=HTMLResponse)
async def get_sign_up(request: Request):
    return templates.TemplateResponse("sign_up.html", {"request": request})

@router.get("/interview_prepare", response_class=HTMLResponse)
async def get_interview_prepare(request: Request):
    return templates.TemplateResponse("interview_prepare.html", {"request": request})

@router.get("/interview_all_repo", response_class=HTMLResponse)
async def get_interview_all_repo(request: Request):
    return templates.TemplateResponse("interview_all_repo.html", {"request": request})