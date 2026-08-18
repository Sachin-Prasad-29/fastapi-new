from pydantic import BaseModel


class Address(BaseModel):
    city: str
    state: str
    zip: str


class Patient(BaseModel):
    name: str
    age: int
    gender: str
    address: Address


address_dict = {"city": "Korba", "state": "Chhattisgarh", "zip": "495677"}

address_one = Address(**address_dict)

patient_dict = {"name": "Sachin", "age": 25, "gender": "male", "address": address_one}

patient_one = Patient(**patient_dict)

print(patient_one)
