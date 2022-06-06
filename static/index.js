function jump() {
    
    alert('即將跳轉頁面');
    window.location.replace("/");
      
  };

  function jump2() {
    
    //alert('即將跳轉頁面');
    window.location.replace("/control");
      
  };

  function control(cmd) {
    var xhr = new XMLHttpRequest();
    var url = "cmd/" + cmd;
    xhr.open("POST", url);
    xhr.send();
    console.log(cmd)
      
  };


