function jump() {
    var xhr = new XMLHttpRequest();
    var url = "state/alto";
    xhr.open("POST", url);
    xhr.send();
    
    //alert('即將跳轉頁面');
    window.location.replace("/");
      
  };

  function jump_history() {
    
    //alert('即將跳轉頁面');
    window.location.replace("/history");
      
  };

  function jump_ins() {
    
    //alert('即將跳轉頁面');
    window.location.replace("/home");
      
  };

  function jump2() {
    var xhr = new XMLHttpRequest();
    var url = "state/notalto";
    xhr.open("POST", url);
    xhr.send();
    //alert('即將跳轉頁面');
    window.location.replace("/control");
      
  };

  function control(cmd) {
    var xhr = new XMLHttpRequest();
    var url = "cmd/" + cmd;
    xhr.open("POST", url);
    xhr.send();
    console.log(cmd);
      
    if(cmd=='light:101'){
        document.getElementById('light_button2').style.background='#FF79BC';
        document.getElementById('light_button1').style.background='#6fa8dc';
    }
    else if(cmd=='light:100'){
      document.getElementById('light_button1').style.background='#FF79BC';
      document.getElementById('light_button2').style.background='#6fa8dc';
  }

    else if(cmd=='light:110'){
        document.getElementById('row_button2').style.background='#FF79BC';
        document.getElementById('row_button1').style.background='#6fa8dc';
    }
    else if(cmd=='light:111'){
      document.getElementById('row_button1').style.background='#FF79BC';
      document.getElementById('row_button2').style.background='#6fa8dc';
    }

    else if(cmd=='fan:1'){
      document.getElementById('fan_button2').style.background='#FF79BC';
      document.getElementById('fan_button1').style.background='#6fa8dc';
    }
    else if(cmd=='fan:0'){
      document.getElementById('fan_button1').style.background='#FF79BC';
      document.getElementById('fan_button2').style.background='#6fa8dc';
    }
  
  else if(cmd=='monitor:1'){
    document.getElementById('mon_button2').style.background='#FF79BC';
    document.getElementById('mon_button1').style.background='#6fa8dc';
  }
  else {
    document.getElementById('mon_button1').style.background='#FF79BC';
    document.getElementById('mon_button2').style.background='#6fa8dc';
  }

  }

  function changeColor(id) {
    document.getElementById(id).style.background='#5e2e2e';
}

function get_newest(){
  var xhr = new XMLHttpRequest();
  var url = "state";
  xhr.open("GET", url);
  xhr.onload = function () {
      var obj = JSON.parse(xhr.responseText);
      obj =  JSON.parse(obj);
      console.log(obj);
      if(obj.fan=='0'){
        document.getElementById('fan_button1').style.background='#FF79BC';
        document.getElementById('fan_button2').style.background='#6fa8dc';
      }
      else{
        document.getElementById('fan_button2').style.background='#FF79BC';
        document.getElementById('fan_button1').style.background='#6fa8dc';
      }

      if(obj.light1=="101"){
        console.log("open");
        document.getElementById('light_button2').style.background='#FF79BC';
        document.getElementById('light_button1').style.background='#6fa8dc';
      }
      else{
        document.getElementById('light_button1').style.background='#FF79BC';
        document.getElementById('light_button2').style.background='#6fa8dc';
      }

      if(obj.light2=="111"){
        console.log("open2");
        document.getElementById('row_button2').style.background='#FF79BC';
        document.getElementById('row_button1').style.background='#6fa8dc';
      }
      else{
        document.getElementById('row_button1').style.background='#FF79BC';
        document.getElementById('row_button2').style.background='#6fa8dc';
      }

      if(obj.monitor=='0'){
        document.getElementById('mon_button1').style.background='#FF79BC';
        document.getElementById('mon_button2').style.background='#6fa8dc';
      }
      else{
        document.getElementById('mon_button2').style.background='#FF79BC';
        document.getElementById('mon_button1').style.background='#6fa8dc';
      }
      
  };
  xhr.send();
}