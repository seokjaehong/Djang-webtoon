from django.db import models

import os
import re
import requests
from bs4 import BeautifulSoup, NavigableString

# utils가 있는
PATH_MODULE = os.path.abspath(__file__)

# 프로젝트 컨테이너 폴더 경로
ROOT_DIR = os.path.dirname(PATH_MODULE)

# data/ 폴더 경로
DATA_DIR = os.path.join(ROOT_DIR, 'data')

# Create your models here.
class Webtoon(models.Model):
    webtoon_id = models.CharField(max_length=200)
    title  = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def get_episode_list(self, refresh_html=True):
        '''
         """웹에서 크롤링 한 결과로 이 Webtoon에 속하는 Episode들을 생성해준다"""
        :return:
        '''
        webtoon_id = '703835' #1인용기분
        page = 1

        url = "https://comic.naver.com/webtoon/list.nhn"
        parameter = {
            'titleId': webtoon_id,
            'page': page
        }
        response = requests.get(url, parameter)
        source = response.text

        soup = BeautifulSoup(response.text, 'lxml')

        viewlist = soup.select('div#content table.viewList > tr')
        result = list()
        for tr in viewlist:
            title = tr.find('td', class_="title").find('a').text
            # title = tr.find('td', class_="title").find('a').find('img')
            episode_id_meta = tr.find('a').get('href')
            episode_id = re.search(r"=.*?=(.*?)&", episode_id_meta, re.DOTALL).group(1)
            url_thumbnail = tr.find('a').find('img').get('src')
            rating = tr.find('div', class_='rating_type').find('strong').text
            created_date = tr.find('td', class_='num').text

            Episode.objects.create(webtoon_id=self.pk, title=title, episode_id=episode_id,
                                      rating=rating,created_date=created_date)
            # episode_data_list.save()

class Episode(models.Model):
    webtoon = models.ForeignKey(Webtoon, on_delete=models.CASCADE)
    episode_id  = models.CharField(max_length=200)
    title  = models.CharField(max_length=200)
    rating  = models.CharField(max_length=200)
    created_date  = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.episode_id} {self.webtoon} | {self.title}'