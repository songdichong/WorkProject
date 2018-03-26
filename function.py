#coding=utf-8
'''
提供main.py中所需要的数据的计算方法
'''
import configure
import time
class recv(object):
	def intime_perc(self,total,relation,areacode=1):
		#默认areacode=1，即默认处理地级市的信息。
		adcd			=[total[i][0] for i in range(0,len(total))]
		recv_total		=[total[i][1] for i in range(0,len(total))]
		advan_total 	=[total[i][2] for i in range(0,len(total))]
		intime_total	=[total[i][3] for i in range(0,len(total))]
		later_total		=[total[i][4] for i in range(0,len(total))]
		laterlost_total	=[total[i][5] for i in range(0,len(total))]
		lost_total		=[total[i][6] for i in range(0,len(total))]
		if areacode==1:
			'''
			处理地市级(areacode=0)接受率,并直接输出城市对应的提前报，逾限，缺报（超时），缺报（未到）
			'''
			city_total=dict()
			for i in relation.values():
				if i not in city_total:
					city_total[i]=0
			recv_intime		=city_total.copy()
			recv_advan		=city_total.copy()
			recv_later		=city_total.copy()
			recv_laterlost	=city_total.copy()
			recv_lost		=city_total.copy()
			perc			=city_total.copy()
			for i in range(0,len(adcd)):
				city_total[relation[adcd[i]]]		+=recv_total[i]
				recv_advan[relation[adcd[i]]]		+=advan_total[i]
				recv_intime[relation[adcd[i]]]		+=intime_total[i]
				recv_later[relation[adcd[i]]]		+=later_total[i]
				recv_laterlost[relation[adcd[i]]]	+=laterlost_total[i]
				recv_lost[relation[adcd[i]]]		+=lost_total[i]
			for i in perc.keys():
				try:
					perc[i]=format((recv_intime[i]*1.0)/(city_total[i]*1.0),'0.4')
				except ZeroDivisionError:
					continue
			
			return perc,recv_advan,recv_intime,recv_later,recv_laterlost,recv_lost
		
		elif areacode==2:
			recv_advan=dict()
			recv_intime=dict()
			recv_later=dict()
			recv_laterlost=dict()
			recv_lost=dict()
			for i in relation:
				for j in range(0,len(adcd)):
					if i==adcd[j]:
						recv_advan[i]	=advan_total[j]
						recv_intime[i]	=intime_total[j]
						recv_later[i]	=later_total[j]
						recv_laterlost[i]=laterlost_total[j]
						recv_lost[i]	=lost_total[j]
			perc=recv_intime.copy()
			for i in perc.keys():
				try:
					perc[i]=format((recv_intime[i]*1.0)/((recv_advan[i]+recv_intime[i]+recv_later[i]+recv_laterlost[i]+recv_lost[i])*1.0),'0.4')
				except ZeroDivisionError:
					continue
			return perc,recv_advan,recv_intime,recv_later,recv_laterlost,recv_lost

class indb(object):	
	def indb_data(self,indb,relation,areacode=1):
		adcd		=[indb[i][0] for i in range(0,len(indb))]
		indb_min1	=[indb[i][1] for i in range(0,len(indb))]
		indb_min2	=[indb[i][2] for i in range(0,len(indb))]
		indb_min3	=[indb[i][3] for i in range(0,len(indb))]
		indb_min5	=[indb[i][4] for i in range(0,len(indb))]
		indb_min10	=[indb[i][5] for i in range(0,len(indb))]
		indb_minmax	=[indb[i][6] for i in range(0,len(indb))]
		indb_before	=[indb[i][7] for i in range(0,len(indb))]
		if areacode==1:
			'''
			处理地市级入库信息,并直接输出城市对应的1/3/5/10/最长分钟入库及提前入库
			'''
			city_total=dict()
			for i in relation.values():
				if i not in city_total:
					city_total[i]=0
			min1	=city_total.copy()
			min2	=city_total.copy()
			min3	=city_total.copy()
			min5	=city_total.copy()
			min10	=city_total.copy()
			minmax	=city_total.copy()
			before	=city_total.copy()
			for i in range(0,len(adcd)):
				min1[relation[adcd[i]]]+=indb_min1[i]
				min2[relation[adcd[i]]]+=indb_min2[i]
				min3[relation[adcd[i]]]+=indb_min3[i]
				min5[relation[adcd[i]]]+=indb_min5[i]
				min10[relation[adcd[i]]]+=indb_min10[i]
				minmax[relation[adcd[i]]]+=indb_minmax[i]
				before[relation[adcd[i]]]+=indb_before [i]
			return min1,min2,min3,min5,min10,minmax,before
		
		elif areacode==2:
			min1=dict()
			min2=dict()
			min3=dict()
			min5=dict()
			min10=dict()
			minmax=dict()
			before=dict()
			for i in relation:
				for j in range(0,len(adcd)):
					if i==adcd[j]:
						min1[i]	=indb_min1[j]
						min2[i]	=indb_min2[j]
						min3[i]	=indb_min3[j]
						min5[i]	=indb_min5[j]
						min10[i]=indb_min10[j]
						minmax[i]=indb_minmax[j]
						before[i]=indb_before[j]
			return min1,min2,min3,min5,min10,minmax,before

class send(object):	
	def send_data(self,send,relation,areacode=1):
		'''
		处理地市级发送信息,并直接输出城市对应的及时，提前报，逾限，缺报（超时），缺报（未发送）
		'''
		adcd			=[send[i][0] for i in range(0,len(send))]
		sendbefore		=[send[i][1] for i in range(0,len(send))]
		sendintime		=[send[i][2] for i in range(0,len(send))]
		sendlater		=[send[i][3] for i in range(0,len(send))]
		sendlaterlost	=[send[i][4] for i in range(0,len(send))]
		sendlost		=[send[i][5] for i in range(0,len(send))]
		if areacode==1:
			city_total=dict()
			for i in relation.values():
				if i not in city_total:
					city_total[i]=0
			send_before		=city_total.copy()
			send_intime		=city_total.copy()
			send_later		=city_total.copy()
			send_laterlost	=city_total.copy()
			send_lost		=city_total.copy()
			for i in range(0,len(adcd)):
				send_before[relation[adcd[i]]]+=sendbefore[i]
				send_intime[relation[adcd[i]]]+=sendintime[i]
				send_later[relation[adcd[i]]]+=sendlater[i]
				send_laterlost[relation[adcd[i]]]+=sendlaterlost[i]
				send_lost[relation[adcd[i]]]+=sendlost[i]
			return send_before,send_intime,send_later,send_laterlost,send_lost
			
		elif areacode==2:
			send_before	=dict()
			send_intime	=dict()
			send_later	=dict()
			send_laterlost=dict()
			send_lost	=dict()
			for i in relation:
				for j in range(0,len(adcd)):
					if i==adcd[j]:
						send_before[i]	=sendbefore[j]
						send_intime[i]	=sendintime[j]
						send_later[i]	=sendlater[j]
						send_laterlost[i]=sendlaterlost[j]
						send_lost[i]	=sendlost[j]
			return send_before,send_intime,send_later,send_laterlost,send_lost
def change_date(date,after):
	'''
	根据上一时次和下一时次改变日期时间
	arg: 	date:	用户选取的时间(format: yyyy-mm-dd hh:00:00)。
			after:	1代表上一时次，2代表下一时次。
	return: date:	改变后的时间（format: yyyy-mm-dd hh:00:00）。
	
	bug:闰年的2月没办法
	'''
	a=list(date)
	shi=str(a[11]+a[12])
	ri=str(a[8]+a[9])
	yue=str(a[5]+a[6])
	nian=str(a[0]+a[1]+a[2]+a[3])
	shijian=int(shi)
	riqi=int(ri)
	yuefen=int(yue)
	nianfen=int(nian)
	if after==1 or after==5:
		if shijian>0:
			shijian=shijian-1
		elif shijian==0 and riqi!=1:
			shijian=(shijian-1)%24
			riqi=riqi-1
		elif shijian==0 and riqi==1 and yuefen==1:
			shijian=(shijian-1)%24
			riqi=31
			yuefen=12
			nianfen=nianfen-1
		elif shijian==0 and riqi==1 and (yuefen in [2,4,6,8,9,11]):
			shijian=(shijian-1)%24
			riqi=31
			yuefen=yuefen-1
		elif shijian==0 and riqi==1 and (yuefen in [3,5,7,10,12]):
			shijian=(shijian-1)%24
			riqi=30
			yuefen=yuefen-1
		
	
	elif after==2 or after==6:
		if shijian<23:
			shijian=shijian+1
		elif shijian==23 and riqi!=(30 and 31) and yuefen!=2:
			riqi=riqi+1
			shijian=(shijian+1)%24
		elif shijian==23 and riqi==31 and yuefen==12:
			shijian=(shijian+1)%24
			riqi=1
			yuefen=1
			nianfen=nianfen+1
		elif shijian==23 and riqi==28 and yuefen==2:
			shijian=(shijian+1)%24
			riqi=1
			yuefen=yuefen+1
		elif shijian==23 and riqi==30 and yuefen in [4,6,8,9,11]:
			shijian=(shijian+1)%24
			riqi=1
			yuefen=yuefen+1
		elif shijian==23 and riqi==30 and yuefen in [1,3,5,7,8,10,12]:
			shijian=(shijian+1)%24
			riqi=riqi+1
		elif shijian==23 and riqi==31 and yuefen in [1,3,5,7,8,10]:
			shijian=(shijian+1)%24
			riqi=1
			yuefen=yuefen+1
			
	if shijian<10:
		a[11]='0'
		a[12]=str(shijian)
	else:
		a[11]=str(list(str(shijian))[0])
		a[12]=str(list(str(shijian))[1])
	
	if riqi<10:
		a[8]='0'
		a[9]=str(riqi)
	else:
		a[8]=str(list(str(riqi))[0])
		a[9]=str(list(str(riqi))[1])
	
	if yuefen<10:
		a[5]='0'
		a[6]=str(yuefen)
	else:
		a[5]=str(list(str(yuefen))[0])
		a[6]=str(list(str(yuefen))[1])
	a[0]=str(list(str(nianfen))[0])
	a[1]=str(list(str(nianfen))[1])
	a[2]=str(list(str(nianfen))[2])
	a[3]=str(list(str(nianfen))[3])
	date=''.join(a)
	return date

#~ if __name__=="__main__":
	#~ datatype='SURF@AWS_REG'
	#~ date='2017-07-26 07:00:00'
	#~ t1=time.time()
	#~ recv,indb,send = configure.aService().get_stat_info(datatype,date)
	#~ t2=time.time()
	#~ print ('t1:',t2-t1)
	#~ date='2017-12-31 00:00:00'
	#~ after=2
	#~ print change_date(date,after)
