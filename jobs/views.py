from django.shortcuts import render
from django.http import HttpResponseRedirect
from jobs.dbhelp import execmysql
from jobs.jenkfunc import GetJenkinsInfo
from jobs.config import HOST, USER, PASSWORD, DB
from jobs.config import jenkins_url, jenkinsUser, jenkinsPassword
import json

# Create your views here.


def index(request):
    exmysql = execmysql(HOST, USER, PASSWORD, DB)
    res = exmysql.get_all_counts()
    jobsname_list = res[0]
    jobscount_list = res[1]

    counts = {
        'name': '发版次数',
        'color': 'gray',
        'data': jobscount_list
    }

    xjobname = {
        'categories': jobsname_list,
        'crosshair': 'true'
    }
    json_counts = json.dumps(counts, separators=(',', ':'))
    json_xjobname = json.dumps(xjobname, separators=(',', ':'))

    return render(request, "jobs/index.html", {'jobsname': json_xjobname, 'jobscount': json_counts})


def get_info_bw(request):
    btime = request.GET.get('btime')
    etime = request.GET.get('etime')
    exmysql = execmysql(HOST, USER, PASSWORD, DB)
    res = exmysql.get_counts(btime, etime)
    jobsname_list = res[0]
    jobscount_list = res[1]
    counts = {
        'name': '发版次数',
        'color': 'gray',
        'data': jobscount_list
    }

    xjobname = {
        'categories': jobsname_list,
        'crosshair': 'true'
    }
    json_counts = json.dumps(counts, separators=(',', ':'))
    json_xjobname = json.dumps(xjobname, separators=(',', ':'))

    return render(request, "jobs/index.html", {'jobsname': json_xjobname, 'jobscount': json_counts})


def update_info(request):
    exjenkins = GetJenkinsInfo(jenkins_url, jenkinsUser, jenkinsPassword)
    exjenkins.update_jobinfo()
    exjenkins.update_jobname()

    return HttpResponseRedirect('/')
