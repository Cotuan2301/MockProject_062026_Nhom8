
"""
apps/medical/views.py
SC-022 Initial Assessment - Views
"""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.residents.models import Resident
from .models import Assessment, AssessmentDetail, AssessmentDiagnosis
from .fomrs import (
    AssessmentForm,
    ADL_ITEMS,
    IADL_ITEMS,
    VITAL_SIGN_ITEMS,
    ADL_SCORE_CHOICES,
    IADL_SCORE_CHOICES,
)


# @login_required
def initial_assessment(request, pk, assessment_id=None):
    """
    SC-022: pk = Resident.id (Django auto id)
    """
    resident = get_object_or_404(Resident, pk=pk)

    assessment = None
    existing_details = {}
    existing_diagnoses = []

    if assessment_id:
        assessment = get_object_or_404(Assessment, id=assessment_id, resident=resident)
        for d in assessment.details.all():
            existing_details[(d.category, d.item_key)] = d
        existing_diagnoses = list(assessment.diagnoses.all())

    if request.method == 'POST':
        form = AssessmentForm(request.POST, instance=assessment)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.resident = resident
            obj.assessed_by = request.user
            if not obj.assessment_date:
                obj.assessment_date = timezone.now()
            obj.save()

            for item_key, item_name in ADL_ITEMS:
                score = int(request.POST.get(f'adl_{item_key}', 0))
                AssessmentDetail.objects.update_or_create(
                    assessment=obj, category='adl', item_key=item_key,
                    defaults={'item_name': item_name, 'score': score, 'max_score': 4},
                )
            obj.details.filter(category='adl').exclude(
                item_key__in=[k for k, _ in ADL_ITEMS]
            ).delete()

            for item_key, item_name in IADL_ITEMS:
                score = int(request.POST.get(f'iadl_{item_key}', 0))
                AssessmentDetail.objects.update_or_create(
                    assessment=obj, category='iadl', item_key=item_key,
                    defaults={'item_name': item_name, 'score': score, 'max_score': 1},
                )
            obj.details.filter(category='iadl').exclude(
                item_key__in=[k for k, _ in IADL_ITEMS]
            ).delete()

            for item_key, item_name, unit in VITAL_SIGN_ITEMS:
                value = request.POST.get(f'vs_{item_key}', '').strip()
                AssessmentDetail.objects.update_or_create(
                    assessment=obj, category='vital_sign', item_key=item_key,
                    defaults={'item_name': item_name, 'value': value, 'unit': unit, 'score': None, 'max_score': None},
                )
            obj.details.filter(category='vital_sign').exclude(
                item_key__in=[k for k, _, _ in VITAL_SIGN_ITEMS]
            ).delete()

            diagnoses_json = request.POST.get('diagnoses_json', '[]')
            try:
                diagnoses_data = json.loads(diagnoses_json)
            except json.JSONDecodeError:
                diagnoses_data = []

            obj.diagnoses.all().delete()
            for diag in diagnoses_data:
                if diag.get('name', '').strip():
                    AssessmentDiagnosis.objects.create(
                        assessment=obj,
                        diagnosis_name=diag['name'].strip(),
                        diagnosis_code=diag.get('code', '').strip() or None,
                        is_primary=diag.get('is_primary', False),
                        notes=diag.get('notes', '').strip(),
                    )

            obj.recalculate_scores()
            messages.success(request, 'Initial Assessment saved successfully.')
            return redirect('medical:initial_assessment', pk=resident.pk, assessment_id=obj.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial_data = {}
        if assessment:
            initial_data = {
                'assessment_type': assessment.assessment_type,
                'assessment_date': assessment.assessment_date.strftime('%Y-%m-%dT%H:%M')
                if assessment.assessment_date
                else timezone.now().strftime('%Y-%m-%dT%H:%M'),
                'cognitive_status': assessment.cognitive_status,
                'allergies': assessment.allergies,
                'clinical_notes': assessment.clinical_notes,
            }
        form = AssessmentForm(initial=initial_data)

    adl_rows = []
    for item_key, item_name in ADL_ITEMS:
        detail = existing_details.get(('adl', item_key))
        adl_rows.append({
            'key': item_key, 'name': item_name,
            'score': detail.score if detail else 0, 'max_score': 4,
            'choices': ADL_SCORE_CHOICES,
        })

    iadl_rows = []
    for item_key, item_name in IADL_ITEMS:
        detail = existing_details.get(('iadl', item_key))
        iadl_rows.append({
            'key': item_key, 'name': item_name,
            'score': detail.score if detail else 0, 'max_score': 1,
            'choices': IADL_SCORE_CHOICES,
        })

    vs_rows = []
    for item_key, item_name, unit in VITAL_SIGN_ITEMS:
        detail = existing_details.get(('vital_sign', item_key))
        vs_rows.append({
            'key': item_key, 'name': item_name,
            'value': detail.value if detail else '', 'unit': unit,
        })

    diagnoses_list = [
        {'id': d.id, 'name': d.diagnosis_name, 'code': d.diagnosis_code or '',
         'is_primary': d.is_primary, 'notes': d.notes}
        for d in existing_diagnoses
    ]

    # Tạo initials từ full_name
    name_parts = resident.full_name.split()
    initials = ''.join(p[0].upper() for p in name_parts[:2]) if name_parts else '?'

    context = {
        'resident': resident,
        'initials': initials,
        'form': form,
        'assessment': assessment,
        'adl_rows': adl_rows,
        'iadl_rows': iadl_rows,
        'vs_rows': vs_rows,
        'diagnoses_list_json': json.dumps(diagnoses_list),
        'total_adl': assessment.total_adl_score if assessment else 0,
        'max_adl': assessment.max_adl_score if assessment else 32,
        'total_iadl': assessment.total_iadl_score if assessment else 0,
        'max_iadl': assessment.max_iadl_score if assessment else 8,
        'active_menu': 'medical',
    }
    return render(request, 'medical/sc_022.html', context)


# @login_required
# @require_POST
def api_add_diagnosis(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    name = data.get('name', '').strip()
    if not name:
        return JsonResponse({'error': 'Diagnosis name is required'}, status=400)
    if data.get('is_primary', False):
        assessment.diagnoses.all().update(is_primary=False)
    diag = AssessmentDiagnosis.objects.create(
        assessment=assessment,
        diagnosis_name=name,
        diagnosis_code=data.get('code', '').strip() or None,
        is_primary=data.get('is_primary', False),
        notes=data.get('notes', '').strip(),
    )
    return JsonResponse({
        'id': diag.id, 'name': diag.diagnosis_name,
        'code': diag.diagnosis_code or '', 'is_primary': diag.is_primary,
        'notes': diag.notes,
    })


# @login_required
# @require_POST
def api_remove_diagnosis(request, assessment_id, diagnosis_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    diag = get_object_or_404(AssessmentDiagnosis, id=diagnosis_id, assessment=assessment)
    diag.delete()
    return JsonResponse({'success': True})


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

    
def billing_panel(request):
    """
    SC035 - Cost / Billing Panel
    Dummy data based on Figma mockup + Holiday CR Logic
    """
    # Base daily rates
    loc_daily_rate = 285.00
    room_rate = 140.00
    medication_est = 45.00
    subtotal_per_day = loc_daily_rate + room_rate + medication_est # 470.00

    # CR Holidays Logic
    days_in_month = 30
    holiday_days = 1 # e.g. July 4th
    standard_days = days_in_month - holiday_days # 29
    
    # Holiday Surcharge (assumed $100 per holiday)
    holiday_surcharge_per_day = 100.00
    total_holiday_surcharge = holiday_days * holiday_surcharge_per_day # 100.00

    # Monthly calculation
    estimated_monthly = (standard_days * subtotal_per_day) + (holiday_days * (subtotal_per_day + holiday_surcharge_per_day))

    context = {
        'active_menu': 'care_planning',
        
        # Breakdown data
        'loc_daily_rate': f"{loc_daily_rate:.2f}",
        'room_rate': f"{room_rate:.2f}",
        'medication_est': f"{medication_est:.2f}",
        'subtotal_per_day': f"{subtotal_per_day:.2f}",
        
        # Holiday data
        'holiday_days': holiday_days,
        'holiday_surcharge_per_day': f"{holiday_surcharge_per_day:.2f}",
        'total_holiday_surcharge': f"{total_holiday_surcharge:.2f}",
        
        # Top cards data
        'estimated_day': f"{subtotal_per_day:.2f}",
        'estimated_month': f"{estimated_monthly:,.2f}",
    }
    
    return render(request, 'medical/billing_panel.html', context)

def care_plan_ack(request):
    """
    SC036 - Care Plan Acknowledgment
    Dummy data based on Figma mockup
    """
    context = {
        'active_menu': 'pending_ack',
        
        # Patient & Form info
        'patient_name': 'Robert Hayes',
        'submitted_by': 'Anna Lee, RN',
        'status': 'Pending Review',
        'submit_date': '2026-07-02',
        
        # Goals List
        'goals': [
            {
                'title': 'Mobility',
                'description': 'Goal: Ambulate 50 ft with walker x2/day.',
                'task': 'Assist ambulation w/ walker, 2x daily.',
                'status_badge': 'On Track',
                'status_class': 'badge-success-outline'
            },
            {
                'title': 'Skin Integrity',
                'description': 'Goal: Maintain skin integrity (no stage-2 injury).',
                'task': 'Reposition q2h; skin check each shift.',
                'status_badge': 'At Risk',
                'status_class': 'badge-warning-outline'
            },
            {
                'title': 'Nutrition',
                'description': 'Goal: Maintain fluid intake ≥ 1500 mL/day.',
                'task': 'Monitor fluid intake; document I/O.',
                'status_badge': 'On Track',
                'status_class': 'badge-success-outline'
            }
        ],
        
        # Role Info
        'physician_name': 'Dr. Alan Cho, MD',
        'license': 'CA-MD-88231',
        'npi': '1720493857',
        
        # IDT Acknowledgment Info
        'dietary_name': 'Grace Liu, RD',
        'dietary_status': 'Signed',
        'dietary_date': '2026-07-02 15:30'
    }
    
    return render(request, 'medical/care_plan_ack.html', context)



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

def bedside_vitals(request):
    """
    SC033 - Bedside Vitals (Ghi nhận Sinh hiệu tại giường)
    Dummy data based on Figma mockup
    """
    context = {
        'active_menu': 'care_planning',
        'resident_name': 'Robert Hayes',
        'room_number': 'Room 204B',
        'task_name': 'Vitals check',
        'due_time': 'due 14:00',
        'recorder_name': 'Marcus Rivera, CNA',
        'recorder_time': '2026-07-02 14:05',
    }
    return render(request, 'medical/bedside_vitals.html', context)

from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

def daily_tasks(request):
    # Dummy data based on the Figma mockup for SC032
    tasks_data = [
        {
            'resident_name': 'Robert Hayes',
            'room': 'Room 204B',
            'status': 'Active',
            'has_active_plan': True,
            'tasks': [
                {'id': 1, 'name': 'Ambulation assist (AM)', 'due': '08:00', 'overdue': False, 'state': 'Done'},
                {'id': 2, 'name': 'Reposition + skin check', 'due': '10:00', 'overdue': False, 'state': 'Done'},
                {'id': 3, 'name': 'Vitals check', 'due': '14:00', 'overdue': True, 'state': 'Refused'},
            ]
        },
        {
            'resident_name': 'Elena Ramos',
            'room': 'Room 106A',
            'status': 'Draft',
            'has_active_plan': False,
            'tasks': []
        },
        {
            'resident_name': 'David Nguyen',
            'room': 'Room 222A',
            'status': 'Active',
            'has_active_plan': True,
            'tasks': [
                {'id': 4, 'name': 'Assist with meal', 'due': '12:00', 'overdue': False, 'state': 'Done'},
                {'id': 5, 'name': 'Fluid intake monitoring', 'due': '15:00', 'overdue': False, 'state': 'Refused'},
            ]
        }
    ]
    
    context = {
        'active_menu': 'care_planning',
        'residents_tasks': tasks_data,
        'completed_tasks': 8,
        'total_tasks': 14,
    }
    return render(request, 'medical/daily_tasks.html', context)

@require_POST
def update_task_status(request):
    try:
        data = json.loads(request.body)
        task_id = data.get('task_id')
        new_state = data.get('state')
        
        # NOTE: Here you would normally fetch the task from the database
        # e.g., task = Task.objects.get(id=task_id)
        # task.state = new_state
        # task.save()
        
        return JsonResponse({
            'status': 'success', 
            'task_id': task_id, 
            'new_state': new_state,
            'message': f'Task {task_id} updated to {new_state} successfully.'
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
def save_bedside_vitals(request):
    try:
        data = json.loads(request.body)
        # Mocking DB save
        return JsonResponse({
            'status': 'success',
            'message': 'Vitals saved successfully'
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


