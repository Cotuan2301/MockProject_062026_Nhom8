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