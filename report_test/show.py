#!/usr/bin/env python
#encoding: utf-8
from flask import Flask,jsonify,abort,Response
from flask import Flask,request,render_template
import os,json
import houtai as ht
import reportdata as r
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
    # dat=[1000,1200,1300,1000,4000]
    xvalue,dat,tmpsqllist=r.mydb(days)
    # return "ttttttt"
    return render_template('highchartsline.html',xvalue=xvalue,title=title,data=dat,tmpsqllist=tmpsqllist)
@app.route('/index1')
def index():
  user = { 'nickname': 'Miguel' } # fake user
  posts = [ # fake array of posts
    {
      'author': { 'nickname': 'John' },
      'body': 'Beautiful day in Portland!'
    },
    {
      'author': { 'nickname': 'Susan' },
      'body': 'The Avengers movie was so cool!'
    }
  ]
  return render_template("index.html",
    title = 'Home',
    user = user,
    posts = posts)

@app.route('/flistok', methods=['GET'])
def flistok():
    path=r'd:'
    flist=os.walk(path)
    # return json.dumps(flist)
    print flist
    return render_template('flist.html',flist=flist)
if __name__ == '__main__':
    app.run( host="0.0.0.0",port=21312,debug=True)
