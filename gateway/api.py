from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import HTMLResponse, JSONResponse
from config.main import Settings, SECRET_SYSTEM, URL, fetch_data
from schemas.auth import SignUp, SignIn

app = FastAPI(
    title="XLFood",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://31.129.44.104:5001", "http://90.156.225.8:8000", "http://90.156.225.8:5123000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.on_event("startup")
async def startup_event():
    pass


@app.on_event("shutdown")
async def shutdown_event():
    pass


@app.post("/v1/signup", tags=['Account'])
async def signup(data: SignUp, Authorize: AuthJWT = Depends()):
    result = await fetch_data("authentification/registration/", "POST", data=data.model_dump(), headers={'SECRET-SYSTEM': SECRET_SYSTEM},)
    if result:
        access_token = Authorize.create_access_token(subject=result.get('user', None))
        return {
            'access_token': access_token,
            'customer_id': result.get('user', None)
        }
    else:
        return JSONResponse(status_code=400, content={'status': False})


@app.post("/v1/signin", tags=['Account'])
async def signup(data: SignIn, Authorize: AuthJWT = Depends()):
    result = await fetch_data("authentification/login/", "POST", data=data.model_dump(), headers={'SECRET-SYSTEM': SECRET_SYSTEM},)
    if result:
        access_token = Authorize.create_access_token(subject=result.get('user', None))
        return {
            'access_token': access_token,
            'customer_id': result.get('user', None)
        }
    else:
        return JSONResponse(status_code=400, content={'status': False})
