#!/usr/bin/env python
#encoding: utf-8
from flask import Flask,jsonify,abort,Response
from flask import Flask,request,render_template
import os,json,sys
import houtai as ht
import reportdata as r
import tuodi_oneviw as tuodi_oneviw
import tuodi_day_order as myorder
import hdtmonitor as m
import hdt_cssc as cssc
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC_TXT = os.path.join(APP_ROOT, 'txt') #设置一个专门的类似全局变量的东西
app = Flask(__name__)
app.jinja_env.add_extension("chartkick.ext.charts")

@app.route('/monitor/yiqifahoutaif/<fname>', methods=['GET'])
def yiqifa_houtai1(fname):
    # filenanme='f1.txt'
    # print type(str(fname))
    fname=fname.encode('utf-8')
    # print type(fname)
    # print fname
    f=open('log/'+fname)
    s=f.readlines()
    f.closed
    return  render_template("file.html",user='aaa',title = 'Home',posts = s)
@app.route('/monitor/filelistok/', methods=['GET'])
def filelist():
    flist=ht.filelist(r'D:\work\auto\yiqifa\test_case\wending\log')
    print flist
    return render_template('flist.html',filelist=flist)
@app.route('/monitor/yiqifahoutai')
def yiqifahoutai():
    f=open('f1.txt')
    s=f.readlines()
    # yield '',.join(s)+'\n'
    # sorted(student_tuples, key=itemgetter(2), reverse=True)
    sorted(s,reverse=True)
    f.closed
    return  render_template("file.html",title = 'yiqifahoutai',posts = s)
@app.route('/monitor/error/<err_msg>')
def error(err_msg):
    # err_msg1=err_msg
    # return err_msg
    # print type(err_msg)
    err_msg=err_msg.encode('unicode-escape').decode('string_escape')
    # print type(err_msg)
    # print err_msg
    return render_template('error.html',err_msg1=err_msg)
# 托底广告
@app.route('/adtuodi1/<days>')
def adtuodi(days):
    title=u'托底'
    # xvalue=['Acccc','B','C','d']
    # dat=[1000,1200,1300,1000]
    xvalue,dat,tmpsqllist=r.mydb(days)
    # return "ttttttt"
    return render_template('highchartsline.html',xvalue=xvalue,title=title,data=dat,tmpsqllist=tmpsqllist)

# 托底广告订单按照时间分布
@app.route('/adtuodiorder/')
def adtuodiorder():
    title=u'托底订单按照时间分布'
    # xvalue=['Acccc','B','C','d']
    # dat=[1000,1200,1300,1000]
    day=request.args.get('day')
    order=request.args.get('order')
    xvalue,dat,tmpsqllist,adtuodi_order,adtuodi_order_count=myorder.mydb(int(day),int(order))
    # return "ttttttt%s，%s"%(str(day),str(order))
    return render_template('tuodi_day_order.html',xvalue=xvalue,title=title,data=dat,tmpsqllist=tmpsqllist,adtuodi_order=adtuodi_order,adtuodi_order_count=adtuodi_order_count)
# 按照广告主展示广告投放
@app.route('/ad_by_advertiser_id/')
def testhightchar():
    day=request.args.get('day')
    advertiser_id=request.args.get('advertiser_id')
    (xvalue,data,sql)=tuodi_oneviw.mydbnew(int(day),str(advertiser_id))
    print xvalue,data
    return render_template('ad_by_advertiser_id.html',xvalue=xvalue,d=data,sql=sql)
@app.route('/')
def index():
    print 'ok'
    return render_template("index.html")
@app.route('/summary/')
# 简介介绍
def summary():
    return render_template('summary.html')
@app.route('/flistok', methods=['GET'])
def flistok():
    path=r'd:'
    flist=os.walk(path)
    # return json.dumps(flist)
    print flist
    return render_template('flist.html',flist=flist)
# 互动推监控
@app.route('/hdtmonitor/',methods=['GET','POST'])
def hdtmonitor():
    if request.method=='GET':
        # print days
        return render_template('hdtmonitor.html')
    else:
        if request.form.get('myday')=='':
             days=0
        else:
            days=int(request.form.get('myday'))
        jobid=request.form.get('jobid')
        mytitle=''
        if jobid=='44':
            mytitle=u'展现/抽奖'
        # elif jobid=='45':
        #     mytitle=u'谢谢参与次'
        elif jobid=='46':
            mytitle=u'托底广告次数'
        elif jobid=='47':
            mytitle=u'点击/展现'
        elif jobid=='48':
            mytitle=u'负数个数/总个数'
        elif jobid=='45':
            mytitlemedia=u'谢谢参与数媒体分布'
            mytitle=u'谢谢参与次'
            xvaluemedia,datamedia=m.mymedia(days,'media_id','0')
            xvalue,dat,tmpsqllist=m.mydb(days,jobid)
            return render_template('hdtmonitor.html',xvalue=xvalue,mytitle=mytitle,data=dat,tmpsqllist=tmpsqllist,xvaluemedia=xvaluemedia,mytitlemedia=mytitlemedia,datamedia=datamedia)
        elif jobid=='100':
            mytitlemedia=u'媒体中广告位谢谢参与汇总'
            mediaid=str(request.form.get('mymediaid'))
            xvaluemedia,datamedia=m.mymedia(days,'adzone_id',mediaid)
            return render_template('hdtmonitor.html',xvaluemedia=xvaluemedia,mytitlemedia=mytitlemedia,datamedia=datamedia)

        xvalue,dat,tmpsqllist=m.mydb(days,jobid)
        return render_template('hdtmonitor.html',xvalue=xvalue,mytitle=mytitle,data=dat,tmpsqllist=tmpsqllist)
@app.route('/link/')
def link():
    return render_template('link.html')
@app.route('/hdt_cssc/',methods=['GET','POST'])
def hdt_cssc():
    if request.method=='GET':
        # alladzon=((59L, 101L, '172.16.145.55', 55L, None, 69L, 69L),(59L, 101L, '172.16.145.55', 55L, None, 69L, 69L))
        # for trcout in alladzon:
        #     print trcout
        return render_template('hdt_cssc.html')
    else:
        dbtype=request.form.get('dbtype')
        adzone_click_id=request.form.get('adzone_click_id')
        if request.form.get('myday')=='':
             days=0
        else:
            days=int(request.form.get('myday'))
        alladzon=cssc.mydata(days,dbtype,'adzon',adzone_click_id)
        alllottery=cssc.mydata(days,dbtype,'lottery',adzone_click_id)
        allshow=cssc.mydata(days,dbtype,'show',adzone_click_id)
        allclick=cssc.mydata(days,dbtype,'click',adzone_click_id)
        return render_template('hdt_cssc.html',alladzon=alladzon,alllottery=alllottery,allshow=allshow,allclick=allclick)
@app.route('/hdtapi/',methods=['GET','POST'])
def hdtapi():
    if request.method=='GET':
        print 1111111111
        return render_template('allapi.html')
    else:
        jobid=request.form.get('jobid')
        cmd='''python D:\\work\\auto\\Voyager\\all_tests.py'''
        # cmd='''python all_tests.py'''
        if jobid=='100':
            try:
                os.system(cmd)
            except Exception as e:
                print e.message
        return render_template('allapi.html')

if __name__ == '__main__':
    app.run( host="0.0.0.0",port=21312,debug=True)