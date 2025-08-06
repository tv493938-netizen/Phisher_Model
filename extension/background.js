chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url.startsWith('http')) {
    fetch("http://localhost:8000/check_url/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: tab.url })
    })
    .then(res => res.json())
    .then(data => {
      chrome.storage.local.set({ phishingResult: data.final_verdict });
    })
    .catch(console.error);
  }
});
