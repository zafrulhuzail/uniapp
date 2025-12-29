from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from courses.models import Enrollment


def _get_student(request):
    if not hasattr(request.user, "student"):
        return None
    return request.user.student


@login_required
@require_POST
def show_enrollment(request, enrollment_id: int):
    student = _get_student(request)
    if student is None:
        return JsonResponse({"error": "Not a student"}, status=403)

    try:
        enr = Enrollment.objects.select_related("section").get(id=enrollment_id, student=student)
    except Enrollment.DoesNotExist:
        return JsonResponse({"error": "Enrollment not found"}, status=404)

    enr.show_on_timetable = True
    enr.save(update_fields=["show_on_timetable"])
    return JsonResponse({"ok": True})


@login_required
@require_POST
def hide_enrollment(request, enrollment_id: int):
    student = _get_student(request)
    if student is None:
        return JsonResponse({"error": "Not a student"}, status=403)

    try:
        enr = Enrollment.objects.select_related("section").get(id=enrollment_id, student=student)
    except Enrollment.DoesNotExist:
        return JsonResponse({"error": "Enrollment not found"}, status=404)

    enr.show_on_timetable = False
    enr.save(update_fields=["show_on_timetable"])
    return JsonResponse({"ok": True})
