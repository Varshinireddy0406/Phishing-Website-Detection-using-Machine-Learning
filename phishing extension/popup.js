chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const currentUrl = tabs[0].url;
    document.getElementById("url").textContent = "URL: " + currentUrl;

    fetch("http://127.0.0.1:5000/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: "url=" + encodeURIComponent(currentUrl)
    })
    .then(response => response.text())
    .then(html => {
        if (html.includes("Safe")) {
            document.getElementById("result").textContent = "✅ This site is Safe";
            document.getElementById("result").className = "status safe";
        } else if (html.includes("Unsafe")) {
            document.getElementById("result").textContent = "❌ Phishing site detected!";
            document.getElementById("result").className = "status unsafe";

        } else {
            document.getElementById("result").textContent = "⚠️ Unable to predict";
        }
    })
    .catch(error => {
        console.error(error);
        document.getElementById("result").textContent = " Could not connect to model";
    });
});
