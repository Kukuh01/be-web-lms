from django.shortcuts import get_object_or_404
from .models import Assignment
from apps.lessons.models import Lesson

class AssignmentService:

    def list_by_lesson(self, lesson_id: int):

        _ = get_object_or_404(Lesson, id=lesson_id)

        return Assignment.objects.filter(lesson_id=lesson_id)

    def create(self, lesson_id: int, data):
        return Assignment.objects.create(
            lesson_id=lesson_id,
            **data.dict()
        )

    def update(self, assignment_id: int, data):
        assignment = get_object_or_404(Assignment, id=assignment_id)
        for field, value in data.dict(exclude_unset=True).items():
            setattr(assignment, field, value)
        assignment.save()
        return assignment

    def delete(self, assignment_id: int):
        assignment = get_object_or_404(Assignment, id=assignment_id)
        assignment.delete()

        