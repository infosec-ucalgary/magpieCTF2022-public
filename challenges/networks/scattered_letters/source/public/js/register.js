/**
 * register.js for My First Email Server
 *
 * allows users to register an email with the system
 */

function init(){
  // may be modified by administrator in the future
  const domain = "mompopsflags.com";

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

  function passwordMatches(){
    return document.querySelector("#password").value == document.querySelector("#confirm-password").value;
  }

  async function registerUser(){
    const registrationCall = "/api/v0/register";
    let registrationDate = new Date();
    let username = `${document.querySelector("#email").value}@${domain}`;
    let password = document.querySelector("#password").value;

    if(!passwordMatches()){
      document.querySelector("#send-status").innerText = "Registration failed - passwords do not match";
      return;
    }

    let salt = saltDetails(username, password, registrationDate);

    let query =
      `username=${username}&salt=${salt}&time=${registrationDate.getTime().toString()}`;

    let url = `${window.location.origin}${registrationCall}?${query}`;

    let response = await fetch(url, {
      method: "POST"
    }).then((resp) => {return resp.json()});

    if(!response.success){
      document.querySelector("#send-status").innerText = `Registration failed - ${response.message}`;
      return;
    }

    window.location.href = "/";
  }

  // Ensure user doesn't add an invalid character to their username
  function checkInput(evt){
    let emailRegex = /[A-Za-z0-9.\-_]+/
    return emailRegex.test(evt.key);
  }

  // set the click event of the register button
  document.querySelector("#register-submit").addEventListener("click", (evt) => {
    evt.preventDefault();
    registerUser();
  });

  // write the stored domain
  document.querySelector("#domain").innerText = `@${domain}`;

  // set input checking
  document.querySelector("#email").onkeypress = checkInput;
}

window.addEventListener("load", init);
