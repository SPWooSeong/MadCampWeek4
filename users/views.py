import json
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from users.models import User


# Create your views here.

def index(request):
    return HttpResponse("Hello world. You're at the users index.")

@csrf_exempt
def google_login_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id_token_str = data.get('id_token')

        try:
            idinfo = id_token.verify_oauth2_token(id_token_str, requests.Request(), settings.GOOGLE_CLIENT_ID, clock_skew_in_seconds=10)

            # 사용자 정보 가져오기
            username = idinfo.get('name')
            email = idinfo.get('email')
            profile_picture = idinfo.get('picture')

            # 사용자 정보를 데이터베이스에 저장 또는 업데이트
            user, created = User.objects.get_or_create(
                google_account=email,
                defaults={
                    'nickname': username,
                    'profile_image_url': profile_picture
                }
            )

            return JsonResponse({                
                'access_token': id_token_str,
                'username': username,
                'email': email,
                'profile_picture': profile_picture})
        except ValueError:
            return JsonResponse({'error': 'Invalid token'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def get_user_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            google_account = data.get('google_account')
            
            if not google_account:
                return HttpResponseBadRequest('google_account is required.')
            
            try:
                user = User.objects.get(google_account=google_account)
                response_data = {
                    'profile_image_url': user.profile_image_url,
                    'nickname': user.nickname,
                }
                return JsonResponse(response_data, status=200)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')

    return HttpResponseBadRequest('Only POST method is allowed')

@csrf_exempt  # Use this decorator to exempt the view from CSRF verification
def update_nickname(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            google_account = data.get('google_account')
            new_nickname = data.get('nickname')
            
            if not google_account or not new_nickname:
                return HttpResponseBadRequest('google_account and nickname are required.')
            
            try:
                user = User.objects.get(google_account=google_account)
                user.nickname = new_nickname
                user.save()
                return JsonResponse({'message': 'Nickname updated successfully'}, status=200)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')
    
    return HttpResponseBadRequest('Only PUT methods are allowed')