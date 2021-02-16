from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='api.home'),
    path('video/', include('api.video.urls')),
]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

