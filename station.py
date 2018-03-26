#coding=utf-8
import urllib2
import json
import time
def station_machine(url):
	station=dict()
	content=urllib2.urlopen(url)
	neirong=content.read()
	data=eval(neirong)
	for i in data.keys():
		station[i]=(data[i]['machine'])
	return station
	
#~ if __name__=="__main__":
	#~ t1=time.time()
	#~ url='http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json'
	#~ a=station_machine(url)
	#~ t2=time.time()
	#~ print t2-t1
	#~ print a
