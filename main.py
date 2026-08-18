import json

from fastapi import FastAPI, HTTPException, Path, Query

app = FastAPI()


def load_patients():
    with open("patients.json") as f:
        data = json.load(f)
    return data


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
