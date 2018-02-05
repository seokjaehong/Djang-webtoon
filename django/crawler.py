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


class EpisodeData:
    def __init__(self, episode_id, url_thumbnail, title, rating, created_date):
        self.episode_id = episode_id
        self.url_thumbnail = url_thumbnail
        self.title = title
        self.rating = rating
        self.created_date = created_date

    def __str__(self):
        return f'id:{self.episode_id} | 타이틀:{self.title} | 평점: {self.rating} | 발매일:{self.created_date} '


def get_episode_list(webtoon_id, page, refresh_html=True):
    """
    고유ID(URL에서 titleId값)에 해당하는 웹툰의
    특정 page에 있는 에피소드 목록을 리스트로 리턴
    """
    file_path = os.path.join(DATA_DIR, f'episode_list_{webtoon_id}.html')
    try:
        file_mode = 'wt' if refresh_html else 'xt'
        with open(file_path, file_mode) as f:
            url = "https://comic.naver.com/webtoon/list.nhn"
            parameter = {
                'titleId': webtoon_id,
                'page': page
            }
            response = requests.get(url, parameter)
            source = response.text
            file_length = f.write(source)
            if file_length < 10:
                raise ValueError('파일이 너무 짧습니다')
    except FileExistsError:
        print(f'"{file_path}" file is already exists!')
    except ValueError:
        os.remove(file_path)
        return

    soup = BeautifulSoup(response.text, 'lxml')

    banner = soup.find('tr', class_='band_banner')
    if banner:
        banner.extract()
    # webtoonname = soup.find('div',class_='comicinfo').find('div', class_='thumb').find('a').find('img').get('alt')
    # webtoonID = webtoon_id

    viewlist = soup.select('div#content table.viewList > tr')
    # viewlist = soup.find('div',attrs={'id':'content'}).findAll('table', class_='viewList').findAll('tr')
    result = list()
    for tr in viewlist:
        title = tr.find('td', class_="title").find('a').text
        # title = tr.find('td', class_="title")
        episode_id_meta = tr.find('a').get('href')
        episode_id = re.search(r"=.*?=(.*?)&", episode_id_meta, re.DOTALL).group(1)
        url_thumbnail = tr.find('a').find('img').get('src')
        rating = tr.find('div', class_='rating_type').find('strong').text
        created_date = tr.find('td', class_='num').text

        episodedata = EpisodeData(title=title, episode_id=episode_id,
                                  url_thumbnail=url_thumbnail, rating=rating,
                                  created_date=created_date)
        result.append(episodedata)

    return result



result = get_episode_list('681453',1)

for index, i in enumerate(result):
    print(result[index])
