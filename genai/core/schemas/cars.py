from typing import List, Optional
from pydantic import BaseModel, Field


class Car(BaseModel):
    car_id: str = Field(..., description="Unique identifier for the car")
    brand: str = Field(..., description="Car manufacturer brand")
    model: str = Field(..., description="Car model name")
    year: int = Field(..., description="Manufacturing year of the car")
    trim: Optional[str] = Field(None, description="Trim level of the car")
    body_type: Optional[str] = Field(
        None, description="Type of car body, e.g., Sedan, SUV"
    )
    engine_type: Optional[str] = Field(
        None, description="Engine type, e.g., V6, Electric, Hybrid"
    )
    engine_size_liters: Optional[float] = Field(
        None, description="Engine size in liters"
    )
    horsepower: Optional[int] = Field(None, description="Horsepower rating of the car")
    transmission: Optional[str] = Field(
        None, description="Transmission type, e.g., Automatic, Manual"
    )
    fuel_type: Optional[str] = Field(
        None, description="Fuel type, e.g., Gasoline, Diesel, Electric"
    )
    mileage_km: Optional[int] = Field(None, description="Mileage in kilometers")
    top_speed_kmh: Optional[int] = Field(
        None, description="Top speed in kilometers per hour"
    )
    color: Optional[str] = Field(None, description="Color of the car")
    features: Optional[str] = Field(None, description="List of car features")
    price_usd: Optional[float] = Field(None, description="Price of the car in USD")
    discount_percent: Optional[float] = Field(
        None, description="Discount percentage, if applicable"
    )
    num_in_stock: Optional[int] = Field(
        None, description="Number of units available in stock"
    )
    semantic_desc: Optional[str] = Field(
        None, description="Semantic description of the car for embedding or NLP"
    )


class ManyCars(BaseModel):
    cars: List[Car] = Field(
        ..., description="Most relevant cars for the user's question."
    )
