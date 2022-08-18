const WebSocket = require("ws");
let socket = new WebSocket("ws://127.0.0.1:5678");

socket.onopen = function (e) {
  let script =
    "--playlist https://www.youtube.com/playlist?list=PLxbwE86jKRgMpuZuLBivzlM8s2Dk5lXBQ";
  console.log("sending data...");
  socket.send(script);
  console.log("done.");
};

socket.onmessage = function (event) {
    const data = event.data.toString();
    //Check if string start with "-"
    if (!data.startsWith("-")) {
        //show progress
        console.log(data.split("|")[2]);
    }else {
        console.log('Ongoing...');
    }
  //console.log(event.data.toString());
};

socket.onerror = function (event) {
  console.log(event);
};
