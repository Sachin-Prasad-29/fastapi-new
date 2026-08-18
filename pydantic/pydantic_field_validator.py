from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class Car(BaseModel):
    name: str
    brand: str
    price: int = Field(
        gt=0,
        title="Enter the PRice of the Car",
        description="This is the Price of the Car",
    )
    milage: Annotated[int, Field(default=11, title="This is the milage of the Car")]
    ev: bool

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if value == "M4 Comp":
            return "BMW M4 Competition"
        else:
            return value


car1 = {
    "name": "M5 Compsdfdsfsdf",
    "brand": "BMWsd sddfdsf",
    "price": 120000,
    "milage": 14,
    "ev": False,
}


car1_data = Car(**car1)


print(car1_data)
