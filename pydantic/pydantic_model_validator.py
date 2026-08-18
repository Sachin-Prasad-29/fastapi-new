from pydantic import BaseModel, computed_field, model_validator


class Car(BaseModel):
    name: str
    brand: str
    price: int
    milage: float
    ev: bool

    @model_validator(mode="after")
    def validate_car_performance(cls, model):
        if model.milage < 30 and not model.ev:
            raise ValueError("Car is too expensive")
        return model

    @computed_field
    @property
    def car_type(self) -> str:
        if self.milage < 20 and not self.ev:
            return "Super Car"
        else:
            return "Normal car"


car1 = {
    "name": "M5 Comp",
    "brand": "BMW",
    "price": 120000,
    "milage": 14.3,
    "ev": False,
}


car1_data = Car(**car1)


print(car1_data)
