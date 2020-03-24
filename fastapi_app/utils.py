from sqlalchemy.orm import Session
from . import models , crud
import io ,csv ,json
from math import sin,cos,radians,sqrt,asin


def loadcsv(db: Session, csv_file : object):
    data_set = csv_file.file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        db_pin = crud.get_Loc_by_Pin(db, key = column[0])
        if column[3]=='' or column[4] =='':
            column[3] = 0
            column[4] = 0 
        if db_pin :
            continue
        else:
            crud.create_Loc1(db=db,column = column)
    return {"filename": csv_file.filename}

def loadjson(db: Session, jsonfile : object):
    data = json.load(jsonfile.file)
    list1 = []
    for i in range(len(data['features'])):
        list1.append(data['features'][i]['properties'])
        list1.append(data['features'][i]['geometry'])
        crud.json_to_db(db,list1)
        list1.clear()
    return jsonfile.filename


def mathcal_distance(result,Latitude,Longitude,Radius):
    dict1 = {}
    for row in result:
        lon1 = radians(Longitude) 
        lon2 = radians(row[2]) 
        lat1 = radians(Latitude) 
        lat2 = radians(row[1]) 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = (sin(dlat / 2)**2) + (cos(lat1) * cos(lat2) * (sin(dlon / 2)**2))
        c = 2 * asin(sqrt(a))
        d = c*6371
        if d <= Radius:
            dict1.update( {row[0] : str(d) + " KM "} )
    return dict1




