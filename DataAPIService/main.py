from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from routers import react_router, auth_router
from dotenv import load_dotenv
import uvicorn

load_dotenv()
app = FastAPI(title='Frontend Data API Service')

main_router = APIRouter()

#routers that translate data on frontend
main_router.include_router(react_router, tags=['frontend'])
main_router.include_router(auth_router, tags=['frontend/auth'])

@main_router.get('/')
async def healthy_check():
    return {'Hello':'Mr. Anderson'}

app.include_router(main_router)

origins = [
    "http://nginx",
    "http://localhost"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
