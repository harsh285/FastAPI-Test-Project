from sqlalchemy.orm import Session
from . import models, schemas , utils
import json


def create_Loc(db: Session, loc: schemas.LocCreate):
    db_loc = models.Map(key=loc.key, place_name = loc.place_name, admin_name1 = loc.admin_name1, latitude=loc.latitude, longitude=loc.longitude, accuracy=loc.accuracy)
    db.add(db_loc)
    db.commit()
    db.refresh(db_loc)
    return db_loc

def create_Loc1(db: Session ,column : list):
    db_loc = models.Map(key=str(column[0]), place_name = str(column[1]), admin_name1 = str(column[2]), latitude=column[3], longitude=column[4], accuracy=column[5])
    db.add(db_loc)
    db.commit()
    db.refresh(db_loc)
    return db_loc

def get_Loc(db: Session, Latitude: float ,Longitude :float):
    return db.query(models.Map).filter(models.Map.latitude == Latitude and models.Map.longitude == Longitude).first()

def Get_Loc_from_json(db: Session, Latitude = float ,Longitude = float):
    l=[]
    l.append(Latitude)
    l.append(Longitude)
    result = db.query(models.GeoJson.Geo).all()
    name = db.query(models.GeoJson.pro).all()
    for i in range(len(result)):
        for j in range(len(result[i][0]['coordinates'][0])):
            if result[i][0]['coordinates'][0][j] == l :
                return name[i]
    return None
    
def get_Loc_by_Pin(db: Session, key: str):
    return db.query(models.Map).filter(models.Map.key == key).first()

def get_place_distance(db: Session, Latitude: float ,Longitude :float ,Radius :float):
    query1 = 'select key, earth_distance(ll_to_earth(a.latitude, a.longitude),ll_to_earth(%s, %s)) as distance from mapping a;' % (Latitude,Longitude)
    result = list(db.execute(query1))
    l=[]
    for i in range(len(result)):
        a=(result[i]['distance'])/1000
        if(a <= Radius):
            l.append(str(result[i]['key'])+" , " + str(a) + " KM ")    
    return l
   # pname = [(row[0],row[1]) for row in result if row[1] <= (radius*1000)]   
def get_place_distance_myself(db: Session, Latitude: float ,Longitude :float ,Radius :float):
    query2 = 'select key,latitude,longitude from mapping'
    result = db.execute(query2)
    dict1 = utils.mathcal_distance(result,Latitude,Longitude,Radius)  
    return dict1

def json_to_db(db : Session, list1 : list):
    db_loc = models.GeoJson(pro = list1[0] ,Geo = list1[1])
    db.add(db_loc)
    db.commit()
    db.refresh(db_loc)
    return db_loc

    







