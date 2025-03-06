import jwt
import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from passlib.context import CryptContext
from settings import settings

auth_router = APIRouter(prefix='/auth')

# FAKE_USERS_DB = settings.FAKE_USERS_DB
FAKE_USERS_DB = {'admin': 
                 {'username': settings.AUTH_FAKE_USER, 
                  'password': settings.AUTH_FAKE_PASSWORD, 
                  'hashed_password': settings.AUTH_HASHED_PASSWORD
                  },}
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MIN = int(settings.ACCESS_TOKEN_EXPIRE_MIN)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    password: str

def create_token(data: dict, expire_delta: int|None = None):
    to_encode = data.copy()
    if expire_delta:
        expire =  datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=expire_delta)
    else:
        expire =  datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@auth_router.post("/token")
async def login(user: User):
    json_user = jsonable_encoder(user) 
    if json_user["username"] in FAKE_USERS_DB:
        verified = verify_password(plain_password = json_user["password"], 
                                   hashed_password = FAKE_USERS_DB[json_user["username"]]["hashed_password"])
        assert isinstance(verified, bool), 'Verify password process is broken'
        if verified:
            acc_token = create_token(data={'username':json_user["username"]}, expire_delta=ACCESS_TOKEN_EXPIRE_MIN)
            return {"access_token": acc_token, 'token_type': 'bearer'}
    return {"error": "Invalid credentials"}


@auth_router.get("/validate_token")
async def secure_data(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expiration = payload['exp'] - datetime.datetime.now(datetime.timezone.utc).timestamp()
        if expiration < 0 :
            raise HTTPException(status_code=401, detail="Token has been expired")
        #obviously need more verify logic
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"hello": "mr anderson"}