from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from typing import List
from geoalchemy2 import Geometry
from .db import Base

class Locality(Base):
    __tablename__ = "localities"
    locality_name = Column(String, primary_key=True)
    state = Column(String)
    geom = Column(Geometry("POINT", srid=7844))
    heritage_sites: Mapped[List["HeritageSite"]] = relationship(
            "HeritageSite",
            back_populates="locality",
            cascade="all, delete-orphan"
        )

class HeritageSite(Base):
    __tablename__ = "heritage_sites"
    id = Column(String, primary_key=True)
    name = Column(String)
    geom = Column(Geometry("MULTIPOLYGON", srid=7844))
    locality_name = Column(String, ForeignKey("localities.locality_name"))
    locality: Mapped["Locality"] = relationship(
        "Locality",
        back_populates="heritage_sites"
    )
    
""" class IndigenousLocation(Base):
    __tablename__ = "indigenous_locations"
    code = Column(String, primary_key=True)
    name = Column(String, index=True)
    state = Column(String)
    geom = Column(Geometry("MULTIPOLYGON", srid=4326))
    # geom = Column(Geometry("MULTIPOLYGON", srid=7844))

 """
