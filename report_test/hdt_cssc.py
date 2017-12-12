#encoding:utf-8
import MySQLdb as mysql,time,datetime

def tmpdaylist(days):
    daylist=''
    d = datetime.datetime.now()
    tmpdate_from=d+datetime.timedelta(days=-int(days))
    tmpdate_from=str(tmpdate_from)[0:10].replace('-','')
    # daylist.append(tmpdate_from)
    # daylist.sort()
    daylist=tmpdate_from
    return daylist
# 返回包含日期的sql
def tmpsqllist(days,type,adzone_click_id):
    day=tmpdaylist(days)
    tmpsqllist=[]
    if type=='adzon':
        tmpsql="SELECT act_id,adzone_id,ip,region,media_id,master_id,status,adzone_click_id from voyagerlog.adzone_click_log"+day+" where adzone_click_id='"+adzone_click_id+"'"
    elif type=='lottery':
        tmpsql="SELECT award_id,order_id,act_id,adzone_id,media_id,ip,region,act_award_type,ad_creative_id,plan_id,award_name,choosen_tag,advertiser_id from voyagerlog.lottery_click_log"+day+" where adzone_click_id='"+adzone_click_id+"'"
    elif type=='show':
        tmpsql="SELECT ad_choosen_tag,media_id,adzone_id,act_id,position_id,ad_plan_id,ad_order_id,ad_creative_id,advertiser_id from voyagerlog.ad_show_log"+day+" where adzone_click_id='"+adzone_click_id+"'"
    elif type=='click':
        tmpsql="SELECT media_id,adzone_id,act_id,position_id,ad_plan_id,ad_order_id,ad_creative_id,charge_amount,advertiser_id,occurrence,status,click_source,invalid_message from voyagerlog.ad_click_log"+day+" where adzone_click_id='"+adzone_click_id+"'"
    # tmpsqllist.append(tmpsql)
    print tmpsql
    return tmpsql
def mycursor(type):
    if type=='test':
        db = mysql.connect(host='221.122.127.183',user='voyager',passwd='voyager',db='voyagerlog',port=5701,charset='utf8')
    else:
        db = mysql.connect(host='123.59.17.121',user='voyager',passwd='SIkxiJI5r48JIvPh',db='voyagerlog',port=3306,charset='utf8')
    db.autocommit(True)
    c = db.cursor()
    return c

def mydata(days,dbtype,tabletype,adzone_click_id):
    c=mycursor(dbtype)
    ordersql=tmpsqllist(days,tabletype,adzone_click_id)
    c.execute(ordersql)
    result=c.fetchall()
    c.close()
    return result
    # return '111'
if __name__ == '__main__':
    myc=mycursor('test1')
    sql=r"SELECT create_time  from voyagerlog.lottery_click_log20171121 where adzone_click_id='B0H2DDC11HKH9UK4N6';"
    myc.execute(sql)
    re=myc.fetchall()
    count=[]
    for i in range(1,len(re)):
        a=re[i][0]-re[i-1][0]
        count.append(a.seconds)
    print count
    # print count[0].seconds
    # print len(re)
    # print type(re[1][0])
    # print re[1][0]-re[0][0]




