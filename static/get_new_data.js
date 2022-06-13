function get_newest(){
    var xhr = new XMLHttpRequest();
    var url = "newestdata";
    xhr.open("GET", url);
    xhr.onload = function () {
        var obj = JSON.parse(xhr.responseText);
        obj =  JSON.parse(obj);
        
        var table_select = document.getElementById('newdataTable');
        inner = "<div class='round'>\
            <p>co2</p>\
            <br><p>" + obj.co2 + "</p>\
        </div>\
        <div class='round'>\
            <p>face</p>\
            <br><p>" + obj.face + "</p>\
        </div>\
        <div class='round'>\
            <p>light</p>\
            <br><p>" + obj.light + "</p>\
        </div>\
        <div class='round'>\
            <p>temperature</p>\
            <br><p>" + obj.temperature + " °C" + "</p>\
        </div>";
        table_select.innerHTML = inner;
    };
    xhr.send();
}

