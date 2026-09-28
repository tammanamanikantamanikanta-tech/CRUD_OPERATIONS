from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

students = []


class Student(BaseModel):
    id:int
    name: str
    email: EmailStr
    course: str
    age: int


# Create student
@app.post("/students")
def create_student(student: Student):
    for existing_student in students:

        if existing_student["email"]==student.email:
            raise HTTPException(
                status_code=404,
                detail="student already exists"
            )
    student_data = {
        "id": len(students) + 1,
        "name": student.name,
        "email": student.email,
        "course": student.course,
        "age": student.age
    }

    students.append(student_data)

    return student_data


# Get all students
@app.get("/students")
def get_students():
    return students


# Get student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int):

    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# Update student
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):

    for s in students:
        if s["id"] == student_id:

            s["name"] = student.name
            s["email"] = student.email
            s["course"] = student.course
            s["age"] = student.age

            return s

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# Delete student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for student in students:
        if student["id"] == student_id:

            students.remove(student)

            return {
                "message": "Student deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# Search by course
@app.get("/students/search")
def search_students(course: str):

    result = []

    for student in students:
        if course.lower() in student["course"].lower():
            result.append(student)

    return result