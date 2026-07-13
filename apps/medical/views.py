from django.shortcuts import render

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
