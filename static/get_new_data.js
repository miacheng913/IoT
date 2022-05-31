function get_newest(){
    var xhr = new XMLHttpRequest();
    var url = "newestdata";
    xhr.open("GET", url);
    xhr.onload = function () {
        var obj = JSON.parse(xhr.responseText);
        obj =  JSON.parse(obj);
        
        var table_select = document.getElementById('newdataTable');
        inner = "<table>\
        <tr>\
            <td>co2</td>\
            <td>" + obj.co2 + "</td>\
        </tr>\
        <tr>\
            <td>face</td>\
            <td>" + obj.face + "</td>\
        </tr>\
        <tr>\
            <td>light</td>\
            <td>" + obj.light + "</td>\
        </tr>\
        <tr>\
            <td>temperature</td>\
            <td>" + obj.temperature + " °C" + "</td>\
        </tr>\
        </table>";
        table_select.innerHTML = inner;
    };
    xhr.send();
}