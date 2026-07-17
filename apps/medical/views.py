from django.shortcuts import render
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
