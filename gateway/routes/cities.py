from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from models.city import City
from schemas.city import (
    CityRead,
    CityCreate,
    CityUpdate
)
from config.database import get_db

router = APIRouter(
    prefix="/v1/city",
    tags=['City']
)


@router.get("/{city_id}", response_model=CityRead)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = db.query(City).filter(City.id == city_id).first()
    if db_city is None:
        raise HTTPException(status_code=404, detail='City not found')
    return db_city


@router.get("/all", response_model=List[CityRead])
async def read_cities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cities = db.query(City).offset(skip).limit(limit).all()
    return cities


@router.post('/', response_model=CityRead)
async def create_city(city: CityCreate, db: Session = Depends(get_db)):
    db_city = City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@router.put("/{city_id}", response_model=CityRead)
def update_city(city_id: int, city: CityUpdate, db: Session = Depends(get_db)):
    db_city = db.query(City).filter(City.id == city_id).first()
    if db_city is None:
        return None
    for key, value in city.dict().items():
        setattr(db_city, key, value)
    db.commit()
    return db_city


@router.delete("/{city_id}", response_model=CityRead)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = delete_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city
