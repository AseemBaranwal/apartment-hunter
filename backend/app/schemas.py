import uuid
from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict


# ---------------------------
# Amenity
# ---------------------------

class AmenityBase(BaseModel):
    name: str
    category: Optional[str] = None
    description: Optional[str] = None


class AmenityOut(AmenityBase):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)


# ---------------------------
# Listing & Unit Types
# ---------------------------

class UnitTypeBase(BaseModel):
    name: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    sqft_min: Optional[int] = None
    sqft_max: Optional[int] = None
    availability: Optional[str] = None
    details_json: Optional[dict] = None


class UnitTypeOut(UnitTypeBase):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)


class PriceSnapshotBase(BaseModel):
    price: int
    currency: str


class PriceSnapshotOut(BaseModel):
    id: uuid.UUID
    price: int
    currency: str
    fetched_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ListingBase(BaseModel):
    source: Optional[str] = None
    source_listing_id: Optional[str] = None
    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = True


class ListingOut(BaseModel):
    id: uuid.UUID
    source: str | None = None
    url: str | None = None
    title: str | None = None
    active: bool | None = True
    created_at: datetime
    price_snapshots: list[PriceSnapshotOut] = []
    model_config = ConfigDict(from_attributes=True)


# ---------------------------
# Community
# ---------------------------

class CommunityBase(BaseModel):
    name: str
    street: Optional[str] = None
    city: Optional[str] = None
    zip: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    primary_source: str


class CommunityCreate(CommunityBase):
    listings: List[ListingBase] = []


class CommunityOut(BaseModel):
    id: uuid.UUID
    name: str
    street: str | None = None
    city: str | None = None
    zip: str | None = None
    lat: float | None = None
    lon: float | None = None
    primary_source: str
    created_at: datetime
    updated_at: datetime
    listings: list[ListingOut] = []
    model_config = ConfigDict(from_attributes=True)


# ---------------------------
# Locality Metrics & Ranking
# ---------------------------

class LocalityMetricOut(BaseModel):
    id: uuid.UUID
    walk_score: Optional[int] = None
    transit_score: Optional[int] = None
    bike_score: Optional[int] = None
    poi_counts_json: Optional[dict] = None
    schools_nearby: Optional[int] = None
    safety_score: Optional[float] = None
    crime_count_12mo: Optional[int] = None
    median_rent_by_h3: Optional[int] = None
    computed_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RankingOut(BaseModel):
    id: uuid.UUID
    price_score: float
    locality_score: float
    amenity_score: float
    composite_score: float
    computed_at: datetime

    model_config = ConfigDict(from_attributes=True)
