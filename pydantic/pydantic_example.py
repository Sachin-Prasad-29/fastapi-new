from typing import Annotated

from pydantic import AnyUrl, BaseModel, EmailStr, Field


class Patient(BaseModel):
    name: Annotated[
        str,
        Field(
            max_length=50,
            title="Name of the patient",
            description="Give the name of the patient in less than 50 Chars",
            examples=["Sachin", "Sameer"],
        ),
    ]
    email: EmailStr
    insta: AnyUrl
    age: int = Field(gt=0, lt=120)
    weight: float = Field(gt=0)
    married: bool
    allergies: list[str] | None = Field(max_length=5)
    contact_details: dict[str, str]


def insert_patient_data(patient: Patient):
    print(patient)
    print("Done")


patient_info = {
    "name": "John",
    "email": "sachinq11@gmail.com",
    "insta": "http://instagram.com/sachin",
    "age": 30,
    "weight": 70.1,
    "married": True,
    "allergies": ["penicillin", "latex"],
    "contact_details": {"email": "jo hn@example.com", "phone": "123-456-7890"},
}

patient_one = Patient(**patient_info)
insert_patient_data(patient_one)
