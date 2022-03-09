from utils.db_util import mysql
from django.shortcuts import render


def main(request):
    sql = 'select id,title from novel limit 10'
    result = mysql.getAll(sql)

    context = {'novel_list': result}
    return render(request, 'novel_list.html', context)


def chapter(request, novel_id):
    sql = 'select title, content from novel where id = %(id)s'
    param = {'id': novel_id}
    result = mysql.getOne(sql, param)
    context = {'novel': result}
    return render(request, 'novel.html', context)

