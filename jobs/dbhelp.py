#数据库相关功能

import pymysql
from jobs.config import HOST, USER, PASSWORD, DB

class execmysql(object):

    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    #创建数据库连接
    def connectdb(self):
        db = pymysql.connect(self.host, self.user, self.password, self.db)

        return db

    #查找jobname和buildnum 确认数据不重复存储
    def search_jobname_buildnum(self, jobname, buildnum):
        db = self.connectdb()
        cursor = db.cursor()
        SQL = "SELECT JOBNAME, BUILDNUM FROM jobinfo WHERE JOBNAME = '%s' AND BUILDNUM = '%d'" \
              % (jobname, int(buildnum))
        try:
            cursor.execute(SQL)
            result = cursor.fetchall()
            if result:
                return False
            else:
                return True
        except BaseException as e:
            print("出现错误: %s " % e)
        db.close()

    #查找jobname，确认数据不重复存储
    def search_jobname(self, jobname):
        db = self.connectdb()
        cursor = db.cursor()
        SQL = "SELECT JOBNAME FROM jobname WHERE JOBNAME = '%s'" % (jobname)
        try:
            cursor.execute(SQL)
            result = cursor.fetchall()
            if result:
                return False
            else:
                return True
        except BaseException as e:
            print("出现错误：%s" % e)
        db.close()

    #获取所有的jobname
    def get_all_jobname(self):
        db = self.connectdb()
        cursor = db.cursor()
        get_jobname_sql = "SELECT * FROM jobname"
        try:
            cursor.execute(get_jobname_sql)
            result = cursor.fetchall()
            jobsname_list = []
            for job in result:
                jobsname_list.append(job[1])
        except BaseException as e:
            print("出现错误：%s" % e)
        db.close()
        return jobsname_list

    #获取每个jobname的build次数
    def get_all_counts(self):
        db = self.connectdb()
        cursor = db.cursor()
        jobsname_list = self.get_all_jobname()
        nozerojobsname_list = []
        jobscount_list = []
        for jobname in jobsname_list:
            get_counts_sql = "SELECT COUNT(JOBNAME) FROM jobinfo WHERE JOBNAME = '%s'" % (jobname)
            try:
                cursor.execute(get_counts_sql)
                count = cursor.fetchone()[0]
                if int(count) == 0:
                    continue
                else:
                    jobscount_list.append(count)
                    nozerojobsname_list.append(jobname)
            except BaseException as e:
                print("出现错误：%s" % e)
        name_count = [nozerojobsname_list, jobscount_list]
        db.close()
        return name_count

    #按时间范围查找次数
    def get_counts(self, btime, etime):
        db = self.connectdb()
        cursor = db.cursor()
        jobsname_list = self.get_all_jobname()
        jobscount_list = []
        nozero_jobname = []
        for jobname in jobsname_list:
            get_counts_sql = "SELECT COUNT(JOBNAME) FROM jobinfo WHERE JOBNAME = '%s' \
            AND date(BUILDTIME) BETWEEN '%s' AND '%s'" % (jobname, btime, etime)
            try:
                cursor.execute(get_counts_sql)
                counts = cursor.fetchone()[0]
                if int(counts) == 0:
                    continue
                else:
                    nozero_jobname.append(jobname)
                    jobscount_list.append(counts)
            except BaseException as e:
                print("出现错误：%s" % e)
        name_count = [nozero_jobname, jobscount_list]
        db.close()
        print(name_count)
        return name_count


    #插入build 历史
    def insert_buildhistory(self, jobname, status, buildnum, buildtime):
        db = self.connectdb()
        cursor = db.cursor()
        SQL = "INSERT INTO jobinfo(JOBNAME, STATUS, BUILDNUM, BUILDTIME) VALUES ('%s', '%s', '%d', '%s')" \
              % (jobname, status, buildnum, buildtime)
        try:
            if self.search_jobname_buildnum(jobname, buildnum):
                cursor.execute(SQL)
                db.commit()
            else:
                print("%s的%d记录已存在" % (jobname, buildnum))
        except BaseException as e:
            print("出现错误：%s" % e)
        db.close()

    #插入jobname
    def insert_jobname(self, jobname):
        db = self.connectdb()
        cursor = db.cursor()
        SQL = "INSERT INTO jobname(JOBNAME) VALUES ('%s')" % (jobname)
        try:
            if self.search_jobname(jobname):
                cursor.execute(SQL)
                db.commit()
            else:
                print("记录已存在")
        except BaseException as e:
            print("出现错误：%s" % e)
        db.close()


if __name__ == '__main__':
    exmysql = execmysql(HOST, USER, PASSWORD, DB)
    exmysql.get_counts('2018-10-10', '2019-1-4')