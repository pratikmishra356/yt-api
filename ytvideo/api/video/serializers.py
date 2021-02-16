from rest_framework import serializers
from .models import Video



class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = ('id','video_id','title','description','url', 'upload_time', 'thumbnail')
