function f(){
  async function sendEmail(){
    let recipient = document.querySelector("#email-to").value;
    let subject = document.querySelector("#email-subject").value;
    let message = document.querySelector("#email-body").value;
    let senderToken = window.localStorage.getItem("user");

    let sender = await fetch(`${window.location.origin}/api/v0/link?token=${senderToken}`, {
      method: "POST",
    }).then((resp) => {
      return resp.json();
    }).then((json) => {
      console.log(json);
      return json.uid
    });

    let currTime = new Date().getTime();

    let query = `to=${recipient}&from=${sender}&subject=${subject}&date=${currTime}`;

    let response = await fetch(`${window.location.origin}/api/v0/sendmessage?${query}`, {
      method: "POST",
      body: message,
    }).then((resp) => {return resp.json();});

    if(!response.success){
      document.querySelector("#send-status").innerText = "Failed to send message";
    }

    document.querySelector("#send-status").innerText = "Sent successfully";
  }

  document.querySelector("#email-compose").addEventListener("submit", (evt) => {
    evt.preventDefault();
    document.querySelector("#send-status").innerText = "Sending...";
    sendEmail();
  });
}

window.addEventListener("load", f);
