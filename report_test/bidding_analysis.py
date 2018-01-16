#!/usr/bin/env python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
from collections import Counter
from elasticsearch import Elasticsearch
# 对未出的广告订单进行汇总
def getorderreson(mydit):
    # mydit={"6350":"Q","8894":"B","8891":"B","8892":"B","8777":"K","8895":"B","9061":"L","9062":"Y","9065":"B","8098":"M","8890":"B","9063":"Y","9064":"K","8090":"L","8648":"K","8526":"B","8768":"B","8889":"L","8783":"K","8781":"K","9078":"K","8782":"K","9079":"K","8664":"Q","8665":"D","9072":"B","9073":"B","9071":"K","9076":"K","9077":"L","9074":"K","9075":"K","8537":"A","8658":"B","8779":"K","5041":"B","8673":"A","8552":"B","8674":"Y","7343":"L","8671":"Y","8672":"Y","8793":"D","8675":"Y","7346":"L","8676":"Y","8670":"K","6491":"A","9080":"L","5956":"K","8326":"K","8323":"B","7903":"K","8332":"M","8572":"A","8457":"K","8578":"A","8214":"K","8577":"A","8570":"B","8450":"A","8448":"Q","5979":"L","6168":"A","8588":"B","6169":"Q","8596":"A","8475":"B","8352":"K","8593":"Q","8907":"L","8908":"K","8901":"Y","8902":"M","8349":"B","8905":"L","8906":"K","8903":"L","8904":"B","8363":"F","8483":"K","8918":"K","8919":"M","8912":"B","8917":"B","8914":"K","8135":"K","8374":"B","8495":"L","8375":"B","8930":"K","8810":"L","8378":"K","8258":"Q","8252":"K","8370":"B","8491":"B","8371":"K","8809":"D","8924":"K","8921":"A","8801":"B","8806":"A","8805":"L","8264":"M","8028":"B","8821":"B","8027":"B","8384":"K","8936":"B","8937":"Q","8036":"B","9004":"B","9002":"L","9007":"K","8832":"L","9008":"Q","8950":"B","9005":"K","7742":"B","8830":"B","9006":"A","8031":"K","8032":"A","8709":"B","414":"A","415":"A","416":"A","5798":"B","417":"A","5799":"B","418":"A","9014":"Q","8960":"A","9015":"Q","7992":"K","9012":"Q","9013":"Q","8963":"B","8722":"K","8961":"A","9010":"Q","9011":"A","421":"A","422":"A","423":"A","7747":"B","9009":"Q","8713":"Q","8955":"B","7746":"B","7867":"K","7627":"B","7748":"B","8716":"A","8717":"A","8959":"B","8838":"K","8299":"B","8850":"B","8971":"K","8851":"B","8972":"K","8292":"B","8847":"B","6548":"Q","8602":"B","8965":"B","8845":"B","6547":"Q","8849":"B","8860":"B","8069":"B","8864":"L","8502":"B","8744":"Q","8865":"L","8862":"Q","8863":"A","9039":"B","9030":"B","8614":"B","8735":"B","8750":"B","9047":"B","9048":"B","9046":"B","8512":"B","8997":"D","9049":"B","8511":"B","9040":"A","9041":"A","9042":"K","8868":"B","7777":"K","8503":"B","8745":"A","8746":"Q","8749":"A","9058":"K","8520":"B","9059":"L","9056":"A","8880":"K","9057":"A","7796":"B","8523":"B","8524":"B","8521":"B","8522":"B","9050":"B","9051":"B","8081":"M","9054":"A","9055":"A","9052":"M","9053":"Q","8637":"B","8759":"B","8756":"K","8519":"B"}
    orderreson={"A":"同一用户cookie24小时内重复展现","B":"订单无效或当前时间不可投放","C":"今日没有预算","D":"预算已不足","E":"投放状态错误（冻结或暂停或结束）","F":"出价过低","G":"订单对应广告主无效或状态错误","H":"订单对应广告计划无效或错误","I":"被此广告位定向过滤过滤","J":"被此广告位URL定向过滤","K":"该订单过滤该广告位媒体","L":"被订单的地域限制过滤","M":"被订单的设备限制过滤","N":"被用户频次限制过滤","O":"坑位类型不匹配","P":"没有广告着陆页地址","Q":"广告链接重复","R":"广告着陆页域名被封","S":"广告图片相似","T":"创意无效或状态错误","U":"被广告位次配置过滤","V":"没有小时预算","W":"小时预算不足","X":"广告位和广告创意等级不匹配","Y":"隐藏过滤时间","Z":"隐藏过滤地域","a":"广告订单媒体资质定向不符","b":"广告订单媒体广告位定向不符"}
    # 分组未出订单原因 字典
    count=Counter(mydit.values())
    print count
    # 相同原因未出广告订单列表
    orderlist=[]
    alldit={}
    for (j,k) in count.items():
        for(mykey,myv) in mydit.items():
            if myv==j:
                orderlist.append(mykey)
        alldit[j]=orderlist
        orderlist=[]
    # 与错误原因的字典进行匹配替换key值
    for (j,k) in alldit.items():
        for (rj,rk) in orderreson.items():
            if j==rj:
                alldit[rk]=alldit.pop(j)
    return json.dumps(alldit, encoding='UTF-8', ensure_ascii=False)
# 根据点击id查询出所有的过滤原因的订单
def orderbylog(zclk):
    es=Elasticsearch([{"host":"221.122.127.41"}],port=9200);
    # res = es.search(index="logstash-voyagerjavalog-*", body={"query": {"zclk":"B3J3JDC11HP5D1KDOM"}, "_source": "BID_INFO"})
    body={
	"sort": {
		"@timestamp": "desc"
	},
	"size": 13,
	"query": {
		"bool": {
			"must": [{
				"query_string": {
					"query": "\"B0H3CDC01HQJHIYMTD\"",
					"analyze_wildcard": True
				}}]}}}
    body['query']["bool"]['must'][0]['query_string']['query']='path:bidding  AND message:"{0}"'.format(zclk)
    print body
    res = es.search(index="logstash-voyagerjavalog-*", body=body)
    # print res
    tmplist=[]
    tmpwadlist=[]
    tmpdict={}
    for hit in res["hits"]["hits"]:
        print 5555555555555555555555555555
        tmpwad=str(hit["_source"]["message"][0]).split("bid:")[1].split(", wad:")[1]
        # 不出广告订单列表
        tmpdit=str(hit["_source"]["message"][0]).split("bid:")[1].split(", wad:")[0].split("fad:")[1]
        tmpdit=eval(tmpdit)
        tmpdict[tmpwad]=tmpdit
        tmplist.append(tmpdict)
    return tmplist

# 根据点击id查询出所有的过滤原因的订单
def orderbylognew(zclk):
    es=Elasticsearch([{"host":"221.122.127.41"}],port=9200);
    # res = es.search(index="logstash-voyagerjavalog-*", body={"query": {"zclk":"B3J3JDC11HP5D1KDOM"}, "_source": "BID_INFO"})
    body={
	"sort": {
		"@timestamp": "desc"
	},
	"size": 3,
	"query": {
		"bool": {
			"must": [{
				"query_string": {
					"query": "\"B0H3CDC01HQJHIYMTD\"",
					"analyze_wildcard": True
				}}]}}}
    body['query']["bool"]['must'][0]['query_string']['query']='path:bidding  AND message:"{0}"'.format(zclk)
    # print body
    res = es.search(index="logstash-voyagerjavalog-*", body=body)
    tmplist=[]
    for hit in res["hits"]["hits"]:
        tmpdict={}

        # print hit
        # print 5555555555555555555555555555
        # 时间
        mytime=str(hit["_source"]["message"])[3:22]
        # 筛选条件
        bid=str(hit["_source"]["message"]).split("bid:")[1].split(", tad:")[0]
        # 选出来的订单列表
        tad=str(hit["_source"]["message"]).split("tad:[")[1].split("], fad:")[0]
        #选出来的订单
        tmpwad=str(hit["_source"]["message"]).split("}, wad:")[1].split("'")[0]
        # print 77777777777777777777
        # print tmpwad
	# print 222222
        # 不出广告订单列表
        tmpdit=str(hit["_source"]["message"]).split("bid:")[1].split(", wad:")[0].split("fad:")[1]
        tmpdit=eval(tmpdit)
        tmpdict["wad"]=tmpwad
        tmpdict["fad"]=eval(getorderreson(tmpdit))
        tmpdict["mytime"]=mytime
        tmpdict["bid"]=eval(bid)
        tmpdict["tad"]=tad.split(",")
        tmplist.append(tmpdict)
    return tmplist


if __name__ == '__main__':
    # mydit={"6350":"Q","8894":"B","8891":"B","8892":"B","8777":"K","8895":"B","9061":"L","9062":"Y","9065":"B","8098":"M","8890":"B","9063":"Y","9064":"K","8090":"L","8648":"K","8526":"B","8768":"B","8889":"L","8783":"K","8781":"K","9078":"K","8782":"K","9079":"K","8664":"Q","8665":"D","9072":"B","9073":"B","9071":"K","9076":"K","9077":"L","9074":"K","9075":"K","8537":"A","8658":"B","8779":"K","5041":"B","8673":"A","8552":"B","8674":"Y","7343":"L","8671":"Y","8672":"Y","8793":"D","8675":"Y","7346":"L","8676":"Y","8670":"K","6491":"A","9080":"L","5956":"K","8326":"K","8323":"B","7903":"K","8332":"M","8572":"A","8457":"K","8578":"A","8214":"K","8577":"A","8570":"B","8450":"A","8448":"Q","5979":"L","6168":"A","8588":"B","6169":"Q","8596":"A","8475":"B","8352":"K","8593":"Q","8907":"L","8908":"K","8901":"Y","8902":"M","8349":"B","8905":"L","8906":"K","8903":"L","8904":"B","8363":"F","8483":"K","8918":"K","8919":"M","8912":"B","8917":"B","8914":"K","8135":"K","8374":"B","8495":"L","8375":"B","8930":"K","8810":"L","8378":"K","8258":"Q","8252":"K","8370":"B","8491":"B","8371":"K","8809":"D","8924":"K","8921":"A","8801":"B","8806":"A","8805":"L","8264":"M","8028":"B","8821":"B","8027":"B","8384":"K","8936":"B","8937":"Q","8036":"B","9004":"B","9002":"L","9007":"K","8832":"L","9008":"Q","8950":"B","9005":"K","7742":"B","8830":"B","9006":"A","8031":"K","8032":"A","8709":"B","414":"A","415":"A","416":"A","5798":"B","417":"A","5799":"B","418":"A","9014":"Q","8960":"A","9015":"Q","7992":"K","9012":"Q","9013":"Q","8963":"B","8722":"K","8961":"A","9010":"Q","9011":"A","421":"A","422":"A","423":"A","7747":"B","9009":"Q","8713":"Q","8955":"B","7746":"B","7867":"K","7627":"B","7748":"B","8716":"A","8717":"A","8959":"B","8838":"K","8299":"B","8850":"B","8971":"K","8851":"B","8972":"K","8292":"B","8847":"B","6548":"Q","8602":"B","8965":"B","8845":"B","6547":"Q","8849":"B","8860":"B","8069":"B","8864":"L","8502":"B","8744":"Q","8865":"L","8862":"Q","8863":"A","9039":"B","9030":"B","8614":"B","8735":"B","8750":"B","9047":"B","9048":"B","9046":"B","8512":"B","8997":"D","9049":"B","8511":"B","9040":"A","9041":"A","9042":"K","8868":"B","7777":"K","8503":"B","8745":"A","8746":"Q","8749":"A","9058":"K","8520":"B","9059":"L","9056":"A","8880":"K","9057":"A","7796":"B","8523":"B","8524":"B","8521":"B","8522":"B","9050":"B","9051":"B","8081":"M","9054":"A","9055":"A","9052":"M","9053":"Q","8637":"B","8759":"B","8756":"K","8519":"B"}
    # mydit={"8893":"B","9102":"D","6350":"D","8894":"B","8135":"K","9100":"D","9189":"D","7202":"K","8930":"D","7201":"K","8777":"D","8810":"L","6871":"K","8895":"B","8896":"K","9105":"D","9061":"L","9182":"L","9183":"B","9180":"L","9181":"L","9186":"L","9066":"D","8098":"B","9187":"L","8252":"K","8370":"B","9184":"K","8371":"B","9064":"K","8090":"K","8922":"D","8526":"B","8768":"B","8889":"L","8805":"L","8783":"D","8781":"D","9199":"K","8782":"D","8661":"B","8028":"B","8821":"K","8268":"K","8664":"D","8027":"K","8665":"D","9193":"D","9194":"D","9191":"D","9192":"K","8384":"K","9077":"L","9198":"B","8260":"M","9195":"B","9196":"B","9190":"K","8658":"K","8779":"D","8937":"D","8673":"D","9004":"B","8036":"B","7343":"L","8671":"Y","9002":"B","8672":"Y","8793":"D","9007":"K","8798":"B","8435":"B","8832":"K","9008":"D","9129":"K","9005":"K","8830":"B","9083":"D","9084":"B","8270":"K","9081":"L","9082":"L","7180":"K","9087":"L","8031":"K","8670":"K","9088":"K","8032":"D","9121":"L","9085":"L","6491":"B","9086":"D","5956":"K","9014":"D","9015":"D","9012":"D","7199":"K","9013":"D","8601":"B","8961":"D","9098":"D","9010":"D","9099":"D","9011":"D","9096":"L","7196":"D","9090":"B","9091":"K","8318":"B","9009":"D","8438":"K","8713":"D","8955":"K","7867":"K","7903":"K","8716":"D","8959":"B","8717":"D","8332":"D","8850":"B","8851":"B","8214":"K","8292":"B","8605":"B","6548":"B","6547":"B","8860":"B","9036":"K","8864":"K","6168":"D","8502":"B","8865":"K","9039":"B","6169":"D","8588":"B","9154":"L","9030":"K","8735":"B","8856":"K","8614":"B","9168":"K","8596":"K","9169":"D","9048":"B","9166":"B","8352":"K","9167":"B","9046":"B","8512":"B","8997":"B","8755":"B","8598":"K","8511":"B","9165":"K","8593":"K","9162":"B","8908":"K","8901":"B","7777":"K","8869":"B","8902":"B","8229":"B","8906":"K","9058":"K","8640":"B","8520":"B","9059":"L","8880":"B","9177":"B","8363":"F","9178":"B","7796":"K","8523":"B","8524":"B","8521":"B","8885":"K","8522":"B","9171":"K","9050":"B","9172":"D","9170":"D","9175":"K","9176":"B","8483":"K","9173":"K","9174":"K","8918":"K","8919":"K","8912":"B","8917":"K","8519":"B"}
    tmpdit=orderbylognew('B0H2UDC01HQNFDNXUP')
    # for i in tmpdit:
    #     print i['tad']
    # print tmpdit
    # print type(tmpdit[0])
    # print type(tmpdit[0]["wad"])
    # print type(tmpdit[0]["fad"])
    # print type(tmpdit[0]["mytime"])
    # print type(tmpdit[0]["bid"])
    # print type(tmpdit[0]["tad"])
    # print type(tmpdit['tad'])


    # tmpalldict={}
    # for i in tmpdit:
    #     for (j,k) in i.items():
    #         # print j
    #         # print getorderreson(k)
    #         tmpalldict[j]=getorderreson(k)
    # print tmpalldict


        # print getorderreson(i)

