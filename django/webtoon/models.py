from django.db import models
from django.utils import timezone
import crawler

# Create your models here.
class Webtoon(models.Model):
    webtoon_id = models.CharField(max_length=200)
    title  = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def get_episode_list(self):
        '''
         """웹에서 크롤링 한 결과로 이 Webtoon에 속하는 Episode들을 생성해준다"""
        :return:
        '''



class Episode(models.Model):
    webtoon = models.ForeignKey(Webtoon, on_delete=models.CASCADE)
    episode_id  = models.CharField(max_length=200)
    title  = models.CharField(max_length=200)
    rating  = models.CharField(max_length=200)
    created_date  = models.CharField(max_length=200)

    def __str__(self):
        return self.title