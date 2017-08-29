# encoding: utf-8
import requests,datetime,time,os
def login():
    param={'name':'test','pwd':'qq'}
    url='login/login_in.htm?'
    print url
    s=requests.session()
    s.get(url,params=param)
    # r=s.get('http://admin.adhudong.com:17071/user/ListUser.htm?username=coldman&status=1&descn=jack&create_time=1')
    return s
# 调用接口
def getcod(url):
    s=requests.session()
    jar = requests.cookies.RequestsCookieJar()
    jar.set('YQFJSESSIONID','8DC44EA9A30E4AE6868A0CDF1AC4B2BA',domain='221.122.127.41')
    try:
        r=s.get(url,cookies=jar, timeout=2)
    except Exception as e:
        return e
    return r.status_code
# 写文件
def writefile(t,url,code):
    f=open('f1.txt','a')
    f.write(t+','+url+','+code+'\n')
    f.closed
def wf(url):
    code=getcod(url)
    now=datetime.datetime.now()
    writefile(str(now),str(url),str(code))
    print str(now),str(url),str(code)+'\n'
def do():
     while 1==1:
        urllist=['http://221.122.127.41:19100/benefitlist.do','http://221.122.127.206:19100/benefitlist.do','http://221.122.127.63:19100/benefitlist.do','https://admin.yiqifa.com/benefitlist.do']
        for url in urllist:
            wf(url)
        time.sleep(5)

def filelist(path):
    return os.listdir(path)
if __name__ == '__main__':
    do()
    # while 1==1:
    #     urllist=['http://221.122.127.41:19100/benefitlist.do','http://221.122.127.206:19100/benefitlist.do','http://221.122.127.63:19100/benefitlist.do','https://admin.yiqifa.com/benefitlist.do']
    #     for url in urllist:
    #         wf(url)
    #     time.sleep(5)


