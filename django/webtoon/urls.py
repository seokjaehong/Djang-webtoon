from django.urls import path

from . import views

app_name='webtoon'
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.webtoon_list, name='webtoon_list'),
    path('<int:webtoonid>/', views.webtoon_detail, name='webtoon_detail')
]