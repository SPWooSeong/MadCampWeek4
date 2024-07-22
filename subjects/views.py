from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from subjects.models import Element, Subject

# Create your views here.
def index(request):
    return HttpResponse("Hello world. You're at the subjects index.")

def subject_ranking(request):
    # 모든 Subject 객체를 가져와 num_used를 기준으로 내림차순 정렬
    subjects = Subject.objects.all().order_by('-num_used')
    
    # 리스트에 담을 데이터 생성
    subjects_rank = []
    for rank, subject in enumerate(subjects, start=1):
        subjects_rank.append({
            'subject_id': subject.subject_id,
            'subject_name': subject.subject_name,
            'subject_rank': rank,
            'num_used': subject.num_used
        })

    return JsonResponse(subjects_rank, safe=False)

def element_ranking(request, subject_id):
    try:
        elements = Element.objects.filter(subject_id=subject_id).order_by('-num_won')
        
        elements_data = []
        for rank, element in enumerate(elements, start=1):
            elements_data.append({
                'element_id': element.element_id,
                'element_name': element.element_name,
                'element_image': element.element_image.url,  # 이미지 URL
                'num_won': element.num_won,
                'element_rank': rank
            })
        
        return JsonResponse(elements_data, safe=False)
    except :
        return JsonResponse([], safe=False)
    
def subject_list(request):
    subjects = Subject.objects.all()
    
    subjects_data = []
    for subject in subjects:
        subjects_data.append({
            'subject_id': subject.subject_id,
            'subject_name': subject.subject_name,
        })
    
    return JsonResponse(subjects_data, safe=False)