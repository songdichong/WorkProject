#coding=utf-8
from flask import Flask,render_template,jsonify,request,session
from flask_bootstrap import Bootstrap
import configure
import function
import station
import datetime
import time #用来优化运行速度
app=Flask(__name__)

def rearrange(city):
	'''
	按照对应地区格式整理数据（和城市对应）
	arg: 	city,		格式{城市编号：接受/入库/传输率}
	return:	new_city,	格式{城市名称：接受/入库/传输率}
	'''
	guanxi=configure.aService().translate()
	new_city=dict()
	for i in city.keys():
		new_city[guanxi[i]]=city[i]
	return new_city
		
def getkey(relation,city):
	return [k for k, v in relation.items() if v==city]

def find_datatype(x):
	'''
	对datatype提供解码格式
	
	todo:二级列表
	'''
	if x=='0':
		return 'SURF@AWS_NAT'
	elif x=='1':
		return 'SURF@AWS_REG'
	elif x=='2':
		return 'SURF@AWS_RD'
	elif x=='3':
		return 'SURF@AWS_UNAT'
	elif x=='4':
		return 'SURF@AWS_PRF'
	elif x=='5':
		return 'SURF@AWS_SS'
	elif x=='6':
		return 'RADA@O_DOR'
	elif x=='7':
		return 'RADA@P_R_10_230_5'
	elif x=='8':
		return 'RADA@P_R_10_230_15'
	elif x=='9':
		return 'RADA@P_R_10_230_24'
	elif x=='10':
		return 'RADA@P_R_10_230_34'
	elif x=='11':
		return 'RADA@P_R_10_230_43'
	elif x=='12':
		return 'RADA@P_R_10_230_60'
	elif x=='13':
		return 'RADA@P_R_10_460_5'
	elif x=='14':
		return 'RADA@P_R_10_460_15'
	elif x=='15':
		return 'RADA@P_R_10_460_24'
	

	
def return_title(date):
	a=list(date)
	nian=str(a[0]+a[1]+a[2]+a[3])
	yue=str(a[5]+a[6])
	ri=str(a[8]+a[9])
	shi=str(a[11]+a[12])
	title=nian+'年'+yue+'月'+ri+'日'+shi+'时（世界时）'
	return title
	
def find_sum(x):
	a=0
	for i in x:
		a+=i
	x.append(a)
	return x
	
	
@app.route('/',methods=['GET','POST'])
def index():
	return render_template('base.html')
	
@app.route('/jieshou',methods=['GET','POST'])
def jieshou():
	if request.method == "POST":
		#从session获取数据判断是否需要重新查询（查一次就要2秒）
		old_date=session.get('date')
		old_datatype=session.get('datatype')
		#从前端获取数据
		date=request.form['riqi[0][value]'].encode('utf-8')
		after=request.form['button'].encode('utf-8')
		after=int(after)
		#有没有点上一/下一时次
		if (after!=0):
			date=function.change_date(date,after)
		datatype=request.form['riqi[1][value]'].encode('utf-8')
		datatype=find_datatype(datatype)
		if old_date!=date or old_datatype!=datatype:
			session['datatype']=datatype
			session['date']=date
			try:
				recv,indb,send= configure.aService().get_stat_info(datatype,date)
				session['recv']=recv
				session['indb']=indb
				session['send']=send
			#print session
			except Exception:
				#错误，无内容
				return render_template('jieshou.html')
			
		if after!=3:
			recv=session.get('recv')
			indb=session.get('indb')
			send=session.get('send')
			relation=configure.aService().get_area_info()
			#print('zheli3')
			
			#接收
			jieshou,recv_advan,recv_intime,recv_later,recv_laterlost,recv_lost=function.recv().intime_perc(recv,relation)
			jieshou=rearrange(jieshou)
			recv_advan=rearrange(recv_advan)
			recv_intime=rearrange(recv_intime)
			recv_later=rearrange(recv_later)
			recv_laterlost=rearrange(recv_laterlost)
			recv_lost=rearrange(recv_lost)
			area=[i.decode('utf-8') for i in jieshou.keys()]
			jieshoulv	=[i for i in jieshou.values()]
			jieshou_tiqian	=[i for i in recv_advan.values()]
			jieshou_zhunshi	=[i for i in recv_intime.values()]
			jieshou_yuxian	=[i for i in recv_later.values()]
			jieshou_chaoshi	=[i for i in recv_laterlost.values()]
			jieshou_weidao	=[i for i in recv_lost.values()]
			
			area.append('江西省')
			jieshou_tiqian=find_sum(jieshou_tiqian)
			jieshou_zhunshi=find_sum(jieshou_zhunshi)
			jieshou_yuxian=find_sum(jieshou_yuxian)
			jieshou_chaoshi=find_sum(jieshou_chaoshi)
			jieshou_weidao=find_sum(jieshou_weidao)
			

			#入库
			min1,min2,min3,min5,min10,minmax,before=function.indb().indb_data(indb,relation)
			min1=rearrange(min1)
			min2=rearrange(min2)
			min3=rearrange(min3)
			min5=rearrange(min5)
			min10=rearrange(min10)
			minmax=rearrange(minmax)
			before=rearrange(before)
			min_1	= [i for i in min1.values()]
			min_2	= [i for i in min2.values()]
			min_3	= [i for i in min3.values()]
			min_5	= [i for i in min5.values()]
			min_10	= [i for i in min10.values()]
			min_max	= [i for i in minmax.values()]
			tiqianruku	= [i for i in before.values()]
			min_1=find_sum(min_1)
			min_2=find_sum(min_2)
			min_3=find_sum(min_3)
			min_5=find_sum(min_5)
			min_10=find_sum(min_10)
			min_max=find_sum(min_max)
			tiqianruku=find_sum(tiqianruku)
			
			#发送
			send_before,send_intime,send_later,send_laterlost,send_lost=function.send().send_data(send,relation)
			send_before=rearrange(send_before)
			send_intime=rearrange(send_intime)
			send_later=rearrange(send_later)
			send_laterlost=rearrange(send_laterlost)
			send_lost=rearrange(send_lost)
			
			fasong_tiqian	= [i for i in send_before.values()]
			fasong_zhunshi	= [i for i in send_intime.values()]
			fasong_yuxian	= [i for i in send_later.values()]
			fasong_chaoshi	= [i for i in send_laterlost.values()]
			fasong_weidao	= [i for i in send_lost.values()]
			
			fasong_tiqian=find_sum(fasong_tiqian)
			fasong_zhunshi=find_sum(fasong_zhunshi)
			fasong_yuxian=find_sum(fasong_yuxian)
			fasong_chaoshi=find_sum(fasong_chaoshi)
			fasong_weidao=find_sum(fasong_weidao)
			title=return_title(date)
			return jsonify(shuju_type='0',riqi=date,title=title,
			area=area,jieshoulv=jieshoulv,jieshou_tiqian=jieshou_tiqian,
			jieshou_zhunshi=jieshou_zhunshi,jieshou_yuxian=jieshou_yuxian,
			jieshou_chaoshi=jieshou_chaoshi,jieshou_weidao=jieshou_weidao,#接收
			min_1=min_1,min_2=min_2,min_3=min_3,min_5=min_5,min_10=min_10,
			min_max=min_max,tiqianruku=tiqianruku,#入库
			fasong_tiqian=fasong_tiqian,fasong_zhunshi=fasong_zhunshi,
			fasong_yuxian=fasong_yuxian,fasong_chaoshi=fasong_chaoshi,
			fasong_weidao=fasong_weidao,#发送
			)
			
		elif after==3:
			recv=session.get('recv')
			indb=session.get('indb')
			send=session.get('send')

			city=request.form['city'].encode('utf-8')
			city_relation=configure.aService().translate()
			city_adcd=getkey(city_relation,city)[0]
			town_relation=configure.aService().get_area_info()
			town_adcd=getkey(town_relation,city_adcd)
			#print town_adcd
			#接收
			perc,recv_advan,recv_intime,recv_later,recv_laterlost,recv_lost=function.recv().intime_perc(recv,town_adcd,2)
			perc=rearrange(perc)
			recv_advan=rearrange(recv_advan)
			recv_intime=rearrange(recv_intime)
			recv_later=rearrange(recv_later)
			recv_laterlost=rearrange(recv_laterlost)
			recv_lost=rearrange(recv_lost)
			area=[i.decode('utf-8') for i in recv_advan.keys()]
			jieshoulv		=[i for i in perc.values()]
			jieshou_tiqian	=[i for i in recv_advan.values()]
			jieshou_zhunshi	=[i for i in recv_intime.values()]
			jieshou_yuxian	=[i for i in recv_later.values()]
			jieshou_chaoshi	=[i for i in recv_laterlost.values()]
			jieshou_weidao	=[i for i in recv_lost.values()]
			
			#入库
			min1,min2,min3,min5,min10,minmax,before=function.indb().indb_data(indb,town_adcd,2)
			min1=rearrange(min1)
			min2=rearrange(min2)
			min3=rearrange(min3)
			min5=rearrange(min5)
			min10=rearrange(min10)
			minmax=rearrange(minmax)
			before=rearrange(before)
			min_1	= [i for i in min1.values()]
			min_2	= [i for i in min2.values()]
			min_3	= [i for i in min3.values()]
			min_5	= [i for i in min5.values()]
			min_10	= [i for i in min10.values()]
			min_max	= [i for i in minmax.values()]
			tiqianruku	= [i for i in before.values()]
			
			#发送
			send_before,send_intime,send_later,send_laterlost,send_lost=function.send().send_data(send,town_adcd,2)
			send_before=rearrange(send_before)
			send_intime=rearrange(send_intime)
			send_later=rearrange(send_later)
			send_laterlost=rearrange(send_laterlost)
			send_lost=rearrange(send_lost)
			
			fasong_tiqian	= [i for i in send_before.values()]
			fasong_zhunshi	= [i for i in send_intime.values()]
			fasong_yuxian	= [i for i in send_later.values()]
			fasong_chaoshi	= [i for i in send_laterlost.values()]
			fasong_weidao	= [i for i in send_lost.values()]
			
			return jsonify(area=area,jieshoulv=jieshoulv,shuju_type='0',
			jieshou_tiqian=jieshou_tiqian,jieshou_zhunshi=jieshou_zhunshi,
			jieshou_yuxian=jieshou_yuxian,jieshou_chaoshi=jieshou_chaoshi,jieshou_weidao=jieshou_weidao,
			min_1=min_1,min_2=min_2,min_3=min_3,min_5=min_5,min_10=min_10,
			min_max=min_max,tiqianruku=tiqianruku,#入库
			fasong_tiqian=fasong_tiqian,fasong_zhunshi=fasong_zhunshi,
			fasong_yuxian=fasong_yuxian,fasong_chaoshi=fasong_chaoshi,
			fasong_weidao=fasong_weidao,#发送
			)
			
	print ('zheli3')
	return render_template('jieshou.html')	
	
def return_area(stationum):
	areacode=configure.aService().get_areacode(stationum)
	station_name=areacode[0]
	city_name	=areacode[1]
	country_name=areacode[2]
	return station_name,city_name,country_name
	
@app.route('/tiqian',methods=['GET','POST'])
def tiqian():
	if request.method == "POST":
		#从前端获取数据
		date=request.form['datetime'].encode('utf-8')#时段查询时为starttime
		shijian=request.form['shijian'].encode('utf-8')
		shijian=int(shijian)
		if shijian==0:
			endtime=date
		elif shijian==1:
			endtime=request.form['endtime'].encode('utf-8')
				
		try:
			#检验时间格式是否合法
			date_format='%Y-%m-%d %H:00:00'
			examine_date=datetime.datetime.strptime(date, date_format)
		except Exception:
			app.logger.error('invalid time')
			return render_template('tiqian.html')

		xinxi=request.form['xinxi'].encode('utf-8')
		xinxi=int(xinxi)
		datatype=request.form['datatype'].encode('utf-8')#总是查询区域站(即1)
		after=request.form['button'].encode('utf-8')
		after=int(after)
		#分析需要的datatype
		datatype=find_datatype(datatype)
		#有没有点上一/下一时次
		if (after!=4):
			date=function.change_date(date,after)
		#~ t0=time.time()
		try:
			#err:有问题的站点信息
			err= configure.aService().get_station_info(datatype,date,endtime,xinxi)
		except Exception:
			#错误，重新载入
			return render_template('tiqian.html')
		#~ t1=time.time()
		#~ print 't0',t1-t0
		#这里是希望加快运行速度，于是在网页上保存了zhandian和areainfo两个cookies。一般情况下oldurl==url。
		url='http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json'
		zhandian=station.station_machine(url)
		areainfo=configure.aService().get_all_areacode()
		#zhandain={站点编号：机器型号}
		#areainfo={站点编号:(站点名称，城市名称，区县名称)}
		#~ print session
		#~ print err
		#~ t2=time.time()
		#~ print 't1',t2-t1
		tiqian=dict()
		if shijian==0:
			for i in err:
				station_name,city_name,country_name	=return_area(i[0])
				#tiqian={站点编号：（站点名称，城市名称，区县名称，机器型号）}
				tiqian[i[0]]=(station_name,city_name,country_name,zhandian[i[0]])
		
		elif shijian==1:
			for i in err:
				xinxi=areainfo[i[0]]
				tiqian[str((i[0],str(i[1])))]=(xinxi[0],xinxi[1],xinxi[2],zhandian[i[0]])
				#tiqian={（站点编号,时间）：（站点名称，城市名称，区县名称，机器型号）}
		#~ t3=time.time()
		#~ print 't2',t3-t2
		#~ print tiqian
		def sortedDict(adict):
			keys=adict.keys()
			keys.sort()
			return [(key,adict[key]) for key in keys]
		tiqian=sortedDict(tiqian)
		#tiqian=[(（站点编号,时间）,（站点名称，城市名称，区县名称，机器型号）)]
		try:
			city=request.form['city'].encode('utf-8')
		except Exception:
			city=0
		if city==0:
			#以市为单位统计提前报站
			chengshi=dict()
			for i in tiqian:
				if i[1][1] not in chengshi:
					chengshi[i[1][1]]=0
			for i in tiqian:
				if i[1][1] in chengshi:
					chengshi[i[1][1]]+=1
			area=[i for i in chengshi.keys()]
			number=[i for i in chengshi.values()]

			try:
				max_number=max(number)
				sum_number=sum(number)
			except Exception:
				#错误，无内容
				app.logger.error('no data')
				return render_template('tiqian.html')
			#统计每种机器的提前报量
			jiqi=dict()
			for i in tiqian:
				if i[1][3] not in jiqi:
					jiqi[i[1][3]]=0
			for i in tiqian:
				jiqi[i[1][3]]+=1
			jiqi=sorted(jiqi.iteritems(),key=lambda d:d[1],reverse=True)
			#~ print jiqi

			machine_type	=[i[0] for i in jiqi]
			machine_number	=[i[1] for i in jiqi]
			title_1=return_title(date)
			title_2=0
			if shijian==1:
				title_2=return_title(endtime)
			return jsonify(shuju_type='1',riqi=date,area=area,number=number,max_number=max_number,
			machine_type=machine_type,machine_number=machine_number,title=title_1,title_2=title_2,sum_number=sum_number,)
		else:
			quxian=dict()
			for i in tiqian:
				if (i[1][2] not in quxian) and (i[1][1].encode('utf-8')==city):
					quxian[i[1][2]]=0
			stationcode=[]
			country=[]
			machinetype=[]
			shijianduan=[]
			#统计每个区县的机器信息
			for i in tiqian:
				if i[1][2] in quxian:
					quxian[i[1][2]]+=1
				if i[1][1].encode('utf-8')==city:
					if shijian==0:
						stationcode.append(i[0])
						country.append(i[1][2])
						machinetype.append(i[1][3])
					elif shijian==1:
						diqu_shijian=eval(i[0])
						stationcode.append(diqu_shijian[0])
						shijianduan.append(diqu_shijian[1])
						country.append(i[1][2])
						machinetype.append(i[1][3])
			#~ print stationcode
			area=	[i for i in quxian.keys()]
			number=	[i for i in quxian.values()]
			try:
				max_number=max(number)
				sum_number=sum(number)
			except Exception:
				#错误，无内容
				app.logger.error('no data')
				return render_template('tiqian.html')

			#统计每种机器在市内的提前报量
			jiqi=dict()
			for i in tiqian:
				if i[1][3] not in jiqi:
					jiqi[i[1][3]]=0
			for i in machinetype:
				jiqi[i]+=1
			jiqi=sorted(jiqi.iteritems(),key=lambda d:d[1],reverse=True)
			jiqi_zhonglei=[i[0] for i in jiqi]
			jiqi_shumu=	[i[1] for i in jiqi]
			
			return jsonify(shuju_type='1',riqi=date,area=area,number=number,max_number=max_number,sum_number=sum_number,
			stationcode=stationcode,country=country,machinetype=machinetype,jiqi_zhonglei=jiqi_zhonglei,jiqi_shumu=jiqi_shumu,shijianduan=shijianduan)
			
	return render_template('tiqian.html')

if __name__=="__main__":
	bootstrap=Bootstrap(app)
	app.config['SECRET_KEY']='hard to guess string'
	app.debug=True
	app.run(host='0.0.0.0')


	
