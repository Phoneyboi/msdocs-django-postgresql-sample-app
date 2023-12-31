from django.urls import path
from .views import (FrameListView, FrameDetailView, ExperienceDetailView, AuthenticImmersiveExperienceDetailView,
                    AddLessonLearnedView)
# Import other views

app_name = 'experiential'

urlpatterns = [
    path('frames/', FrameListView.as_view(), name='frames_list'),
    path('frames/<slug:slug>/', FrameDetailView.as_view(), name='frame_detail'),
    path('experience/<int:pk>/', ExperienceDetailView.as_view(), name='experience_detail'),
    path('authentic-immersive-experience/<int:pk>/', AuthenticImmersiveExperienceDetailView.as_view(),
         name='authentic_immersive_experience_detail'),
    path('add-lesson/<int:frame_id>/<int:experience_id>/<int:aie_id>/', AddLessonLearnedView.as_view(),
         name='add-lesson'),
]
