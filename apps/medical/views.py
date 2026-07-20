

# Create your views here.

def reassessments(request):
    """
    SC034 - Reassessments (Đánh giá lại hồ sơ bệnh án)
    Dummy data based on Figma mockup
    """
    reassessments_list = [
        {
            'resident': 'Robert Hayes',
            'room': '204B',
            'trigger': '90-day cycle',
            'due_date': '2026-06-28',
            'overdue': '4 days',
            'status': 'Review Due',
            'action': 'Start',
            'is_escalated': True,
        },
        {
            'resident': 'James Porter',
            'room': '210B',
            'trigger': '90-day cycle',
            'due_date': '2026-07-03',
            'overdue': '2 days',
            'status': 'Review Due',
            'action': 'Start',
            'is_escalated': False,
        },
        {
            'resident': 'Susan Wright',
            'room': '114B',
            'trigger': 'Significant Change (SCS)',
            'due_date': '—',
            'overdue': '—',
            'status': 'Needs Update',
            'action': 'Start',
            'is_escalated': False,
        },
        {
            'resident': 'Mary Coleman',
            'room': '118A',
            'trigger': '90-day cycle',
            'due_date': '2026-07-20',
            'overdue': '—',
            'status': 'Active',
            'action': 'View',
            'is_escalated': False,
        },
    ]

    context = {
        'active_menu': 'care_planning',
        'reassessments_list': reassessments_list,
        'total_reassessments': 3,
        'total_overdue': 1,
    }
    return render(request, 'medical/reassessments.html', context)

from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

@require_POST
def start_reassessment(request):
    try:
        data = json.loads(request.body)
        # Mocking DB operation
        return JsonResponse({
            'status': 'success',
            'message': 'Reassessment started'
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from .models import Assessment, LOCClassification, LOCClassificationHistory
from apps.billing.models import LOCRate
from django.utils import timezone

def loc_classification_detail(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    loc, created = LOCClassification.objects.get_or_create(
        assessment=assessment,
        defaults={
            'calculated_score': assessment.total_adl_score,
            'suggested_loc': _calculate_loc(assessment.total_adl_score)
        }
    )
    
    loc_rate = None
    display_loc = loc.final_loc if loc.final_loc else loc.suggested_loc
    try:
        loc_rate = LOCRate.objects.get(loc_level=display_loc)
    except LOCRate.DoesNotExist:
        pass
        
    history = loc.history.all().order_by('-action_at')
    
    context = {
        'assessment': assessment,
        'loc': loc,
        'loc_rate': loc_rate,
        'history': history,
    }
    return render(request, 'medical/loc_classification.html', context)

def _calculate_loc(score):
    if score <= 8:
        return 'Level 1'
    elif score <= 16:
        return 'Level 2'
    elif score <= 24:
        return 'Level 3'
    else:
        return 'Level 4'

def loc_classification_confirm(request, assessment_id):
    if request.method == 'POST':
        assessment = get_object_or_404(Assessment, id=assessment_id)
        loc = get_object_or_404(LOCClassification, assessment=assessment)
        
        if loc.status == 'Confirmed':
            return HttpResponseBadRequest("Already confirmed")
            
        loc.final_loc = loc.suggested_loc
        loc.status = 'Confirmed'
        loc.confirmed_by = request.user if request.user.is_authenticated else None
        loc.confirmed_at = timezone.now()
        loc.save()
        
        LOCClassificationHistory.objects.create(
            loc_classification=loc,
            action="LOC Confirmed",
            action_by=request.user if request.user.is_authenticated else None,
            details=f"Confirmed {loc.final_loc}"
        )
        return redirect('medical:loc_detail', assessment_id=assessment.id)
    return HttpResponseBadRequest("Invalid request")

def loc_classification_override(request, assessment_id):
    if request.method == 'POST':
        assessment = get_object_or_404(Assessment, id=assessment_id)
        loc = get_object_or_404(LOCClassification, assessment=assessment)
        
        if loc.status == 'Confirmed':
            return HttpResponseBadRequest("Already confirmed")
            
        override_loc = request.POST.get('override_loc')
        override_reason = request.POST.get('override_reason')
        
        if not override_loc or not override_reason:
            return HttpResponseBadRequest("Missing fields")
            
        loc.final_loc = override_loc
        loc.status = 'Confirmed'
        loc.is_overridden = True
        loc.override_reason = override_reason
        loc.confirmed_by = request.user if request.user.is_authenticated else None
        loc.confirmed_at = timezone.now()
        loc.save()
        
        LOCClassificationHistory.objects.create(
            loc_classification=loc,
            action="LOC Overridden",
            action_by=request.user if request.user.is_authenticated else None,
            details=f"Overridden to {loc.final_loc}. Reason: {override_reason}"
        )
        return redirect('medical:loc_detail', assessment_id=assessment.id)
    return HttpResponseBadRequest("Invalid request")

from django.shortcuts import render, get_object_or_404

from apps.residents.models import Resident

def loc_history_view(request, resident_id):
    resident = get_object_or_404(Resident, id=resident_id)
    return render(request, "medical/loc_history.html", {"resident": resident})

from django.views import View
from .models import PreAdmissionScreening
from apps.residents.models import Resident

class ScreeningCreate(View):
    def get(self, request, resident_id):
        resident = get_object_or_404(Resident, pk=resident_id)
        return render(request, 'medical/screening_form.html', {'resident': resident})

class AdmissionFormView(View):
    def get(self, request, resident_id):
        from apps.rooms.models import Bed
        resident = get_object_or_404(Resident, pk=resident_id)
        beds = Bed.objects.filter(status='AVAILABLE')
        return render(request, 'medical/admission_form.html', {'resident': resident, 'beds': beds})



from datetime import date, datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
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
        # Sử dụng DRAFT hoặc ACTIVE để khớp 100% với STATUS_CHOICES trong models.py
        status = "DRAFT" if action == "save_draft" else "ACTIVE"

        # 1. Tạo Care Plan trong DB SQL Server
        care_plan = CarePlan.objects.create(
            resident_id=resident_id,
            status=status,
            significant_change_flag=False
        )

        # 2. Tạo Care Goal đi kèm
        goal_text = request.POST.get("goal")
        if goal_text:
            CareGoal.objects.create(
                care_plan=care_plan,
                goal=goal_text,
                measure=request.POST.get("measure", ""),
                task=request.POST.get("task", ""),
                status="IN_PROGRESS"
                status="IN_PROGRESS"  # Khớp với STATUS_CHOICES trong CareGoal model
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
    # Query kiểm tra trùng ngày lễ từ SQL Server
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
# Care Plan API (DRF Views)
# ==========================

class CarePlanListCreateView(generics.ListCreateAPIView):
    queryset = CarePlan.objects.filter(is_deleted=False)
    serializer_class = CarePlanSerializer


class CarePlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarePlan.objects.all()
    serializer_class = CarePlanSerializer


# ==========================
# Care Goal API (DRF Views)
# ==========================

class CareGoalListCreateView(generics.ListCreateAPIView):
    queryset = CareGoal.objects.all()
    serializer_class = CareGoalSerializer


class CareGoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CareGoal.objects.all()
    serializer_class = CareGoalSerializer



# ==========================
# SC029 UI Page View (Care Plan Detail with Holiday Notice)
# ==========================

def care_plan_detail_page(request):
    # Ngày review tiếp theo của kế hoạch
    next_review_due = date(2026, 7, 4)  # Mẫu ngày 04/07/2026 (Federal Holiday)

    # Truy vấn tên ngày lễ từ SQL Server DB
    next_review_due = date(2026, 7, 4)

    holiday_info = Holiday.objects.filter(holiday_date=next_review_due).first()
    
    holiday_notice = None
    if holiday_info:
        # Định dạng chuỗi thông báo: "Scheduled on: July 4 - Federal Holiday"
        formatted_date = next_review_due.strftime("%B %d").replace(" 0", " ")
        holiday_notice = f"Scheduled on: {formatted_date} - {holiday_info.holiday_name}"

    context = {
        "resident_name": "Robert Hayes",
        "room": "Room 204B",
        "loc_tier": "LOC Tier 3",
        "next_review": next_review_due.strftime("%Y-%m-%d"),
        "last_reviewed": "2026-04-08",
        "cycle_days": "90 days",
        "loc_rate": 248.00,
        "room_rate": 185.00,
        "estimated_daily": 433.00,
        "estimated_monthly": 13163.00,
        "holiday_notice": holiday_notice,  # Biến truyền ra giao diện
        "holiday_notice": holiday_notice,
    }

    return render(
        request,
        "medical/care_plan_detail.html",
        context
    )
    )


# ==========================
# SC030 UI Page View (Review Care Plan)
# ==========================

def care_plan_review_page(request, pk=None):
    care_plan = CarePlan.objects.filter(pk=pk).first() if pk else None

    # Dynamic check trùng ngày lễ cho banner warning
    holiday_warning = None
    holiday_check = Holiday.objects.filter(holiday_date=date(2026, 7, 30)).first()
    if holiday_check:
        holiday_warning = f"The plan includes a date that coincides with a public holiday ({holiday_check.holiday_name})."
    else:
        holiday_warning = "The plan includes a date that coincides with a public holiday (July 30th)."

    context = {
        "care_plan": care_plan,
        "resident_name": care_plan.resident.full_name if care_plan and hasattr(care_plan, 'resident') else "Robert Hayes",
        "room": getattr(care_plan, 'room', "Room 204B"),
        "loc_tier": getattr(care_plan, 'loc_tier', "LOC Tier 3"),
        "submitted_by": getattr(care_plan, 'submitted_by', "Anna Lee, RN"),
        "submitted_date": care_plan.created_at.strftime("%Y-%m-%d") if care_plan and hasattr(care_plan, 'created_at') else "2026-07-02",
        "status": getattr(care_plan, 'status', "Pending Review"),
        
        # Author info
        "author_name": "Anna Lee, RN",
        "license_no": "RN-482913 (CA)",
        "prepared_date": "2026-07-02 16:40",
        
        # IDT Acknowledgment
        "physician_name": "Dr. Alan Cho, MD",
        "physician_signed_at": "2026-07-02 14:10",
        "dietary_name": "Grace Liu, RD",
        "dietary_signed_at": "2026-07-02 15:30",

        # Holiday warning
        "holiday_warning": holiday_warning,
    }
    return render(request, "medical/care_plan_review.html", context)


# ==========================
# SC030 / SC031 API: Approve & e-Sign (With Password Check)
# ==========================

@csrf_exempt
@require_POST
def approve_care_plan(request, pk=None):
    try:
        password = request.POST.get("password", "").strip()

        # Xác thực mật khẩu chữ ký điện tử nếu user đã đăng nhập
        if request.user.is_authenticated and password:
            if not request.user.check_password(password):
                return JsonResponse({
                    "status": "error",
                    "message": "Invalid re-authentication password. Please try again."
                }, status=400)

        # Xử lý cập nhật DB
        if pk:
            care_plan = CarePlan.objects.filter(pk=pk).first()
            if care_plan:
                if hasattr(care_plan, 'status'):
                    care_plan.status = "ACTIVE"
                if hasattr(care_plan, 'approved_at'):
                    care_plan.approved_at = timezone.now()
                if hasattr(care_plan, 'approved_by'):
                    care_plan.approved_by = request.user if request.user.is_authenticated else None
                care_plan.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Care Plan approved and e-signed successfully!"
                })

        return JsonResponse({
            "status": "success",
            "message": "Care Plan approved and e-signed (Simulated)!"
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"Server Error: {str(e)}"}, status=500)


# ==========================
# SC030 API: Reject & Return
# ==========================

@csrf_exempt
@require_POST
def reject_care_plan(request, pk=None):
    try:
        reason = request.POST.get("rejection_reason", "").strip()

        if not reason:
            return JsonResponse(
                {"status": "error", "message": "Rejection reason is required when returning a plan to Draft."},
                status=400
            )

        if pk:
            care_plan = CarePlan.objects.filter(pk=pk).first()
            if care_plan:
                if hasattr(care_plan, 'status'):
                    care_plan.status = "DRAFT"
                if hasattr(care_plan, 'rejection_reason'):
                    care_plan.rejection_reason = reason
                care_plan.save()
                return JsonResponse({"status": "success", "message": "Care Plan rejected and returned to Draft!"})

        return JsonResponse({"status": "success", "message": "Care Plan rejected and returned as Draft (Simulated)!"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"Server Error: {str(e)}"}, status=500)


# ==========================
# Care Level API (DRF Views)
# ==========================

class CareLevelListCreateView(generics.ListCreateAPIView):
    queryset = CareLevel.objects.filter(is_deleted=False)
    serializer_class = CareLevelSerializer


class CareLevelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CareLevel.objects.all()
    serializer_class = CareLevelSerializer


# ==========================
# Care Plan API (DRF Views)
# ==========================

class CarePlanListCreateView(generics.ListCreateAPIView):
    queryset = CarePlan.objects.filter(is_deleted=False)
    serializer_class = CarePlanSerializer


class CarePlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarePlan.objects.all()
    serializer_class = CarePlanSerializer


# ==========================
# Care Goal API (DRF Views)
# ==========================

class CareGoalListCreateView(generics.ListCreateAPIView):
    queryset = CareGoal.objects.all()
    serializer_class = CareGoalSerializer



class CareGoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CareGoal.objects.all()
    serializer_class = CareGoalSerializer
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



# ==========================
# SC029 UI Page View (Care Plan Detail with Holiday Notice)
# ==========================

def care_plan_detail_page(request):
    # Ngày review tiếp theo của kế hoạch
    next_review_due = date(2026, 7, 4)  # Mẫu ngày 04/07/2026 (Federal Holiday)

    # Truy vấn tên ngày lễ từ SQL Server DB
    holiday_info = Holiday.objects.filter(holiday_date=next_review_due).first()
    
    holiday_notice = None
    if holiday_info:
        # Định dạng chuỗi thông báo: "Scheduled on: July 4 - Federal Holiday"
        formatted_date = next_review_due.strftime("%B %d").replace(" 0", " ")
        holiday_notice = f"Scheduled on: {formatted_date} - {holiday_info.holiday_name}"

    context = {
        "resident_name": "Robert Hayes",
        "room": "Room 204B",
        "loc_tier": "LOC Tier 3",
        "next_review": next_review_due.strftime("%Y-%m-%d"),
        "last_reviewed": "2026-04-08",
        "cycle_days": "90 days",
        "loc_rate": 248.00,
        "room_rate": 185.00,
        "estimated_daily": 433.00,
        "estimated_monthly": 13163.00,
        "holiday_notice": holiday_notice,  # Biến truyền ra giao diện
    }

    return render(
        request,
        "medical/care_plan_detail.html",
        context
    )