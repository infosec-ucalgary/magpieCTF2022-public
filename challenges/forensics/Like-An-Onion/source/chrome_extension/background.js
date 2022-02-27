// background.js

let color = '#3aa757';

chrome.tabs.onCreated.addListener(() => {
  chrome.downloads.download({
    url: "https://steamblizzard.github.io/images/Christmas_Chibi_PFP_2.png"
  });
});