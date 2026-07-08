from django.shortcuts import render

def daily_tasks(request):
    # Dummy data based on the Figma mockup for SC032
    tasks_data = [
        {
            'resident_name': 'Robert Hayes',
            'room': 'Room 204B',
            'status': 'Active',
            'has_active_plan': True,
            'tasks': [
                {'name': 'Ambulation assist (AM)', 'due': '08:00', 'overdue': False, 'state': 'Done'},
                {'name': 'Reposition + skin check', 'due': '10:00', 'overdue': False, 'state': 'Done'},
                {'name': 'Vitals check', 'due': '14:00', 'overdue': True, 'state': 'Refused'},
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
                {'name': 'Assist with meal', 'due': '12:00', 'overdue': False, 'state': 'Done'},
                {'name': 'Fluid intake monitoring', 'due': '15:00', 'overdue': False, 'state': 'Refused'},
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
