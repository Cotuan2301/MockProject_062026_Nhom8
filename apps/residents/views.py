import datetime
from django.shortcuts import render


def _sample_residents():
    """
    Sample data so the Resident List page renders immediately without
    requiring migrations/DB seeding. Swap this out for
    Resident.objects.all() once the model is migrated and populated.
    """
    raw = [
        dict(resident_id='RES-1001', full_name='Margaret Thompson', room_number='101-A',
             status='active', dob=datetime.date(1942, 3, 15), gender='female',
             payer_source='Medicare', admission_date=datetime.date(2021, 6, 2)),
        dict(resident_id='RES-1002', full_name='Robert Johnson', room_number='205-B',
             status='active', dob=datetime.date(1938, 7, 22), gender='male',
             payer_source='Medicaid', admission_date=datetime.date(2020, 1, 10)),
        dict(resident_id='RES-1003', full_name='Dorothy Williams', room_number='118-C',
             status='discharged', dob=datetime.date(1945, 11, 4), gender='female',
             payer_source='Private Pay', admission_date=datetime.date(2019, 9, 18)),
        dict(resident_id='RES-1004', full_name='Charles Davis', room_number='302-A',
             status='pending', dob=datetime.date(1950, 5, 18), gender='male',
             payer_source='Medicare', admission_date=datetime.date(2024, 2, 27)),
        dict(resident_id='RES-1005', full_name='Helen Martinez', room_number='210-B',
             status='active', dob=datetime.date(1936, 9, 30), gender='female',
             payer_source='Medicaid', admission_date=datetime.date(2018, 12, 5)),
        dict(resident_id='RES-1006', full_name='James Wilson', room_number='115-A',
             status='active', dob=datetime.date(1940, 2, 14), gender='male',
             payer_source='Medicare', admission_date=datetime.date(2022, 4, 3)),
    ]
    for r in raw:
        r['yob'] = r['dob'].year
    return raw


def resident_list(request):
    status_filter = request.GET.get('status', 'all')
    query = request.GET.get('q', '').strip().lower()

    residents = _sample_residents()

    if status_filter in ('active', 'discharged', 'pending'):
        residents = [r for r in residents if r['status'] == status_filter]

    if query:
        residents = [
            r for r in residents
            if query in r['full_name'].lower()
            or query in r['room_number'].lower()
            or query in r['resident_id'].lower()
        ]

    counts = {
        'all': len(_sample_residents()),
        'active': sum(1 for r in _sample_residents() if r['status'] == 'active'),
        'discharged': sum(1 for r in _sample_residents() if r['status'] == 'discharged'),
        'pending': sum(1 for r in _sample_residents() if r['status'] == 'pending'),
    }

    context = {
        'residents': residents,
        'status_filter': status_filter,
        'query': request.GET.get('q', ''),
        'counts': counts,
    }
    return render(request, 'residents/list.html', context)


# ==========================================
# HÀM MỚI THÊM VÀO CHO PRE-ADMISSION
# ==========================================
def pre_admission(request):
    """
    Hàm xử lý cho màn hình Pre-Admission.
    Lưu ý: Đảm bảo bạn có file HTML tương ứng trong thư mục templates.
    """
    context = {
        'page_title': 'Pre-Admission Screening'
    }
    # Nếu file HTML của bạn tên khác 'pre_admission.html', hãy đổi tên ở dòng dưới cho khớp
    return render(request, 'residents/pre_admission.html', context)