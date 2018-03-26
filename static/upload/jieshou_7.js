//加载初始江西省地图
$.get('static/map/json/江西省.json', function (geoJson) {
	echarts.registerMap('jiangxi', geoJson);
	var myChart = echarts.init(document.getElementById('main'));
	var option = {
	title: {
		text:'江西省地图'
	},
	series: [
		{
			name: '接受率',
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
	tijiao(0);
});

var d= new Date();
function addzero(v){
	if(v<10){
		return '0'+v;
	}
	return v.toString();
}
var s=d.getUTCFullYear().toString()+'-'+addzero(d.getUTCMonth()+1)+'-'+addzero(d.getUTCDate())+' '+addzero(d.getUTCHours())+':00:00';
document.getElementById('datetime').value=s;
var zhandian= $("#datatype option:selected").text();
var title=d.getUTCFullYear().toString()+'年'+addzero(d.getUTCMonth()+1)+'月'+addzero(d.getUTCDate())+'日 '+addzero(d.getUTCHours())+'时（世界时）江西省'+zhandian+'接收率监控';
document.getElementById('title').innerText=title;

function f1(){
	var div1=document.getElementById('main');
	var div2=document.getElementById('main2');
	var div3=document.getElementById('main3');
	var div4=document.getElementById('main4');
	var div5=document.getElementById('main5');
	var div8=document.getElementById('main8');
	var myChart2 = echarts.init(div2);//接收表
	var myChart4 = echarts.init(div4);//入库表
	var myChart5 = echarts.init(div5);//发送表
	if (div1.style.display=="none"&& dicts!=null){
		div1.style.display="block";
		div2.style.display="block";
		div3.style.display="none";
		div4.style.display="block";
		div5.style.display="block";
		div8.style.display="none";
		load_Chart(dicts);
	}
}

function tijiao(x){
	var div1=document.getElementById('main');
	var div2=document.getElementById('main2');
	var div3=document.getElementById('main3');
	var div4=document.getElementById('main4');
	var div5=document.getElementById('main5');
	var div8=document.getElementById('main8');
	
	//x=3,传递最新时间
	if (x==3){
		var d= new Date();
		var s=d.getUTCFullYear().toString()+'-'+addzero(d.getUTCMonth()+1)+'-'+addzero(d.getUTCDate())+' '+addzero(d.getUTCHours())+':00:00';
		document.getElementById('datetime').value=s;
	}
	var rq=$('#myForm').serializeArray();
	var date_time={'button':x,'riqi':rq};
	div2.style.display="none";
	div3.style.display="none";
	div4.style.display="none";
	div5.style.display="none";
	div8.style.display="none";
	div1.style.display="block";
	GetAjaxData1(date_time);
};

var dicts=new Array();
function GetAjaxData1(date_time){
	document.getElementById("back").disabled=false;
	var pendingRequests = {};
    $.ajaxPrefilter(function( options, originalOptions, jqXHR ) {
        var key = options.url;
        console.log(key);
        if (!pendingRequests[key]) {
            pendingRequests[key] = jqXHR;
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
		url:"/jieshou",
		data: date_time,
		dataType: "json",
		async:false,
		error:function(request){
			alert("查询不到任何数据");
			tijiao(0);
		},
		success: function(result){
			dicts=result;
			load_Chart(dicts);
			var zhandian= $("#datatype option:selected").text();
			var title=result.title+'江西省'+zhandian+'接收率监控';
			document.getElementById('title').innerText=title;
		}
	});
};


function load_Chart(result){
	var div1=document.getElementById('main');
	var div2=document.getElementById('main2');
	var div4=document.getElementById('main4');
	var div5=document.getElementById('main5');
	var div9=document.getElementById('main9');
	var myChart = echarts.init(div1);//市地图
	var myChart2 = echarts.init(div2);//接收表
	var myChart4 = echarts.init(div4);//入库表
	var myChart5 = echarts.init(div5);//发送表
	div2.style.display="block";
	div4.style.display="block";
	div5.style.display="block";
	div9.style.display="block";
	document.getElementById('datetime').value=result.riqi;
	
	var option = {
		title: {
			text:'江西省地图',
			subtext:'数据接收率'
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
			type:'piecewise',
			min: 0,
			max: 1,
			splitNumber:7,
			precision:3,
			pieces:[
				{min:0,max:0.7,color:'grey'},
				{min:0.7,max:0.8,color:'red'},
				{min:0.8,max:0.85,color:'orange'},
				{min:0.85,max:0.9,color:'yellow'},
				{min:0.9,max:0.95,color:'#AECC33'},
				{min:0.95,max:0.99,color:'#00EE00'},
				{min:0.99,max:1,color:'green'}]
		},
		series: [
			{
				name: '接受率',
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
		option.series[0].data.push({'name':result.area[i],'value':result.jieshoulv[i]});//索引
	};
	myChart.setOption(option);
	load_recv_Chart(0,result);
	load_indb_Chart(0,result);
	load_send_Chart(0,result);
	var checksubmit=true;
	myChart.on('click',function(params){
		if (checksubmit==true){
			var city=params.name;
			load_recv_Chart(city,result);
			load_indb_Chart(city,result);
			load_send_Chart(city,result);
			loadcity(city,result);
			checksubmit=false;
		}
	});
}

function load_recv_Chart(city,result){
	var myChart2 = echarts.init(document.getElementById('main2'));
	var option2 = {
		title: {
			text:'接收情况'
		},
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
				}
			}
		],
		data:['提前','及时','逾限','超时','未到'],
		yAxis:[
			{
				type:'value'
			}
		],
		series: [
			{
				name:city,
				type: 'bar',
				data:[],
			}
		]
	};
	if (city==0){
		document.getElementById('city').innerText='江西省';
		var j=result.area.length-1;
		option2.series[0].name="江西省";
		option2.series[0].data.push({'value':result.jieshou_tiqian[j]});
		option2.series[0].data.push({'value':result.jieshou_zhunshi[j]});
		option2.series[0].data.push({'value':result.jieshou_yuxian[j]});
		option2.series[0].data.push({'value':result.jieshou_chaoshi[j]});
		option2.series[0].data.push({'value':result.jieshou_weidao[j]});
	}else{
		document.getElementById('city').innerText=city;
		for (i=0; i<result.area.length;i++){
			if (city==result.area[i]){
				option2.series[0].data.push({'value':result.jieshou_tiqian[i]});
				option2.series[0].data.push({'value':result.jieshou_zhunshi[i]});
				option2.series[0].data.push({'value':result.jieshou_yuxian[i]});
				option2.series[0].data.push({'value':result.jieshou_chaoshi[i]});
				option2.series[0].data.push({'value':result.jieshou_weidao[i]});
			}
		}
	}
	myChart2.setOption(option2);
};


function load_indb_Chart(city,result){
	var myChart4 = echarts.init(document.getElementById('main4'));
	var option4 = {
		title: {
			text:'入库情况',
		},
		tooltip: {
			trigger: 'axis',
			axisPointer:{
				type:'shadow'
			}
		},

		xAxis:[
			{
				type:'category',
				data:['0-1分钟','1-2分钟','2-3分钟','3-5分钟','5-10分钟','10分钟以上','入库提前'],
				axisLabel:{
					interval:0
				}
			}
		],
		yAxis:[
			{
				type:'value'
			}
		],
		
		series: [
			{
				name: city,
				type: 'bar',
				data:[]
			}
		]
	};
	if (city==0){
		option4.series[0].name="江西省";
		var j=result.area.length-1;
		option4.series[0].data.push({'value':result.min_1[j]});
		option4.series[0].data.push({'value':result.min_2[j]});
		option4.series[0].data.push({'value':result.min_3[j]});
		option4.series[0].data.push({'value':result.min_5[j]});
		option4.series[0].data.push({'value':result.min_10[j]});
		option4.series[0].data.push({'value':result.min_max[j]});
		option4.series[0].data.push({'value':result.tiqianruku[j]});
	}else{
		for (i=0; i<result.area.length;i++){
			if (city==result.area[i]){
				option4.series[0].data.push({'value':result.min_1[i]});
				option4.series[0].data.push({'value':result.min_2[i]});
				option4.series[0].data.push({'value':result.min_3[i]});
				option4.series[0].data.push({'value':result.min_5[i]});
				option4.series[0].data.push({'value':result.min_10[i]});
				option4.series[0].data.push({'value':result.min_max[i]});
				option4.series[0].data.push({'value':result.tiqianruku[i]});
			}
		};
	}
	myChart4.setOption(option4);
};

function load_send_Chart(city,result){
	var myChart5 = echarts.init(document.getElementById('main5'));
	var option5 = {
		title: {
			text:'发送情况'
		},
		tooltip: {
			trigger: 'axis',
			axisPointer:{
				type:'shadow'
			}
		},

		xAxis:[
			{
				type:'category',
				data:['提前','及时','逾限','超时','未到'],
				axisLabel:{
					interval:0
				}
			}
		],
		yAxis:[
			{
				type:'value'
			}
		],
		
		series: [
			{
				name: city,
				type: 'bar',
				data:[]
			}
		]
	};
	if (city==0){
		var j=result.area.length-1;
		option5.series[0].name="江西省";
		option5.series[0].data.push({'value':result.fasong_tiqian[j]});
		option5.series[0].data.push({'value':result.fasong_zhunshi[j]});
		option5.series[0].data.push({'value':result.fasong_yuxian[j]});
		option5.series[0].data.push({'value':result.fasong_chaoshi[j]});
		option5.series[0].data.push({'value':result.fasong_weidao[j]});
	}else{
		for (i=0; i<result.area.length;i++){
			if (city==result.area[i]){
				option5.series[0].data.push({'value':result.fasong_tiqian[i]});
				option5.series[0].data.push({'value':result.fasong_zhunshi[i]});
				option5.series[0].data.push({'value':result.fasong_yuxian[i]});
				option5.series[0].data.push({'value':result.fasong_chaoshi[i]});
				option5.series[0].data.push({'value':result.fasong_weidao[i]});
			}
		};
	}
	myChart5.setOption(option5);
};


function loadcity(city,result){
	var shuju;
	shuju='3';
	var option3 = {
		title: {
			text:city,
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
			type:'piecewise',
			min: 0,
			max: 1,
			splitNumber:7,
			precision:3,
			pieces:[
				{min:0,max:0.7,color:'grey'},
				{min:0.7,max:0.8,color:'red'},
				{min:0.8,max:0.85,color:'orange'},
				{min:0.85,max:0.9,color:'yellow'},
				{min:0.9,max:0.95,color:'#AECC33'},
				{min:0.95,max:0.99,color:'#00EE00'},
				{min:0.99,max:1,color:'green'}]
		},
		series: [
			{
				name: '接受率',
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
				}
			}
		]
	};
	$.get('static/map/json/'+city+'.json', function (geoJson) {
		echarts.registerMap('city', geoJson);
		var myChart3 = echarts.init(document.getElementById('main3'));
		var rq=$('#myForm').serializeArray();
		var city_date={'button':shuju,'riqi':rq,'city':city};
		var div1=document.getElementById('main');
		var div2=document.getElementById('main2');
		var div3=document.getElementById('main3');
		var div4=document.getElementById('main4');
		var div5=document.getElementById('main5');
		var div8=document.getElementById('main8');
		$.ajax({
			cache: false,
			type:"POST",
			url:"/jieshou",
			data: city_date,
			dataType: "json",
			async:false,
			error:function(request){
				alert("查询不到任何数据");
				tijiao(0);
			},
			success: function(result){
				option3.series[0].data=[];
				for (i=0; i<result.area.length;i++){
					option3.series[0].data.push({'name':result.area[i],'value':result.jieshoulv[i]});
				}
				myChart3.setOption(option3);
				div1.style.display="none";
				div3.style.display="block";
				div8.style.display="block";
				myChart3.on('click',function(params){
					var city=params.name;
						load_recv_Chart(city,result);
						load_indb_Chart(city,result);
						load_send_Chart(city,result);	
				});
			}
		});
	});
};

	
	
	
