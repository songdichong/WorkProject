//加载初始江西省地图
$.get('static/map/json/江西省.json', function (geoJson) {
	echarts.registerMap('jiangxi', geoJson);
	var myChart = echarts.init(document.getElementById('main'));
	var xinxi= $("#xinxi option:selected").text();
	var option = {
	title: {
		text:'江西省地图'
	},
	series: [
		{
			name: xinxi,
			type: 'map',
			mapType: 'jiangxi', // 自定义扩展图表类型
			itemStyle:{
				normal:{label:{show:true}},
				emphasis:{label:{show:true}}
			},
			data:[] 	
		}
	]
	};
	myChart.setOption(option);
	tijiao(4);
});

//默认最新时间
var d= new Date();
function addzero(v){
	if(v<10){
		return '0'+v;
	}
	return v.toString();
}
var s=d.getUTCFullYear().toString()+'-'+addzero(d.getUTCMonth()+1)+'-'+addzero(d.getUTCDate())+' '+addzero(d.getUTCHours())+':00:00';
document.getElementById('datetime').value=s;
var xinxi= $("#xinxi option:selected").text();
var title=d.getUTCFullYear().toString()+'年'+addzero(d.getUTCMonth()+1)+'月'+addzero(d.getUTCDate())+'日 '+addzero(d.getUTCHours())+'时（世界时）江西省区域站'+xinxi+'信息监控';
document.getElementById('title').innerText=title;

function swapTime(){
	var time=document.getElementById('time');
	var newInput = document.createElement("input");
	var shijian= $("#shijian option:selected").val();
	if (shijian==1){
		document.getElementById('datetime').value="起始时间";
		newInput.setAttribute("id","endtime");
		newInput.setAttribute("placeholder","yyyy-mm-dd");
		newInput.setAttribute("onfocus","WdatePicker({maxDate:'%y-%M-%d {%H-8}:%m:%s',dateFmt:'yyyy-MM-dd HH:00:00',lang:'zh-cn'})");
		newInput.value="结束时间";
		time.appendChild(newInput);
		document.getElementById("shangyi").disabled='disabled';
		document.getElementById("xiayi").disabled='disabled';
		document.getElementById("zuixin").disabled='disabled';
	}else if (shijian==0){
		document.getElementById('datetime').value=s;
		document.getElementById('endtime').remove();
		document.getElementById("shangyi").disabled=false;
		document.getElementById("xiayi").disabled=false;
		document.getElementById("zuixin").disabled=false;
	}
}

function tijiao(x,y){
	var div1=document.getElementById('main');
	var div2=document.getElementById('main2');
	var div3=document.getElementById('main3');
	var div6=document.getElementById('main6');
	var div8=document.getElementById('main8');
	//x=7,传递最新时间
	if (x==7){
		var d= new Date();
		var s=d.getUTCFullYear().toString()+'-'+addzero(d.getUTCMonth()+1)+'-'+addzero(d.getUTCDate())+' '+addzero(d.getUTCHours())+':00:00';
		document.getElementById('datetime').value=s;
	}
	var datetime=$('#datetime').val();
	var endtime=$('#endtime').val();
	var shijian= $("#shijian option:selected").val();
	if (y==0){
		shijian=0;
		document.getElementById("shijian").options[0].selected = true;
		swapTime();
	}
	var xinxi=$("#xinxi option:selected").val();
	var date_time={'button':x,'datetime':datetime,'datatype':1,'shijian':shijian,'xinxi':xinxi,'endtime':endtime};
	div2.style.display="none";
	div3.style.display="none";
	div6.style.display="none";
	div8.style.display="none";
	div1.style.display="block";
	$('tbody#main7').empty();
	GetAjaxData1(date_time);
};

function f1(){
	var div1=document.getElementById('main');
	var div2=document.getElementById('main2');
	var div3=document.getElementById('main3');
	var div6=document.getElementById('main6');
	var div8=document.getElementById('main8');
	if (div1.style.display=="none"&& dicts!=null){
		div1.style.display="block";
		div2.style.display="block";
		div3.style.display="none";
		div6.style.display="none";
		div8.style.display="none";
		load_Chart(dicts);
	}
}

var dicts=new Array();
function GetAjaxData1(date_time){
	document.getElementById("back").disabled=false;
	var pendingRequests = {};
    $.ajaxPrefilter(function( options, originalOptions, jqXHR ) {
        var key = options.url;
        console.log(key);
        if (!pendingRequests[key]) {
            pendingRequests[key] = jqXHR;0
        }else{
            //jqXHR.abort();    //放弃后触发的提交
            pendingRequests[key].abort();   // 放弃先触发的提交
        }

        var complete = options.complete;
        options.complete = function(jqXHR, textStatus) {
            pendingRequests[key] = null;
            if ($.isFunction(complete)) {
            complete.apply(this, arguments);
            }
        };
    });
	$.ajax({
		cache: false,
		type:"POST",
		url:"/tiqian",
		data: date_time,
		dataType: "json",
		async:false,
		error:function(request){
			alert("本时段没有数据");
			document.getElementById('datetime').value=s;
			$("#shijian").val()=0;
			tijiao(4);
		},
		success: function(result){
			dicts=result;
			load_Chart(dicts);
			var xinxi= $("#xinxi option:selected").text();
			var shijian= $("#shijian option:selected").val();
			if (shijian==0){
				var title=result.title+'江西省区域站'+xinxi+'信息监控';
				document.getElementById('title').innerText=title;
			}else if(shijian==1){
				var title=result.title+'到'+result.title_2+'江西省区域站'+xinxi+'信息监控';
				document.getElementById('title').innerText=title;
			}
		}
	});
};

function load_Chart(result){
	var div1=document.getElementById('main');
	var div2=document.getElementById('main2');
	var myChart = echarts.init(div1);//市地图
	var myChart2 = echarts.init(div2);//接收表
	div2.style.display="block";
	document.getElementById('datetime').value=result.riqi;
	var xinxi= $("#xinxi option:selected").text();
	var option = {
		title: {
			text:'江西省地图',
			subtext:xinxi,
		},
		tooltip: {
			trigger: 'item',
			formatter: '{b}<br/>{c} '
		},
		toolbox: {
			show: true,
			orient: 'vertical',
			left: 'right',
			top: 'center',
			feature: {
				dataView: {readOnly: false},
				restore: {},
				saveAsImage: {}
			}
		},
		visualMap: {
			type:'continuous',
			min: 0,
			max: result.max_number,
			realtime: false,
			calculable: true,
			inRange: {
				color: ['lightskyblue','yellow','red']
			}
		},
		series: [
			{
				name: xinxi,
				type: 'map',
				mapType: 'jiangxi', // 自定义扩展图表类型
				itemStyle:{
					normal:{label:{show:true}},
					emphasis:{label:{show:true}}
				},
				data:[] 	
			}
		]
	};
	option.series[0].data=[];
	for (i=0; i<result.area.length;i++){
		option.series[0].data.push({'name':result.area[i],'value':result.number[i]});//索引
	};
	myChart.setOption(option);
	load_recv_Chart(0,result);
	var checksubmit=true;
	myChart.on('click',function(params){
		//~ alert('zenmeban');
		if (checksubmit==true){
			var city=params.name;
			loadcity(city,result);
			checksubmit=false;
		}
	});
}
function load_recv_Chart(city,result){
	var myChart2 = echarts.init(document.getElementById('main2'));
	var option2 = {
		title: [],
		tooltip: {
			trigger: 'axis',
			axisPointer:{
				type:'shadow'
			},
		},
		xAxis:[
			{	position:'bottom',
				type:'category',
				axisLabel:{
					interval:0,
					rotate:-20
				}
			}
		],
		data:[],
		yAxis:[
			{
				type:'value'
			}
		],
		series: [
			{
				type: 'bar',
				data:[],
				barWidth : 30,
			}
		]
	};
	var xinxi= $("#xinxi option:selected").text();
	if (city==0){
		option2.title={text:'江西省本时次'+xinxi+'总和:'+result.sum_number,subtext:'机器型号'};
		for (i=0; i<result.machine_type.length;i++){
			option2.data.push(result.machine_type[i]);
			option2.series[0].data.push({'name':result.machine_type[i],'value':result.machine_number[i]});
		}
	}else{
		option2.title={text:city+'本时次'+xinxi+'总和:'+result.sum_number,subtext:'机器型号'};
		for (i=0; i<result.jiqi_zhonglei.length;i++){
			option2.data.push(result.jiqi_zhonglei[i]);
			option2.series[0].data.push({'name':result.jiqi_zhonglei[i],'value':result.jiqi_shumu[i]});
		}
	}
	myChart2.setOption(option2);

};

function loadcity(city,result){
	var shuju='4';
	var xinxi= $("#xinxi option:selected").text();
	var option3 = {
		title: {
			text:city,
			subtext:xinxi
		},
		tooltip: {
			trigger: 'item',
			formatter: '{b}<br/>{c} '
		},
		toolbox: {
			show: true,
			orient: 'vertical',
			left: 'right',
			top: 'center',
			feature: {
				dataView: {readOnly: false},
				restore: {},
				saveAsImage: {}
			}
		},
		visualMap: {
			type:'continuous',
			min: 0,
			realtime: false,
			calculable: true,
			inRange: {
				color: ['lightskyblue','yellow','red']
			}
		},
		series: [
			{
				name: city,
				type: 'map',
				mapType: 'city', // 自定义扩展图表类型
				itemStyle:{
					normal:{label:{show:true}},
					emphasis:{label:{show:true}}
				},
				data:[],
				nameMap:{
					'濂溪区':'九江市辖区',
					'浔阳区':'九江市辖区',
					'湘东区':'萍乡市辖区',
					'安源区':'萍乡市辖区',
					'青山湖区':'南昌市辖区',
					'东湖区':'南昌市辖区',
					'西湖区':'南昌市辖区',
					'青云谱区':'南昌市辖区',
				},
			}
		]
	};
	
	$.get('static/map/json/'+city+'.json', function (geoJson) {
		echarts.registerMap('city', geoJson);
		var div1=document.getElementById('main');
		var div2=document.getElementById('main2');
		var div3=document.getElementById('main3');
		var div8=document.getElementById('main8');
		var myChart3 = echarts.init(div3);
		var datetime=$('#datetime').val();
		var endtime=$('#endtime').val();
		var shijian= $("#shijian option:selected").val();
		var xinxi=$("#xinxi option:selected").val();
		var city_date={'button':shuju,'datetime':datetime,'datatype':1,'shijian':shijian,'xinxi':xinxi,'endtime':endtime,'city':city};
		$.ajax({
			cache: false,
			type:"POST",
			url:"/tiqian",
			data: city_date,
			dataType: "json",
			async:false,
			error:function(request){
				alert("查询不到任何数据");
				document.getElementById('datetime').value=s;
				tijiao(4,0);
			},
			success: function(result){
				option3.series[0].data=[];
				option3.visualMap.max=result.max_number;
				for (i=0; i<result.area.length;i++){
					option3.series[0].data.push({'name':result.area[i],'value':result.number[i]});
				};
				myChart3.setOption(option3);
				div1.style.display="none";
				div3.style.display="block";
				div8.style.display="block";
				load_recv_Chart(city,result);
				myChart3.on('click',function(params){
					var div6=document.getElementById('main6');
					var town=params.name;
					$('tbody#main7').empty();
					for (i=0;i<result.country.length;i++){
						if (result.country[i]==town){
							var row=loadbiaoge(result,i,shijian);
							$('tbody#main7').append(row);
							div2.style.display="none";
							div6.style.display="block";
						}
					}
				});
			}
		});

	});
};
function loadbiaoge(result,i,shijian){
	var row=document.createElement('tr');
	var codeCell=document.createElement('td');
	codeCell.innerHTML=result.stationcode[i];
	row.appendChild(codeCell);
	var nameCell=document.createElement('td');
	nameCell.innerHTML=result.country[i];
	row.appendChild(nameCell);
	var machineCell=document.createElement('td');
	machineCell.innerHTML=result.machinetype[i];
	row.appendChild(machineCell);
	var timeCell=document.createElement('td');
	if (shijian==0){
		timeCell.innerHTML=result.riqi;
	}else if (shijian==1){
		timeCell.innerHTML=result.shijianduan[i];
	}
	row.appendChild(timeCell);
	return row
}
		
	
	
	
