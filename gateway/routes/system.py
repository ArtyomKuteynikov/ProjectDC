from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from config.main import fetch_data, SECRET_SYSTEM

router = APIRouter(prefix="", tags=["System"])


@router.get("/v1/cities", tags=['System'])
async def cities():
    result = await fetch_data("authentification/cities/", "GET", headers={'SECRET-SYSTEM': SECRET_SYSTEM}, )
    if result:
        return JSONResponse(status_code=200, content=result)
    else:
        return JSONResponse(status_code=400, content={'status': False})


@router.get("/v1/grades", tags=['System'])
async def grades():
    result = await fetch_data("authentification/grades/", "GET", headers={'SECRET-SYSTEM': SECRET_SYSTEM}, )
    if result:
        return JSONResponse(status_code=200, content=result)
    else:
        return JSONResponse(status_code=400, content={'status': False})


@router.get("/v1/specs", tags=['System'])
async def specs():
    result = await fetch_data("authentification/specs/", "GET", headers={'SECRET-SYSTEM': SECRET_SYSTEM}, )
    if result:
        return JSONResponse(status_code=200, content=result)
    else:
        return JSONResponse(status_code=400, content={'status': False})
