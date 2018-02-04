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
    def __init__(self, webtoonname, episode_id, url_thumbnail, title, rating, created_date):
        self.webtoonname = webtoonname
        self.episode_id = episode_id
        self.url_thumbnail = url_thumbnail
        self.title = title
        self.rating = rating
        self.created_date = created_date

    def __str__(self):
        return f'웹툰이름 : {self. webtoonname} id:{self.episode_id} | 타이틀:{self.title} | 발매일:{self.created_date} | 평점: {self.rating}'


def get_episode_list(webtoon_id, page, refresh_html = True):
    """
    고유ID(URL에서 titleId값)에 해당하는 웹툰의
    특정 page에 있는 에피소드 목록을 리스트로 리턴
    """
    file_path = os.path.join(DATA_DIR, f'episode_list_{webtoon_id}.html')
    try:
        file_mode = 'wt' if refresh_html else 'xt'
        with open(file_path, file_mode) as f:
            # url과 parameter구분해서 requests사용
            url = "https://comic.naver.com/webtoon/list.nhn"
            parameter = {
                'titleId': webtoon_id,
                'page': page
            }
            response = requests.get(url, parameter)
            source = response.text
            # 만약 받은 파일의 길이가 지나치게 짧을 경우 예외를 일으키고
            # 예외 블럭에서 기록한 파일을 삭제하도록 함
            file_length = f.write(source)
            if file_length < 10:
                raise ValueError('파일이 너무 짧습니다')
    except FileExistsError:
        print(f'"{file_path}" file is already exists!')
    except ValueError:
        # 파일이 너무 짧은 경우
        os.remove(file_path)
        return

    soup = BeautifulSoup(response.text, 'lxml')

    # basicinfo = soup.select('div.comicinfo > div.detail h2')

    # webtoonname = re.search(r"(.*?)\>\s\t(.*?)\<",basicinfo,re.DOTALL).group(2)

    # webtoonname= r
    webtoonname='빈칸'


    viewlist = soup.select('div#content table.viewList > tr')
    result = list()
    for tr in viewlist:
        title = tr.find('td', class_="title").find('a').text
        episode_id_meta =  tr.find('a').get('href')
        episode_id = re.search(r"\=.*?\=(.*?)\&",episode_id_meta,re.DOTALL).group(1)
        url_thumbnail = tr.find('a').find('img').get('src')
        rating = tr.find('div', class_='rating_type').find('strong').text
        created_date = tr.find('td', class_='num').text

        episodedata = EpisodeData(webtoonname=webtoonname, title=title, episode_id=episode_id, url_thumbnail=url_thumbnail, rating=rating,
                                  created_date=created_date)
        result.append(episodedata)

    return result

result = get_episode_list('703835',1)


for index, i in enumerate(result) :
    print(result[index])