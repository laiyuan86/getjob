#jenkins相关功能

from jenkinsapi.jenkins import Jenkins
from jenkinsapi.build import Build
from jobs.config import jenkins_url, jenkinsUser, jenkinsPassword
from jobs.config import HOST, USER, PASSWORD, DB
from jobs.dbhelp import execmysql
import time


class GetJenkinsInfo(object):

    def __init__(self, jenkins_url, jenkinsUser, jenskinsPassword):
        self.jenkins_url = jenkins_url
        self.jenkinsUser = jenkinsUser
        self.jenkinsPassword = jenskinsPassword

    #获取服务实例
    def get_server_instance(self):
        server = Jenkins(jenkins_url, username=jenkinsUser, password=jenkinsPassword)
        return server

    #获取jobs
    def get_jobs(self):
        server = self.get_server_instance()
        jobs = server.get_jobs()
        jobs_name_list = []
        for job_name, _ in jobs:
            jobs_name_list.append(job_name)
        print(jobs_name_list)
        return jobs_name_list

    #获取jobs build num
    def get_jobs_build_num(self):
        server = self.get_server_instance()
        jobs_list = server.get_jobs_list()
        build_num = {}
        for i in jobs_list:
            try:
                build_num[i] = server[i].get_last_good_buildnumber()
            except BaseException as e:
                print("出现错误： %s" % e)
        print(build_num)
        return build_num

    #获取构建历史
    def get_job_buildhistory(self, jobname):
        server = self.get_server_instance()
        job = server[jobname]
        data = job.__dict__['_data']['builds']
        job_build_list = []
        for i in data:
            job_build_dic = {}
            lll = Build(i['url'], i['number'], job)
            lll_dic = lll.get_data(i['url']+'api/python/')
            timest = lll_dic['timestamp']/1000
            job_build_dic['buildtime'] = time.strftime("%Y-%m-%d", time.localtime(timest))
            job_build_dic['status'] = lll_dic['result']
            job_build_dic['buildnum'] = lll_dic['number']
            job_build_list.append(job_build_dic)
        return job_build_list

    #更新jobinfo数据
    def update_jobinfo(self):
        exmysql =  execmysql(HOST, USER, PASSWORD, DB)
        jobs_name_list = self.get_jobs()
        for jobname in jobs_name_list:
            res = self.get_job_buildhistory(jobname)
            for jobuild in res:
               exmysql.insert_buildhistory(jobname, jobuild['status'], jobuild['buildnum'], jobuild['buildtime'])

    #更新jobname数据
    def update_jobname(self):
        exmysql = execmysql(HOST, USER, PASSWORD, DB)
        jobs_name_list = self.get_jobs()
        for jobname in jobs_name_list:
            exmysql.insert_jobname(jobname)


if __name__ == '__main__':
    JenkinsInfo = GetJenkinsInfo(jenkins_url, jenkinsUser, jenkinsPassword)
    res = JenkinsInfo.update_jobinfo()