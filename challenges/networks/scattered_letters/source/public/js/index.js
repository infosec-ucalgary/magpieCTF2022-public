/**
 * index.js for My First Email Server
 *
 * an experimental email server i'm making while bored because
 * they forgot about their intern :/
 *
 * Note: this version is NOT ready for deployment, patch bugs if
 * this gets deployed.
 */

function init(){
  function chunkToHex(num){
    return ("0" + num.toString(16)).substr(-2);
  }

  function chrToHex(num){
    return chunkToHex(num.charCodeAt(0));
  }

  function textToHex(text){
    return text.split('').map(chrToHex);
  }

  function saltDetails(username, password, registrationDate){
    let salt = textToHex(registrationDate.getTime().toString());

    let mixedString = [];
    let splitPass = textToHex(password);
    let splitUser = textToHex(username);

    for(let i in splitPass){
      mixedString.push(splitPass[i]);
      if(!splitUser[i]) continue;
      mixedString.push(splitUser[i]);
    }

    // store the salted value elsewhere
    password = mixedString
      .map((m, n) => m ^ salt[n])
      .map(chunkToHex)
      .join('');

    return password;
  }

  async function checkCredentials(){
    let username = document.querySelector("#email").value;
    let password = document.querySelector("#password").value;

    const loginResponseDiv = document.querySelector("#login-response");

    let query = `?username=${username}`;
    let epoch = await fetch(`${window.location.origin}/api/v0/getdate${query}`,
      {method: "POST"}
    ).then((res) => {return res.json()});
    console.log("epoch", epoch);

    // clear response box if needed
    loginResponseDiv.innerHTML = "";

    if(epoch.success === false){
      // username does not exist

      // State response
      let response = document.createElement("p");
      response.innerText = `User "${username}" not found`;
      loginResponseDiv.appendChild(response);
      console.log("user doesn't exist");
      return;
    }

    let date = new Date(Number(epoch.time));

    let salt = saltDetails(username, password, date);

    query = `username=${username}&salt=${salt}`;

    let auth = await fetch(`${window.location.origin}/api/v0/login?${query}`,
      {method: "POST"}
    ).then((res) => {return res.json()});

    if(!auth.success){
      // failed credentials

      // State response
      let response = document.createElement("p");
      response.innerText = "Incorrect password";
      loginResponseDiv.appendChild(response);
      console.log("incorrect password");
      return;
    }

    // correct credentials
    console.log("logged in");
    window.localStorage.setItem("user", auth.auth);
    window.location.href = "/email";
  }

  window["checkCredentials"] = checkCredentials;

  document.querySelector("#login").addEventListener("submit", async (evt) => {
    evt.preventDefault();
    await checkCredentials();
  });
}

window.addEventListener("load", init);
