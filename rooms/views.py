import json
from django.http import HttpResponse, JsonResponse
from subjects.models import Subject
from users.models import User
from rooms.models import Room
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    return HttpResponse("Hello world. You're at the users index.")

def current_room(request):
    rooms = Room.objects.filter(is_started=False)
    
    # 반환할 데이터 리스트
    rooms_info = []

    for room in rooms:
        subject = room.subject_id  # ForeignKey 관계를 통해 Subject 객체를 가져옴
        room_data = {
            'room_id': room.room_id,
            'room_title': room.room_title,
            'google_account': room.google_account.google_account,  # 외래 키의 실제 값을 가져옴
            'subject_name': subject.subject_name,  # subject_id 대신 subject_name을 사용
            'max_people': room.max_people,
            'current_people': room.current_people,
            'is_started': room.is_started,            
        }
        rooms_info.append(room_data)

    return JsonResponse(rooms_info, safe=False)

@csrf_exempt
def make_room(request):
    # POST 요청으로 전달된 데이터를 가져옴
    data = json.loads(request.body)
    google_account = data.get('google_account')
    room_title = data.get('room_title')
    subject_id = data.get('subject_id')
    max_people = data.get('max_people')
    user = User.objects.get(google_account=google_account)
    subject = Subject.objects.get(subject_id=subject_id)

    room = Room.objects.create(
        google_account=user,
        room_title=room_title,
        subject_id=subject,
        max_people=max_people
    )
    
    return HttpResponse("Room created successfully.")