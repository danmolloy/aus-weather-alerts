from sqlalchemy import Column, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, Mapped
from typing import List
from geoalchemy2 import Geometry
from .db import Base

alert_locality = Table(
    "alert_locality",
    Base.metadata,
    Column("alert_id", ForeignKey("alerts.id"), primary_key=True),
    Column("locality_name", ForeignKey("localities.locality_name"), primary_key=True)
)

class Locality(Base):
    __tablename__ = "localities"
    locality_name = Column(String, primary_key=True)
    state = Column(String)
    geom = Column(Geometry("POINT", srid=7844))
    alerts: Mapped[List["Alert"]] = relationship(
        "Alert",
        secondary=alert_locality,
        back_populates="localities"
    )
    heritage_sites: Mapped[List["HeritageSite"]] = relationship(
            "HeritageSite",
            back_populates="locality",
            cascade="all, delete-orphan"
        )
    radar_id = Column(String)

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

class BomRadar(Base):
    __tablename__ = "bom_radars"
    id = Column(String, primary_key=True)
    name = Column(String)
    geom = Column(Geometry("POINT", srid=7844)) 

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(String, primary_key=True)
    headline = Column(String)
    area = Column(String)
    expires_at = Column(DateTime)
    localities: Mapped[List["Locality"]] = relationship(
        "Locality",
        secondary=alert_locality,
        back_populates="alerts"
    )
    
""" class IndigenousLocation(Base):
    __tablename__ = "indigenous_locations"
    code = Column(String, primary_key=True)
    name = Column(String, index=True)
    state = Column(String)
    geom = Column(Geometry("MULTIPOLYGON", srid=4326))
    # geom = Column(Geometry("MULTIPOLYGON", srid=7844))

 """
