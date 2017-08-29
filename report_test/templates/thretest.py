#coding=utf-8
import threading,time,datetime
from time import ctime,sleep


def music(func):
    j=0
    while True:
        print j
        j=j+1
        time.sleep(1)
    #
    # i=0
    # for i in range(3):
    #     print "I was listening to %s. %s" %(func,ctime())
    #     print '\n'
    #     sleep(1)

def move(func):
    for i in range(5):
        print "I was at the %s! %s" %(func,ctime())
        sleep(5)

threads = []
t1 = threading.Thread(target=music,args=(u'爱情买卖',))
threads.append(t1)
t2 = threading.Thread(target=move,args=(u'阿凡达',))
threads.append(t2)

def do():
    for t in threads:
        t.setDaemon(True)
        t.start()
        t.join()
    # t.join()
def filename():
    now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    a = '2016-09-18'
    a_ = datetime.datetime.strptime(a,'%Y-%M-%d')
    b_ = datetime.datetime.strptime(now,'%Y-%M-%d')
    c = b_ - a_
    print c.days
    # if (time.mktime('2017-8-15')>time.mktime(t)):
    #     print '大于当天'
    # else:
    #     print '小于 当天'
    # filename = 'log/log%s.txt' %(t)
    # fp = file(filename, 'wb')
    # f=open(filename,'a')
    # f.write('test')
if __name__ == '__main__':
    filename()
    # while  True: