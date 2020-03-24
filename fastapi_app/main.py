from typing import List
from fastapi import Depends, FastAPI, HTTPException ,File, UploadFile
from sqlalchemy.orm import Session
from . import crud, models, schemas , utils
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/Location/")
def Post_Location(loc: schemas.LocCreate, db: Session = Depends(get_db)):
    db_loc = crud.get_Loc_by_Pin(db, key = loc.key)
    if db_loc:
        raise HTTPException(status_code=400, detail="Pincode already In Database")
    return crud.create_Loc(db=db, loc=loc)

@app.get("/Location/{latitude}{longitude}")
def Get_Location(Latitude: float ,Longitude : float , db: Session = Depends(get_db)):
    db_loc = crud.get_Loc(db, Latitude = Latitude  ,Longitude = Longitude)
    if db_loc is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_loc

@app.get("/EarthDistance_postgres/{latitude}{longitude}{radius}")
def get_using_postgres(Latitude: float ,Longitude : float ,Radius : float, db: Session = Depends(get_db)):
    result = crud.get_place_distance(db, Latitude = Latitude  ,Longitude = Longitude ,Radius = Radius)
    if result is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return result

@app.get("/EarthDistance_myself/{latitude}{longitude}{radius}")
def get_using_myself(Latitude: float ,Longitude : float ,Radius : float, db: Session = Depends(get_db)):
    result = crud.get_place_distance_myself(db, Latitude = Latitude  ,Longitude = Longitude ,Radius = Radius)
    if result is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return result
@app.get("/Detect/{latitude}{longitude}")
def Get_Location_from_json(Latitude: float ,Longitude : float , db: Session = Depends(get_db)):
    db_loc = crud.Get_Loc_from_json(db, Latitude = Latitude  ,Longitude = Longitude)
    if db_loc is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_loc

@app.post("/uploadJson File/")
def upload_json(jsonfile: UploadFile = File(...),db: Session = Depends(get_db)):
    return utils.loadjson(db,jsonfile = jsonfile )

@app.post("/uploadcsv File/")
def upload_csv(csv_file: UploadFile = File(...),db: Session = Depends(get_db)):
    return utils.loadcsv(db,csv_file = csv_file )
 