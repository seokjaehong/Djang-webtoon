from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from .models import Webtoon
from .models import Episode, Webtoon


def webtoon_list(request):
    '''
    webtoon 목록 보여주기
    :param request:
    :return:
    '''
    webtoonlist = Webtoon.objects.all()
    context = {
        'webtoonlist': webtoonlist
    }

    return render(request, 'webtoon/main.html', context)


def webtoon_detail(request, pk):
    # webtoon = Webtoon.objects.get(pk=pk)
    webtoon = Webtoon.objects.get(pk=pk)
    context = {
        'webtoon': webtoon
    }
    # detail을 불러올 때 crawling을 실행하도록 변경 ,page는 일단 1페이지만.
    webtoon.get_episode_list(webtoon_id=webtoon.webtoon_id)
    return render(request, 'webtoon/detail.html', context)
    '''
    webtoon episode 목록 보여주기
    '''
