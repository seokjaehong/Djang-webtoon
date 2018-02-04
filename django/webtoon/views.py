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
    return render(request, 'webtoon/detail.html', context)
    '''
    webtoon episode 목록 보여주기
    '''

