from typing import Optional, List
from ninja import Schema
from apps.lessons.api import LessonOut

class InstructorOut(Schema):
    id: int
    name: str

class CourseStatsOut(Schema):
    total_courses: int

class CourseIn(Schema):
    id: int
    title: str
    description: Optional[str]
    linkMeet: Optional[str] = None
    linkWa: Optional[str] = None
    instructor: InstructorOut
    thumbnail: Optional[str] = None

class CourseOut(Schema):
    id: int
    title: str
    description: Optional[str]
    linkMeet: Optional[str] = None
    linkWa: Optional[str] = None
    instructor: InstructorOut
    thumbnail: Optional[str] = None
    lessons: List[LessonOut] = []

class CourseDetail(CourseOut):
    lessons: List[LessonOut]
