from django.shortcuts import render

# Create your views here.

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
