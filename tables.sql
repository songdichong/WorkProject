drop table if exists st_adcd_v;
drop table if exists st_pro_areacode;
drop table if exists st_pro_areastat;
drop table if exists st_pro_station_program;
drop table if exists st_stationinfo_v;
create table st_adcd_v (adcd int,
adnm text, pst text,
PRCD int, PRNM text,
CTCD int, CTNM text,
primary key(adcd));

create table st_pro_areacode(
ADCD int, ADNM text, PST text,primary key(adcd));

create table st_pro_areastat(ADCD int, OBTYPE text, TM date, FLAG int, TOTAL int, OBSTOTAL int, BEFORETOTAL int, INTIMETOTAL int, LATERTOTAL int, LATERLOSTTOTAL int, LOSTTOTAL int, INDBMINU1 int, INDBMINU2 int, INDBMINU3 int, INDBMINU5 int, INDBMINU10 int, INDBMINUMAX int, INDBBEFORE int, INDBUNDO int, SENDBEFORE int, SENDINTIME int, SENDLATER int, SENDLATERLOST int, SENDLOST int,primary key(adcd,OBTYPE,TM));

create table st_pro_station_program(CODE text, OBTYPE text, TM date, RECVSTATUS int, TOTAL text, INDB text, SEND text,UNKONWNINT int,OBTYPE2 text, primary key(CODE));

create table st_stationinfo_v(stationnum text, cname blob, cityname blob, countyname blob, stationtype text, rulecode text, ruledesc blob,stationtpnm blob, primary key(stationnum));
