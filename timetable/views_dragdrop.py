from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

from courses.models import Enrollment
from timetable.services import detect_conflict_for_section


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

# -------------------------
# Drag-drop show/hide for enrollments (SOFT WARNING + FORCE)
# -------------------------
@login_required
@require_POST
def show_enrollment(request, enrollment_id):
    student = getattr(request.user, "student", None)
    if not student:
        return JsonResponse({"error": "You are not a student."}, status=403)

    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=student)

    force = request.POST.get("force") == "1"

    msg = detect_conflict_for_section(
        student=student,
        section_id=enrollment.section_id,
        ignore_enrollment_id=enrollment.id,
    )

    # Soft warning (do not block)
    if msg and not force:
        return JsonResponse({"warning": msg, "can_force": True}, status=200)

    enrollment.show_on_timetable = True
    enrollment.save(update_fields=["show_on_timetable"])
    return JsonResponse({"ok": True}, status=200)

@login_required
@require_POST
def hide_enrollment(request, enrollment_id):
    student = getattr(request.user, "student", None)
    if not student:
        return JsonResponse({"error": "You are not a student."}, status=403)

    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=student)
    enrollment.show_on_timetable = False
    enrollment.save(update_fields=["show_on_timetable"])
    return JsonResponse({"ok": True}, status=200)
