import json
from django.http import HttpResponse, JsonResponse
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
            idinfo = id_token.verify_oauth2_token(id_token_str, requests.Request(), settings.GOOGLE_CLIENT_ID)

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