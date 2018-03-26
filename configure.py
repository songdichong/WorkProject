#coding=utf-8
import MySQLdb
import sqlite3
import time
class aService(object):	
	
	'''
	Data are originally connected using MySQLdb. For information safety I 
	use a sqlite database here and it could be examined if anyone creates a database locally.
	'''
	def connect(self):
		conn== sqlite3.connect('./monitorcimiss.db')
		cursor = connection.cursor()
		cursor.execute('PRAGMA foreign_keys=ON; ')
		connection.commit()
		return conn,cursor
	
	'''
	在st_adcd_v视图中选取地区信息
	args: 	None.
	return: relation,格式：{adcd:CTCD}。
	'''
	def get_area_info(self):
		conn,cursor=aService().connect()
		a=cursor.execute("select adcd,CTCD from st_adcd_v")
		area=cursor.fetchmany(a)
		relation=dict()
		for i in range(0,len(area)):
			relation[area[i][0].encode('utf-8')]=area[i][1].encode('utf-8')
		cursor.close()
		conn.close()
		return relation
	'''
	在st_pro_areacode表格中选取地区信息
	args: 	None.
	return: relation,格式：{adcd:ADNM}。
	'''
	def translate(self):
		conn,cursor=aService().connect()
		a=cursor.execute("select ADCD,ADNM from st_pro_areacode")
		area=cursor.fetchmany(a)
		relation=dict()
		for i in range(0,len(area)):
			relation[area[i][0].encode('utf-8')]=area[i][1].encode('utf-8')
		cursor.close()
		conn.close()
		return relation
		
	'''
	在st_pro_areastat表格中选取专业信息，
	arg: 
		obtype: 需要的专业信息，对应信息在st_datatype表格中可查到
		time:	用户输入的时间
	return:
		分为recv,indb,send三类。
	'''
	def get_stat_info(self,obtype,time):
		conn,cursor=aService().connect()
								#~ 0 	1 		2			3			4			5			6			7		8			9			10		11			12			13		14			15			16			17			18
		a=cursor.execute("select ADCD,TOTAL,BEFORETOTAL,INTIMETOTAL,LATERTOTAL,LATERLOSTTOTAL,LOSTTOTAL,INDBMINU1,INDBMINU2,INDBMINU3,INDBMINU5,INDBMINU10,INDBMINUMAX,INDBBEFORE,SENDBEFORE,SENDINTIME,SENDLATER,SENDLATERLOST,SENDLOST from st_pro_areastat where OBTYPE='{0}' and TM='{1}'".format(obtype,time))
		all_info=cursor.fetchmany(a)
		#~ a=cursor.execute("select ADCD,TOTAL,BEFORETOTAL,INTIMETOTAL,LATERTOTAL,LATERLOSTTOTAL,LOSTTOTAL from st_pro_areastat where OBTYPE='{0}' and TM='{1}'".format(obtype,time))
		#~ b=cursor.execute("select ADCD,INDBMINU1,INDBMINU2,INDBMINU3,INDBMINU5,INDBMINU10,INDBMINUMAX,INDBBEFORE from st_pro_areastat where OBTYPE='{0}' and TM='{1}'".format(obtype,time))
		#~ stat_indb=cursor.fetchmany(b)
		#~ c=cursor.execute("select ADCD,SENDBEFORE,SENDINTIME,SENDLATER,SENDLATERLOST,SENDLOST from st_pro_areastat where OBTYPE='{0}' and TM='{1}'".format(obtype,time))
		#~ stat_send=cursor.fetchmany(c)
		cursor.close()
		conn.close()
		stat_recv=[]
		stat_indb=[]
		stat_send=[]
		for i in range(0,len(all_info)):
			recv=[]
			recv.append(all_info[i][0])
			indb=[]
			indb.append(all_info[i][0])
			send=[]
			send.append(all_info[i][0])
			for j in range(1,7):
				recv.append(all_info[i][j])
			for j in range(7,14):
				indb.append(all_info[i][j])
			for j in range(14,19):
				send.append(all_info[i][j])
			stat_recv.append(recv)
			stat_indb.append(indb)
			stat_send.append(send)
		return stat_recv,stat_indb,stat_send

	#一个运用di表查询的方法，后面改成用st_pro_station_program表查询
	#~ def get_station_info(self,obtype,endtime):
		#~ conn,cursor=aService().connect()
		#~ a=cursor.execute("select station,recv_diff,send_diff,indb_diff from st_di where cate_data='{0}' and  obs_time='{1}'".format(obtype,endtime))
		#~ station_info=cursor.fetchmany(a)
		#~ cursor.close()
		#~ conn.close()
		#~ return station_info
	
	def get_station_info(self,obtype,starttime,endtime,xinxi):
		conn,cursor=aService().connect()
		a=cursor.execute("select CODE,TM from st_pro_station_program where OBTYPE='{0}' and TM between '{1}' and '{2}' and RECVSTATUS='{3}'".format(obtype,starttime,endtime,xinxi))
		station_info=cursor.fetchmany(a)
		cursor.close()
		conn.close()
		return station_info
	
	def get_areacode(self, stationnum):
		conn,cursor=aService().connect()
		a=cursor.execute("select areacode,cityname,countyname from st_stationinfo_v where stationnum='{0}'".format(stationnum))
		areacode=cursor.fetchmany(a)
		cursor.close()
		conn.close()
		return areacode[0]
		
	def get_all_areacode(self):
		conn,cursor=aService().connect()
		a=cursor.execute("select stationnum,areacode,cityname,countyname from st_stationinfo_v")
		b=cursor.fetchmany(a)
		cursor.close()
		conn.close()
		areacode=dict()
		for i in b:
			areacode[i[0]]=(i[1],i[2],i[3])
		return areacode
#~ if __name__=="__main__":
	#~ t1=time.time()
	#~ obtype='SURF@AWS_REG'
	#~ time1='2017-08-03 17:00:00'
	#~ time2='2017-08-03 23:00:00'
	#~ err=aService().get_station_info(obtype,time1,time2,0)
	#~ t2=time.time()
	#~ print t2-t1
	#~ print err
	#~ a=aService().get_all_areacode()
	#~ print a
	#~ t3=time.time()
	#~ print t3-t2
	#~ err=[]
	#~ for i in station_info:
		#~ if i[1]=='0':
			#~ err.append(i)
	#~ print err
	#~ t2=time.time()
	#~ print ('t1:',t2-t1)
	#~ relation=aService().translate()
	#~ t3=time.time()
	#~ print ('t2:',t3-t2)
