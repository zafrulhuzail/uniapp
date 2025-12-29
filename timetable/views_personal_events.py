from datetime import time
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from buildings.models import Building, Room
from .models import StudentPersonalEvent


def _get_student(request):
    return getattr(request.user, "student", None)


def _parse_time(s: str) -> time:
    h, m = s.split(":")
    return time(int(h), int(m))


def _get_fk_or_none(model_cls, raw_id: str):
    raw_id = (raw_id or "").strip()
    if not raw_id:
        return None
    return model_cls.objects.get(id=int(raw_id))


@login_required
@require_POST
def personal_event_create(request):
    student = _get_student(request)
    if not student:
        return JsonResponse({"error": "Not a student"}, status=403)

    title = (request.POST.get("title") or "").strip()
    weekday = int(request.POST.get("weekday") or 0)
    start_time = (request.POST.get("start_time") or "").strip()
    end_time = (request.POST.get("end_time") or "").strip()
    description = (request.POST.get("description") or "").strip()

    if not title:
        return JsonResponse({"error": "Title is required"}, status=400)
    if weekday < 1 or weekday > 7:
        return JsonResponse({"error": "Weekday must be 1..7"}, status=400)

    try:
        st = _parse_time(start_time)
        et = _parse_time(end_time)
    except Exception:
        return JsonResponse({"error": "Invalid time format (HH:MM)"}, status=400)

    if et <= st:
        return JsonResponse({"error": "End time must be after start time"}, status=400)

    try:
        building = _get_fk_or_none(Building, request.POST.get("building_id"))
    except Building.DoesNotExist:
        return JsonResponse({"error": "Building not found"}, status=400)

    try:
        room = _get_fk_or_none(Room, request.POST.get("room_id"))
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=400)

    ev = StudentPersonalEvent.objects.create(
        student=student,
        title=title,
        weekday=weekday,
        start_time=st,
        end_time=et,
        building=building,
        room=room,
        description=description,
    )

    return JsonResponse({"ok": True, "id": ev.id})


@login_required
@require_POST
def personal_event_update(request, event_id: int):
    student = _get_student(request)
    if not student:
        return JsonResponse({"error": "Not a student"}, status=403)

    try:
        ev = StudentPersonalEvent.objects.get(id=event_id, student=student)
    except StudentPersonalEvent.DoesNotExist:
        return JsonResponse({"error": "Event not found"}, status=404)

    title = (request.POST.get("title") or "").strip()
    weekday = int(request.POST.get("weekday") or 0)
    start_time = (request.POST.get("start_time") or "").strip()
    end_time = (request.POST.get("end_time") or "").strip()
    description = (request.POST.get("description") or "").strip()

    if not title:
        return JsonResponse({"error": "Title is required"}, status=400)
    if weekday < 1 or weekday > 7:
        return JsonResponse({"error": "Weekday must be 1..7"}, status=400)

    try:
        st = _parse_time(start_time)
        et = _parse_time(end_time)
    except Exception:
        return JsonResponse({"error": "Invalid time format (HH:MM)"}, status=400)

    if et <= st:
        return JsonResponse({"error": "End time must be after start time"}, status=400)

    try:
        building = _get_fk_or_none(Building, request.POST.get("building_id"))
    except Building.DoesNotExist:
        return JsonResponse({"error": "Building not found"}, status=400)

    try:
        room = _get_fk_or_none(Room, request.POST.get("room_id"))
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=400)

    ev.title = title
    ev.weekday = weekday
    ev.start_time = st
    ev.end_time = et
    ev.building = building
    ev.room = room
    ev.description = description
    ev.save()

    return JsonResponse({"ok": True})


@login_required
@require_POST
def personal_event_delete(request, event_id: int):
    student = _get_student(request)
    if not student:
        return JsonResponse({"error": "Not a student"}, status=403)

    try:
        ev = StudentPersonalEvent.objects.get(id=event_id, student=student)
    except StudentPersonalEvent.DoesNotExist:
        return JsonResponse({"error": "Event not found"}, status=404)

    ev.delete()
    return JsonResponse({"ok": True})
