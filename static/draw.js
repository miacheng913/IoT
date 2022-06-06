function drawLineCanvas(id,data) {
    var ctx = document.getElementById(id).getContext("2d");
    
    window.myLine = new Chart(ctx, {  //先建立一個 chart
        type: 'line', // 型態
        data: data,
        options: {
                responsive: true,
                legend: { //是否要顯示圖示
                    display: true,
                },
                tooltips: { //是否要顯示 tooltip
                    enabled: true
                },
                scales: {  //是否要顯示 x、y 軸
                    xAxes: [{
                        display: true
                    }],
                    yAxes: [{
                        display: true
                    }]
                },
                animation: {
                    duration: 0
                },
                responsive: true,
                maintainAspectRatio: false
            }
    });
};
function get_history(){
    var xhr2 = new XMLHttpRequest();
    var url2 = "historydata";
    xhr2.open("GET", url2);
    xhr2.onload = function () {
        var obj2 = JSON.parse(xhr2.responseText);
        
        obj2 =  JSON.parse(obj2);
        console.log(obj2)
        var lineChartData = {
            labels:obj2.time_stamp, //顯示區間名稱
            datasets : [
                {
                    label: '溫度', // tootip 出現的名稱
                    //lineTension: 0, // 曲線的彎度，設0 表示直線
                    backgroundColor: "#ea464d",
                    borderColor: "#ea464d",
                    //borderWidth: 5,
                    data: obj2.temperature, // 資料
                    fill: false, // 是否填滿色彩
                },
            ]
        };
        var lineChartData2 = {
            labels:obj2.time_stamp, //顯示區間名稱
            datasets : [
                {
                    label: 'light', // tootip 出現的名稱
                    //lineTension: 1, // 曲線的彎度，設0 表示直線
                    backgroundColor: "#ea464d",
                    borderColor: "#ea464d",
                    //borderWidth: 5,
                    data: obj2.light, // 資料
                    fill: false, // 是否填滿色彩
                },
            ]
        };
        var lineChartData3 = {
            labels:obj2.time_stamp, //顯示區間名稱
            datasets : [
                {
                    label: 'co2', // tootip 出現的名稱 // 曲線的彎度，設0 表示直線
                    backgroundColor: "#ea464d",
                    borderColor: "#ea464d",
                    //borderWidth: 5,
                    data: obj2.co2, // 資料
                    fill: false, // 是否填滿色彩
                },
            ]
        };
    
        drawLineCanvas("temperature",lineChartData);
        drawLineCanvas("light",lineChartData2);
        drawLineCanvas("co2",lineChartData3);
    };
    xhr2.send();
}