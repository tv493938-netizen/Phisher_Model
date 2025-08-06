chrome.storage.local.get('phishingResult', function(data) {
  const verdictBox = document.getElementById("verdict");
  const result = data.phishingResult;

  if (result === "phishing") {
    verdictBox.textContent = "⚠️ Phishing";
    verdictBox.style.color = "red";
  } else if (result === "safe") {
    verdictBox.textContent = "✅ Safe";
    verdictBox.style.color = "green";
  } else if (result === "suspicious") {
    verdictBox.textContent = "⚠️ Suspicious";
    verdictBox.style.color = "orange";
  } else {
    verdictBox.textContent = "URL not scanned.";
    verdictBox.style.color = "gray";
  }
});
