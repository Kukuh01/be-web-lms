from ninja import NinjaAPI
from apps.accounts.api import router as accounts_router
from apps.courses.api import router as courses_router
from apps.lessons.api import router as lessons_router
from apps.assignments.api import router as assignments_router
from apps.submissions.api import router as submissions_router

api = NinjaAPI(title="LMS API")

api.add_router("/accounts/", accounts_router)
api.add_router("/courses/", courses_router)
api.add_router("/lessons/", lessons_router)
api.add_router("/assignments/", assignments_router)
api.add_router("/submissions/", submissions_router)