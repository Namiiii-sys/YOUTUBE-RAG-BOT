chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "GET_CURRENT_TAB_URL") {
    
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const url = tabs[0]?.url || "";
      console.log("Active Tab URL:", url);
      sendResponse({ url });
    });

    return true;
  }
});
