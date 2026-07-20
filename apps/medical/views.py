from datetime import date, datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import generics

from apps.medical.models import (
    CareLevel,
    CarePlan,
    CareGoal,
    Holiday
)

from apps.medical.api.serializers import (
    CareLevelSerializer,
    CarePlanSerializer,
    CareGoalSerializer
)


# ==========================
# SC027 UI Page View (Create Care Plan + Holiday Check)
# ==========================

def care_plan_create_page(request):

    # =====================
    # SUBMIT FORM (POST)
    # =====================
    if request.method == "POST":
        resident_id = request.POST.get("resident_id", 1)
        action = request.POST.get("action", "save_draft")

        status = "DRAFT" if action == "save_draft" else "PENDING_REVIEW"

        # 1. Tạo Care Plan
        care_plan = CarePlan.objects.create(
            resident_id=resident_id,
            status=status,
            significant_change_flag=False
        )

        # 2. Tạo Care Goal
        goal_text = request.POST.get("goal")
        if goal_text:
            CareGoal.objects.create(
                care_plan=care_plan,
                goal=goal_text,
                measure=request.POST.get("measure", ""),
                task=request.POST.get("task", ""),
                status="IN_PROGRESS"
            )

        messages.success(request, f"Care Plan created successfully with status: {status}")
        return redirect("care_plan_create")

    # =====================
    # DISPLAY PAGE (GET) & HOLIDAY CHECK LOGIC
    # =====================
    review_date_input = request.GET.get("review_date", "2026-09-02")
    try:
        target_date = datetime.strptime(review_date_input, "%Y-%m-%d").date()
    except ValueError:
        target_date = date(2026, 9, 2)

    # Đã map db_column='HolidayDate' chuẩn trong model -> Query trực tiếp cực ngắn gọn
    is_holiday_conflict = Holiday.objects.filter(holiday_date=target_date).exists()

    care_areas = [
        {
            "name": "Mobility",
            "suggested": True,
            "goal": "Resident will ambulate 50 ft with walker x2/day by 2026-07-30.",
            "measure": "Distance log",
            "target": "2026-07-30",
            "task": "Assist ambulation with front-wheel walker, twice daily."
        },
        {
            "name": "Skin Integrity",
            "suggested": True,
            "goal": "Maintain skin integrity.",
            "measure": "Braden score",
            "target": "2026-10-07",
            "task": "Reposition every 2 hours."
        },
        {
            "name": "Nutrition",
            "suggested": False,
            "goal": "Maintain hydration ≥1500 ml/day.",
            "measure": "I/O log",
            "target": "Ongoing",
            "task": "Monitor daily fluid intake."
        }
    ]

    context = {
        "resident_id": 1,
        "resident_name": "Robert Hayes",
        "room": "204B",
        "loc_tier": "LOC Tier 3",
        "loc_rate": 248.00,
        "room_rate": 185.00,
        "estimated_daily": 433.00,
        "estimated_monthly": 13163.00,
        "is_holiday_conflict": is_holiday_conflict,
        "care_areas": care_areas
    }

    return render(
        request,
        "medical/care_plan_create.html",
        context
    )


# ==========================
# SC028 UI Page View (Care Plan Locked Page)
# ==========================

def care_plan_locked_page(request):
    target_date = date(2026, 9, 2)
    
    # Query trực tiếp sạch đẹp
    is_holiday_conflict = Holiday.objects.filter(holiday_date=target_date).exists()

    context = {
        "resident_name": "Elena Ramos",
        "room": "Room 106A",
        "loc_tier": "LOC: Suggested (Tier 1)",
        "is_holiday_conflict": is_holiday_conflict,
    }

    return render(
        request,
        "medical/care_plan_locked.html",
        context
    )


# ==========================
# Care Level API
# ==========================

class CareLevelListCreateView(generics.ListCreateAPIView):
    queryset = CareLevel.objects.filter(is_deleted=False)
    serializer_class = CareLevelSerializer


class CareLevelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CareLevel.objects.all()
    serializer_class = CareLevelSerializer


# ==========================
# Care Plan API
# ==========================

class CarePlanListCreateView(generics.ListCreateAPIView):
    queryset = CarePlan.objects.filter(is_deleted=False)
    serializer_class = CarePlanSerializer


class CarePlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarePlan.objects.all()
    serializer_class = CarePlanSerializer


# ==========================
# Care Goal API
# ==========================

class CareGoalListCreateView(generics.ListCreateAPIView):
    queryset = CareGoal.objects.all()
    serializer_class = CareGoalSerializer


class CareGoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CareGoal.objects.all()
    serializer_class = CareGoalSerializer