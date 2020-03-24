from sqlalchemy import Column, Float, String ,Integer
from sqlalchemy.dialects.postgresql import JSON
from .database import Base


class Map(Base):
    __tablename__ = "mapping"

    key	= Column(String, primary_key=True, index=True)
    place_name = Column(String)
    admin_name1	= Column(String)
    latitude = Column(Float)
    longitude = Column(Float)	
    accuracy = Column(String)

class GeoJson(Base):
    __tablename__ = "geojson"
    id = Column(Integer , primary_key=True ,index =True)
    pro = Column(JSON)
    Geo = Column(JSON)


    