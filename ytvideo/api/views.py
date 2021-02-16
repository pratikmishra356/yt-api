import requests
from django.conf import settings
from django.http import JsonResponse
from api.video.models import Video
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.db.models import Q

# Create your views here.
    
#Creting async function which will fetch data from the api
#and will store it in the database

@sync_to_async
def fetch_data():
    
    p=100;
    while(p):
        
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part' : 'snippet',
            'q' : 'cricket',
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 10,
            'type' : 'video'
        }

        #querying the videos with thier id
        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        

        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 10
        }
        #querying detail infromation about the videos
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
            #stroing the new video data into the databse
            video_data.save()
        
        p=p-1
    
    
#it will give a html response based on the query
async def home(request):
    

    
    asyncio.ensure_future(fetch_data())
    
    
    item = []
    
    if request.method == 'POST':

        if request.POST['submit'] == 'lucky':
            
            item = Video.objects.all()

        else:

            item = Video.objects.filter(
                Q(title__contains=request.POST['search'])
                   
            )


    context = {
    'videos' : item
    }

    return render(request, 'api/index.html', context)


