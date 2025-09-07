import uuid
import datetime
from sqlalchemy import (
    Column, String, Float, Boolean, ForeignKey, Integer, DateTime, Text, Enum, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from .database import Base

# ---------------------------
# Core Entities
# ---------------------------


class Community(Base):
    __tablename__ = "community"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    normalized_address = Column(Text, index=True)
    street = Column(Text)
    city = Column(Text)
    zip = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    geom = Column(Geometry("POINT", srid=4326))
    primary_source = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow)

    listings = relationship("Listing", back_populates="community")
    locality_metrics = relationship(
        "LocalityMetric", back_populates="community")
    rankings = relationship("Ranking", back_populates="community")


class Listing(Base):
    __tablename__ = "listing"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    community_id = Column(UUID(as_uuid=True), ForeignKey("community.id"))
    source = Column(Text)  # zillow, avalon, etc.
    source_listing_id = Column(Text)  # unique per source
    url = Column(Text)
    title = Column(Text)
    description = Column(Text)
    last_scraped = Column(DateTime)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    community = relationship("Community", back_populates="listings")
    price_snapshots = relationship("PriceSnapshot", back_populates="listing")
    listing_amenities = relationship(
        "ListingAmenity", back_populates="listing")
    source_snapshots = relationship("SourceSnapshot", back_populates="listing")


class UnitType(Base):
    __tablename__ = "unit_type"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listing.id"))
    name = Column(Text)  # e.g. "1BR/1BA"
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    sqft_min = Column(Integer)
    sqft_max = Column(Integer)
    availability = Column(Text)
    details_json = Column(JSON)

    listing = relationship("Listing")


class PriceSnapshot(Base):
    __tablename__ = "price_snapshot"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listing.id"))
    unit_type_id = Column(UUID(as_uuid=True), ForeignKey("unit_type.id"))
    price = Column(Integer)
    currency = Column(Text)
    fetched_at = Column(DateTime, default=datetime.datetime.utcnow)

    listing = relationship("Listing", back_populates="price_snapshots")
    unit_type = relationship("UnitType")


class Amenity(Base):
    __tablename__ = "amenity"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    category = Column(Text)  # community/unit/shared
    description = Column(Text)

    listing_amenities = relationship(
        "ListingAmenity", back_populates="amenity")


class ListingAmenity(Base):
    __tablename__ = "listing_amenity"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listing.id"))
    amenity_id = Column(UUID(as_uuid=True), ForeignKey("amenity.id"))
    source_reported = Column(Boolean, default=True)
    confidence = Column(Float)

    listing = relationship("Listing", back_populates="listing_amenities")
    amenity = relationship("Amenity", back_populates="listing_amenities")

# ---------------------------
# Locality, Ranking, Caches
# ---------------------------


class LocalityMetric(Base):
    __tablename__ = "locality_metric"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    community_id = Column(UUID(as_uuid=True), ForeignKey("community.id"))
    walk_score = Column(Integer)
    transit_score = Column(Integer)
    bike_score = Column(Integer)
    poi_counts_json = Column(JSON)
    schools_nearby = Column(Integer)
    h3_cell = Column(Text)
    safety_score = Column(Float)
    crime_count_12mo = Column(Integer)
    median_rent_by_h3 = Column(Integer)
    computed_at = Column(DateTime, default=datetime.datetime.utcnow)

    community = relationship("Community", back_populates="locality_metrics")


class Ranking(Base):
    __tablename__ = "ranking"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    community_id = Column(UUID(as_uuid=True), ForeignKey("community.id"))
    price_score = Column(Float)
    locality_score = Column(Float)
    amenity_score = Column(Float)
    composite_score = Column(Float)
    rank_run_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    computed_at = Column(DateTime, default=datetime.datetime.utcnow)

    community = relationship("Community", back_populates="rankings")


class SourceSnapshot(Base):
    __tablename__ = "source_snapshot"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listing.id"))
    url = Column(Text)
    raw_html = Column(Text)
    raw_json = Column(JSON)
    last_scraped = Column(DateTime)

    listing = relationship("Listing", back_populates="source_snapshots")


class RouteCache(Base):
    __tablename__ = "route_cache"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    origin_community_id = Column(
        UUID(as_uuid=True), ForeignKey("community.id"))
    destination_label = Column(Text)
    mode = Column(Text)  # driving, walking, transit
    duration_seconds = Column(Integer)
    distance_meters = Column(Integer)
    matrix_element_hash = Column(Text)
    fetched_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime)


class PlaceCache(Base):
    __tablename__ = "place_cache"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    community_id = Column(UUID(as_uuid=True), ForeignKey("community.id"))
    google_place_id = Column(Text)
    details_json = Column(JSON)
    photos_meta = Column(JSON)
    rating = Column(Float)
    phone = Column(Text)
    website = Column(Text)
    fetched_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime)


class CacheTable(Base):
    __tablename__ = "cache_table"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    api_name = Column(Text, nullable=False)
    cache_key = Column(Text, nullable=False, unique=True)
    response_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime)
