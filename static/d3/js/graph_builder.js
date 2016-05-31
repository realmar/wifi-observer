var colors_red    = ['#FF545A'];
var colors_rg     = ['#D62728', '#2CA02C'];
var colors_rgg    = ['#D62728', '#2CA02C', '#7F7F7F'];
var colors_duo    = ['#1F77B4', '#9ADA81'];
var colors_custom = '#7F7F7F #1F77B4 #9467BD #8C564B #E377C2 #17BECF #FF7F0E #BCBD22'.split(' ');
var date_format   = d3.time.format.utc('%Y-%m-%d %H:%M:%S');

function displayData(render_all) {
  var url = "";
  if(!render_all) {
    url = "/static/d3/" + $("span#data_year")[0].innerHTML + "-" + $("span#data_week_start")[0].innerHTML + "-" + $("span#data_week_end")[0].innerHTML + ".csv";
  }else{
    url = "/static/d3/all.csv"
  }
  d3.csv(url, function(data) {
      return parse(data);
  }, function(error, data) {
      if (error) {
          console.log(error);
      } else {
          visualize(data);
      }
  });
}

function parse(data) {
    return {
        id:        data.id,
        timestamp: date_format.parse(data.timestamp),
        conn:      data.conn,
        dhcp:      data.dhcp,
        ssid:      data.ssid,
        bssid:     data.bssid,
    };
};

function visualize(data) {

    var cf  = crossfilter(data);

    var dim_id    = cf.dimension(function(d) { return d.id; });
    var dim_conn  = cf.dimension(function(d) { return d.conn; });
    var dim_dhcp  = cf.dimension(function(d) {
         if(d.conn == '0') {
             return 2;
         }else if(d.dhcp == '0' && d.conn == '1') {
             return 0;
         }else{
             return 1;
         }
    });
    var dim_ssid  = cf.dimension(function(d) { return d.ssid; });
    var dim_bssid = cf.dimension(function(d) { if(!(d.dhcp == '1' && d.conn == '0')) { return d.bssid; } else { return 3; } });
    var dim_hour  = cf.dimension(function(d) { return d3.time.hour(d.timestamp); });

    var group_conn  = dim_conn.group().reduceCount();
    var group_dhcp  = dim_dhcp.group().reduceCount();
    var group_ssid  = dim_ssid.group().reduceCount();
    var group_bssid = dim_bssid.group().reduceCount();
    var group_const = dim_hour.group().reduce(
        function reduceAdd(p, v) { return p; },
        function reduceRemove(p, v) { return p; },
        function reduceInitial() { return 0; }
    );
    var group_conn_fails = dim_hour.group().reduceSum(function(d) { return d.conn == '0' ? 1 : 0; });
    var group_dhcp_fails = dim_hour.group().reduceSum(function(d) {
        if(d.dhcp == '0' && d.conn == '1') {
            return 1;
        }else{
            return 0;
	}
    });

    var timerange = [d3.min(data,function(d){return d.timestamp}), d3.max(data,function(d){return d.timestamp})];

    dc.dataCount("#datacount-projects")
        .dimension(cf)
        .group(cf.groupAll());

    dc.pieChart("#piechart-conn")
        .width(250)
        .height(250)
        .dimension(dim_conn)
        .group(group_conn)
        .ordinalColors(colors_rg)
        .label(function(d) { return d.key == 1 ? 'success' : 'failure'; })
        .title(function(d) { return d.value; });

    dc.pieChart("#piechart-dhcp")
        .width(250)
        .height(250)
        .dimension(dim_dhcp)
        .group(group_dhcp)
        .ordinalColors(colors_rgg)
        .label(function(d) {
            if (d.key == 1){
                return 'success';
            } else if (d.key == 0){
                return 'failure';
            } else if (d.key == 2) {
                return 'noconn';
            }
        })
        .title(function(d) { return d.value; });

    dc.pieChart("#piechart-ssid")
        .width(250)
        .height(250)
        .dimension(dim_ssid)
        .group(group_ssid)
        .ordinalColors(colors_duo)
        .label(function(d) { return d.key; })
        .title(function(d) { return d.value; });

    dc.rowChart("#rowchart-bssid")
        .width(350)
        .height(350)
        .dimension(dim_bssid)
        .group(group_bssid)
        .ordinalColors(colors_custom)
        .labelOffsetX(5)
        .label(function(d) {
	    if(d.key == '' && d.key != 3) {
	        return 'noconn';
	    }else{
		return d.key;
            }
        })
        .title(function(d) { return d.value; })
        .elasticX(false)
        .x(d3.scale.log().clamp(true).domain([1, 15000]).range([0,350]).nice());

    var conntime = dc.lineChart("#linechart-conn-time");
    conntime
        .renderArea(true)
        .mouseZoomable(false)
        .width(1150)
        .height(70)
        .dimension(dim_hour)
        .group(group_const)
        .x(d3.time.scale().domain(timerange))
        .round(d3.time.hour.round)
        .xUnits(d3.time.hours)
        .yAxisLabel('zoom')
        .yAxis().ticks([]);

    dc.lineChart("#linechart-conn-failure")
        .rangeChart(conntime)
        .renderArea(true)
        .mouseZoomable(false)
        .width(1150)
        .height(200)
        .ordinalColors(colors_red)
        .dimension(dim_hour)
        .group(group_conn_fails)
        .x(d3.time.scale().domain(timerange))
        .round(d3.time.hour.round)
        .xUnits(d3.time.hours);

    var dhcptime = dc.lineChart("#linechart-dhcp-time");
    dhcptime
        .renderArea(true)
        .mouseZoomable(false)
        .width(1150)
        .height(70)
        .dimension(dim_hour)
        .group(group_const)
        .x(d3.time.scale().domain(timerange))
        .round(d3.time.hour.round)
        .xUnits(d3.time.hours)
        .yAxisLabel('zoom')
        .yAxis().ticks([]);

    dc.lineChart("#linechart-dhcp-failure")
        .rangeChart(dhcptime)
        .renderArea(true)
        .mouseZoomable(false)
        .width(1150)
        .height(200)
        .ordinalColors(colors_red)
        .dimension(dim_hour)
        .group(group_dhcp_fails)
        .x(d3.time.scale().domain(timerange))
        .round(d3.time.hour.round)
        .xUnits(d3.time.hours)
        .xAxis();

    dc.dataTable("#datatable-projects")
        .dimension(dim_id)
        .group(function (d) { return ''; })
        .size(50)
        .columns([
            function (d) { return d.timestamp; },
            function (d) { return d.conn == 1 ? 'success' : 'failure' ; },
            function (d) {
                if (d.dhcp == '1'){
                    return 'success';
                } else if (d.dhcp == '0'){
                    return 'failure';
                } else {
                    return d.dhcp;
                }
            },
            function (d) { return d.ssid; },
            function (d) { return d.bssid; },
            function (d) { return d.id; }
        ])
        .sortBy(function (d) { return +d.id; })
        .order(d3.ascending);

    dc.renderAll();
}


displayData(false);
