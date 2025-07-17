from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey, Numeric
from uuid import uuid4
from app.db.base import Base
from sqlalchemy.orm import relationship


class Country(Base):
    __tablename__ = 'countries'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    iso_code = Column(String(10), nullable=False, unique=True)

    def __repr__(self):
        return f"<Country {self.name}>"


class State(Base):
    __tablename__ = 'states'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    country_id = Column(UUID(as_uuid=True), ForeignKey('countries.id'), nullable=False)

    country = relationship("Country", backref="states")

    def __repr__(self):
        return f"<State {self.name}>"


class City(Base):
    __tablename__ = 'cities'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    state_id = Column(UUID(as_uuid=True), ForeignKey('states.id'), nullable=False)

    state = relationship("State", backref="cities")

    def __repr__(self):
        return f"<City {self.name}>"


class Area(Base):
    __tablename__ = 'areas'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    city_id = Column(UUID(as_uuid=True), ForeignKey('cities.id'), nullable=False)

    city = relationship("City", backref="areas")

    def __repr__(self):
        return f"<Area {self.name}>"


class Locality(Base):
    __tablename__ = 'localities'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    area_id = Column(UUID(as_uuid=True), ForeignKey('areas.id'), nullable=False)
    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)

    area = relationship("Area", backref="localities")

    @property
    def city(self):
        return self.area.city if self.area else None

    @property
    def state(self):
        return self.city.state if self.city else None

    @property
    def country(self):
        return self.state.country if self.state else None

    @property
    def full_address(self):
        parts = [self.name]
        if self.area: parts.append(self.area.name)
        if self.city: parts.append(self.city.name)
        if self.state: parts.append(self.state.name)
        if self.country: parts.append(self.country.name)
        return ", ".join(parts)

    def __repr__(self):
        return f"<Locality {self.name}>"
