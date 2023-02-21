from django.urls import path
from .views import TopicViews

urlpatterns = [
    path('<str:author_id>', TopicViews.as_view())

]