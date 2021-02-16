from rest_framework import viewsets
from .serializers import VideoSerializer
from .models import Video


# Create your views here.


#querying all the video from the databse 
class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by('-upload_time')
    serializer_class = VideoSerializer

    

