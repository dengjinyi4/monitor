    #encoding:utf-8
import MySQLdb as mysql,time,datetime

def tmpday(days):
    # daylist=[]
    d = datetime.datetime.now()
    # for i in range(0,int(days)):
    tmpdate_from=d+datetime.timedelta(days=-days)
    tmpdate_from=str(tmpdate_from)[0:10].replace('-','')
        # daylist.append(tmpdate_from)
        # daylist.sort()
    return tmpdate_from
def mydbnew1():
    db = mysql.connect(host='221.122.127.183',user='voyager',passwd='voyager',db='voyager',port=5701,charset='utf8')
    db.autocommit(True)
    myc = db.cursor()
    days=tmpday(1)
    sql='''UPDATE voyager.ctr_log SET ctr_time='''+days+''' where ctr_key='adzone_101' ORDER BY create_time DESC LIMIT 1 ;'''
    print sql
    myc.execute(sql)
    myc.close()
    db.close()
    # return 1
    return 1

if __name__ == '__main__':
    mydbnew1()
    # print y





