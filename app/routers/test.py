from fastapi import Body, Depends, FastAPI,Response,status,HTTPException,APIRouter

router = APIRouter(
    prefix="/welcome",
    tags=['Welcome']
)

@router.get("/")
async def welcome():
    return {"message": "Welcome to my fastAPI with bind mount"}