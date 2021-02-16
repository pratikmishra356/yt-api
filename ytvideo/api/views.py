import requests
from django.conf import settings
from django.http import JsonResponse
from api.video.models import Video
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.db.models import Q

# Create your views here.



    

def home(request):
    

    
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    search_params = {
        'part' : 'snippet',
        'q' : 'cricket',
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'maxResults' : 10,
        'type' : 'video'
    }

    r = requests.get(search_url, params=search_params)

    results = r.json()['items']

    video_ids = []
    for result in results:
        video_ids.append(result['id']['videoId'])

    

    video_params = {
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'part' : 'snippet,contentDetails',
        'id' : ','.join(video_ids),
        'maxResults' : 9
    }

    r = requests.get(video_url, params=video_params)

    results = r.json()['items']

    
    for result in results:
        video_data = Video(
            
            video_id = result['id'],
            title = result['snippet']['title'],
            description = result['snippet']['description'],
            url = f'https://www.youtube.com/watch?v={ result["id"] }',
            upload_time = result['snippet']['publishedAt'],
            thumbnail = result['snippet']['thumbnails']['high']['url']
        )

        video_data.save()
        print(video_data)
    
    items = []
    
    if request.method == 'POST':

        if request.POST['submit'] == 'lucky':
            
            items = Video.objects.all()

        else:

            items = Video.objects.filter(
                Q(title__contains=request.POST['search']) |
                Q(description__contains=request.POST['search'])     
            )


    context = {
    'videos' : items
    }

    return render(request, 'api/index.html', context)

