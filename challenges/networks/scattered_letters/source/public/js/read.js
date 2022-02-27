function init(){
  async function readEmail(){
    let query = window.location.search.substr(1) // remove '?' for consistency

    let response = await fetch(`${window.location.origin}/api/v0/reademail?${query}`, {
      method: "POST",
    }).then((resp) => {return resp.json()});

    if(!response.success){
      console.log("fail");
      return;
    }

    document.querySelector("#email-subject").innerText = response.subject;
    document.querySelector("#email-sender").innerText = response.sender;
    document.querySelector("#email-date").innerText = response.date;
    document.querySelector("#email-body").innerText = response.message;
  }

  readEmail();
}

window.addEventListener("load", init);
