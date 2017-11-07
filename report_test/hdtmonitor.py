#encoding:utf-8
import MySQLdb as mysql,time,datetime

def tmpdaylist(days):
    d = datetime.datetime.now()
    # tmpdate_from=d+datetime.timedelta(days=-int(days))
    tmpdate_from=d+datetime.timedelta(days=-int(days))
    tmpdate_from=str(tmpdate_from)[0:10]
    daylist=tmpdate_from
    return daylist

# 返回包含日期的sql 查找托底订单
def tmpsqllist(days,job_id):
    tmpsqllist=[]
    day=tmpdaylist(days)
    # if type==1:
    tmpsql=r'SELECT data,create_time from job_log where create_time>'+'\''+day+'\''+' and create_time<\''+day+r''' 23:59:59' and job_id='''+'\''+job_id+'\''
    # print tmpsql
    tmpsqllist.append(tmpsql)
    (leftthreshold,rightthreshold)=mythreshold(job_id)
    return tmpsqllist,leftthreshold,rightthreshold
def mythreshold(jobid):
    if jobid=='44':
        return 90,100
    elif jobid=='45':
        return 0,1000
    elif jobid=='46':
        return 0,1000
    elif jobid=='47':
        return 10,100
    elif jobid=='48':
        return 0,10
def mydb(days,job_id):
    db = mysql.connect(host='123.59.17.246',user='egou_read',passwd='urm8cq9fey7gapnn',db='monitor',port=3306,charset='utf8')
    db.autocommit(True)
    c = db.cursor()
    sqllist=[]
    # 返回横坐标的数据 时间
    xcount=[]
    # 返回纵坐标 监控数据
    yclist=[]
    # 返回的数据 小时
    job_log,leftthreshold,rightthreshold=tmpsqllist(days,job_id)
    c.execute(job_log[0])
    # 返回监控数据
    orderresult=c.fetchall()
    for i in orderresult:
        xcount.append(str(i[1]))
        yclist.append(int(i[0]))
    tmpyclist=[]
    tmpdata={}
    for y in yclist:
        if int(y)>float(rightthreshold) or int(y)<float(leftthreshold):
            tmpdata={'y':int(y),
                     'marker':{'symbol':'url(http://www.highcharts.com/demo/gfx/snow.png)'}}
            tmpyclist.append(tmpdata)
        else:
            tmpyclist.append(int(y))
    db.close()
    print xcount,tmpyclist
    return xcount,tmpyclist,job_log
    # return '111'
if __name__ == '__main__':
    # mydb(2)

    print  tmpdaylist(0)



