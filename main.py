from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from scheduler import generate_timetable
from validator import validate_input, validate_timetable



app = FastAPI(
    title="Clash-Free Timetable Generator",
    description="Generate and validate clash-free school timetables.",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# DATA MODELS
# =========================================================

class ClassData(BaseModel):
    id: str
    name: str


class TeacherData(BaseModel):
    id: str
    name: str


class RoomData(BaseModel):
    id: str
    name: str


class SubjectData(BaseModel):
    id: str
    name: str
    class_id: str
    teacher_id: str
    room_id: str
    periods_per_week: int


class TimetableRequest(BaseModel):
    classes: List[ClassData]
    teachers: List[TeacherData]
    rooms: List[RoomData]
    subjects: List[SubjectData]


# =========================================================
# BASIC ROUTES
# =========================================================

@app.get("/")
def root():

    return {
        "message": "Clash-Free Timetable Generator API is running!"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# =========================================================
# GENERATE TIMETABLE
# =========================================================

@app.post("/api/timetable/generate")
def generate(request: TimetableRequest):

    # -----------------------------------------------------
    # CONVERT REQUEST DATA
    # -----------------------------------------------------

    classes = [
        item.model_dump()
        for item in request.classes
    ]

    teachers = [
        item.model_dump()
        for item in request.teachers
    ]

    rooms = [
        item.model_dump()
        for item in request.rooms
    ]

    subjects = [
        item.model_dump()
        for item in request.subjects
    ]

    # -----------------------------------------------------
    # VALIDATE INPUT
    # -----------------------------------------------------

    input_errors = validate_input(
        classes=classes,
        subjects=subjects,
        teachers=teachers,
        rooms=rooms
    )

    if input_errors:

        return {
            "success": False,
            "stage": "input_validation",
            "message": "Invalid timetable data.",
            "errors": input_errors
        }

    # -----------------------------------------------------
    # GENERATE TIMETABLE
    # -----------------------------------------------------

    result = generate_timetable(
        classes=classes,
        subjects=subjects,
        teachers=teachers,
        rooms=rooms
    )

    # -----------------------------------------------------
    # CHECK SOLVER RESULT
    # -----------------------------------------------------

    if not result["success"]:

        return result

    timetable = result["timetable"]

    # -----------------------------------------------------
    # VALIDATE GENERATED TIMETABLE
    # -----------------------------------------------------

    timetable_errors = validate_timetable(
        timetable
    )

    if timetable_errors:

        return {
            "success": False,
            "stage": "timetable_validation",
            "message": "Generated timetable contains clashes.",
            "errors": timetable_errors,
            "timetable": timetable
        }

    # -----------------------------------------------------
    # SUCCESS
    # -----------------------------------------------------

    return {
        "success": True,
        "message": "Timetable generated and validated successfully.",
        "clashes": [],
        "timetable": timetable
    }