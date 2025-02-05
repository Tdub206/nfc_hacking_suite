const socket = new WebSocket("ws://localhost:5000");

socket.onmessage = function(event) {
    const log = document.getElementById("nfc-log");
    const listItem = document.createElement("li");
    listItem.textContent = event.data;
    log.appendChild(listItem);
};

document.getElementById("start-sniffing").addEventListener("click", () => {
    fetch("/start_sniffing").then(response => console.log("NFC sniffing started"));
});

document.getElementById("stop-sniffing").addEventListener("click", () => {
    fetch("/stop_sniffing").then(response => console.log("NFC sniffing stopped"));
});
