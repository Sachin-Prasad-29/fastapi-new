from typing import Optional
import json  
from typing import Annotated, Literal
from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field

app = FastAPI()
class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Id of the Patient", examples=["P001"])]
    name: Annotated[
        str, Field(..., description="Name of the Patient", examples=["John Doe"])
    ]
    city: Annotated[
        str, Field(..., description="City of the Patient", examples=["Mumbai"])
    ]
    age: Annotated[
        int, Field(..., gt=0, lt=120, description="Age of the Patient", examples=[25])
    ]
    gender: Annotated[
        Literal["Male", "Female", "Other"],
        Field(
            ...,
            description="Gender of the Patient",
            examples=["Male"],
        ),
    ]
    height: Annotated[
        float,
        Field(..., gt=0, description="Height of the Patient in Meters", examples=[5.9]),
    ]
    weight: Annotated[
        float,
        Field(
            ..., gt=0, description="Weight of the Patient in Kilograms", examples=[70.0]
        ),
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height * self.height), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obesity"


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str],Field(default=None)]
    city: Annotated[Optional[str],Field(default=None)]
    age: Annotated[Optional[int],Field(default=None,gt=0,lt=120)]
    gender: Annotated[Optional[Literal["Male","Female","Other"]],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None,gt=0)]
    weight:Annotated[Optional[float],Field(default=None,gt=0)]


def load_patients():
    with open("patients.json") as f:
        data = json.load(f)
    return data


def save_data(patients):
    with open("patients.json", "w") as f:
        json.dump(patients, f, indent=4)


@app.get("/")
def hello():
    return {"message": "Patient Management System"}


@app.get("/about")
def about():
    return {"message": "a fully functional patient management system"}


# view all patients
@app.get("/view")
def view():
    patients = load_patients()
    return {"patients": patients}


# view a single patient
@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ..., description="The ID of the patient to view", example="P001"
    ),
):
    # load all patients from the json file
    patients = load_patients()

    if patient_id in patients:
        return patients[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/sort")
def sort_patients(
    sort_by: str = Query(
        ...,
        description="The field to sort by",
        example="height",
        enum=["height", "weight", "bmi"],
    ),
    order: str = Query("asc", description="The order to sort by", enum=["asc", "desc"]),
):

    data = load_patients()
    sort_order = True if order == "desc" else False
    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=sort_order)
    return {"sorted_data": sorted_data}


@app.post("/create")
def create_patient(patient: Patient):
    # load the data
    patients = load_patients()

    #  check if Patient already exists
    if patient.id in patients:
        raise HTTPException(status_code=400, detail="Patient Already Exist")

    #  New Patient add to the Database
    patients[patient.id] = patient.model_dump(exclude={"id"})

    # save the json data
    save_data(patients)

    return JSONResponse(
        status_code=201, content={"message": "Patient created successfully"}
    )

@app.put("/edit/{patient_id}")
def update_patient(patient_id:str,patient_update:PatientUpdate):
    data = load_patients()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient Not Found")
    
    existing_patient_data = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    print(updated_patient_info)

    for key, value in updated_patient_info.items():
        existing_patient_data[key] = value
   
    existing_patient_data['id'] = patient_id
    print('existing_patient_data 1',existing_patient_data)
    patient_pydantic_obj = Patient(**existing_patient_data)
    print('patient_dydantic_object',patient_pydantic_obj)
    existing_patient_data =  patient_pydantic_obj.model_dump(exclude={'id'})
    print('existing_patient_data',existing_patient_data)
    data[patient_id] = existing_patient_data
    save_data(data)

    return JSONResponse(
        status_code=200, content={"message": "Patient updated successfully"}
    )


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):
    data = load_patients()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient Not Found")
    
    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200,content={'message':"Patient Deleted Successfully"})