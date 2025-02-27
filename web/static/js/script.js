function sendMessage() {
    pywebview.api.greet("User").then(response => {
        document.getElementById("response").innerText = response;
    });
}
