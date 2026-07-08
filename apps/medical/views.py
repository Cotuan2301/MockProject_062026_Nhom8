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
