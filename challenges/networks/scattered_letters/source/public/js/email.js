function init(){
  async function getEmails(uid){
    let query = `uid=${uid}`;

    let response = await fetch(`${window.location.origin}/api/v0/listemails?${query}`, {
      method: "POST"
    }).then((resp) => {return resp.json()});

    let respMessages = response.messages;

    if(!response.success){
      console.error("fail");
      // clear everything
      document.querySelector("#email-subject").innerText = "";
      document.querySelector("#email-sender").innerText = "";
      document.querySelector("#email-date").innerText = "";
      document.querySelector("#email-body").innerText = "";

      let errorElement = document.createElement("div");
      errorElement.id = "body-init";
      errorElement.innerText = "An error has occurred. Please try again.\n(If this error persists, contact a challenge administrator.)"
      document.querySelector("#email-body").appendChild(errorElement);
      return;
    }

    for(var messageId in respMessages.ids){
      var subject = respMessages.ids[messageId].subject;
      var sender = respMessages.ids[messageId].sender;

      var newLink = document.createElement("a");
      newLink.classList.add("email-link");
      newLink.id = messageId;

      newLink.addEventListener("click", (evt) => {
        var mid = evt.target.id? evt.target.id : evt.target.parentElement.id;
        readEmail(uid, mid)}
      );
      newLink.innerHTML = `<h3>${subject}</h3><br /><i>${sender}</i>`;

      document.querySelector("#email-list").appendChild(newLink);
    }
  }

  async function getUId(token){
    let query = `token=${token}`;

    let response = await fetch(`${window.location.origin}/api/v0/link?${query}`,{
      method: "POST",
    }).then((resp) => {return resp.json()});

    if(!response.success){
      window.location.href = "/";
      return "";
    }

    return response.uid;
  }

  async function readEmail(uid, mid){
    let query = `uid=${uid}&mid=${mid}`;
    let response = await fetch(`${window.location.origin}/api/v0/reademail?${query}`, {
      method: "POST",
    }).then((resp) => {return resp.json()});

    if(!response.success){
      console.log("fail");
      // clear everything
      document.querySelector("#email-subject").innerText = "";
      document.querySelector("#email-sender").innerText = "";
      document.querySelector("#email-date").innerText = "";
      document.querySelector("#email-body").innerText = "";

      let errorElement = document.createElement("div");
      errorElement.id = "body-init";
      errorElement.innerText = "An error has occurred. Please try again.\n(If this error persists, contact a challenge administrator.)"
      document.querySelector("#email-body").appendChild(errorElement);
      return;
    }

    document.querySelector("#email-subject").innerText = response.subject;
    document.querySelector("#email-sender").innerText = `From: ${response.sender}`;
    document.querySelector("#email-date").innerText = `(${new Date(parseInt(response.date)).toLocaleString()})`;
    document.querySelector("#email-body").innerText = response.message;
}

  async function main(){
    if(window.localStorage.getItem("user") === null){
      window.location.href = "/";
    }

    let token = window.localStorage.getItem("user");
    let uid = await getUId(token);

    document.querySelector("#email-title").innerText = `Emails of ${uid}`;
    getEmails(uid);
  }

  main();
}

window.addEventListener("load", init);
