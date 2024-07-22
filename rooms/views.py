import json
from django.http import HttpResponse, JsonResponse
from subjects.models import Subject
from users.models import User
from rooms.models import Room
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


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
    
    return JsonResponse({'status': 'success', 'room_id': room.room_id})

@csrf_exempt
def exit_room(request):
    # Extract google_account from request body
    body = json.loads(request.body.decode('utf-8'))
    google_account = body.get('google_account')

    # Retrieve the user and the room they are in
    try:
        user = User.objects.get(google_account=google_account)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    
    room = user.room_id

    if not room:
        return JsonResponse({"error": "User is not in a room"}, status=400)

    # Update the user's room_id to null
    user.room_id = None
    user.save()

    # Decrement the current_people count of the room
    room.current_people -= 1

    # If current_people is 0, delete the room
    if room.current_people == 0:
        room.delete()
        return JsonResponse({"message": "Room deleted as it became empty"}, status=200)

    # If the google_account of the room owner is the same as the exiting user's google_account
    if room.google_account.google_account == google_account:
        # Find another user in the room to assign as the new owner
        new_owner = User.objects.filter(room_id=room).exclude(google_account=google_account).first()
        if new_owner:
            room.google_account = new_owner
        else:
            room.delete()
            return JsonResponse({"message": "Room deleted as it became empty"}, status=200)

    room.save()

    return JsonResponse({"message": "User has exited the room"}, status=200)

@require_http_methods(["POST"])
@csrf_exempt
def enter_room(request):
    # Extract google_account and room_id from request body
    body = json.loads(request.body.decode('utf-8'))
    google_account = body.get('google_account')
    room_id = body.get('room_id')

    # Retrieve the user and the room
    try:
        user = User.objects.get(google_account=google_account)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    
    try:
        room = Room.objects.get(room_id=room_id)
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)
    
    if user.room_id is None:
        # Enter room
        # Check if the room is full
        if room.current_people >= room.max_people:
            return JsonResponse({"error": "방이 모두 찼습니다"}, status=400)
        else:
            # Update the user's room_id and increment the current_people of the room
            user.room_id = room
            user.save()
            room.current_people += 1
            room.save()
    else:
        # Not new user, reloading
        if user.room_id.room_id != int(room_id):
            return JsonResponse({"error": "Wrong room"}, status=404)
    
    # Prepare the response data
    subject = room.subject_id
    users_in_room = User.objects.filter(room_id=room)

    response_data = {
        "room_id": room.room_id,
        "title": room.room_title,
        "google_account": room.google_account.google_account,
        "max_people": room.max_people,
        "current_people": room.current_people,
        "is_started": room.is_started,
        "subject": {
            "subject_id": subject.subject_id,
            "subject_name": subject.subject_name,
            "num_used": subject.num_used,
        },
        "users": [
            {
                "google_account": user.google_account,
                "nickname": user.nickname,
                "profile_image_url": user.profile_image_url,
                "room_id": user.room_id.room_id,
            } for user in users_in_room
        ]
    }

    return JsonResponse(response_data, status=200)