function f(){
  function onCommand(){
    let command = document.querySelector("#answer").value;

    addToHistory(`> ${command}`);

    switch(command){
      case("help"):
        writeHelp();
        break;
      case("sites"):
        writeSites();
        break;
      case("solve"):
        // TODO: possibly replace with state variable instead of checking text
        document.querySelector("#answer-prompt").innerHTML = "ciphertext:";
        document.querySelector("#answer-input").onsubmit = (evt) => {
          evt.preventDefault();
          confirmData();
        };
        document.querySelector("#answer").value = "";
        return;
      default:
        addToHistory(`invalid command \"${command}\"`);
        addToHistory("for a list of valid commands, type \"help\"");
        addToHistory(' ');
    }

    document.querySelector("#answer-prompt").innerText = "> ";
    document.querySelector("#answer").value = "";
  }

  async function confirmData(){
    let guess = document.querySelector("#answer").value;
    let state = document.querySelector("#answer-prompt").innerHTML;

    addToHistory(`${state} ${guess}`);
    switch(state){
      case("ciphertext:"):
        sendCipherGuess(guess);
        break;
      case("plaintext:"):
        sendWrittenAnswer(guess);
        document.querySelector("#answer-prompt").innerHTML = "> ";
        document.querySelector("#answer-input").onsubmit = (evt) => {
          evt.preventDefault();
          onCommand();
        };
    }

    document.querySelector("#answer").value = "";
  }

  async function sendCipherGuess(ans){
    let data = {
      answer: ans,
    }

    let response = await fetch(`${window.location.origin}/check-cipher`, {
      method: "POST",
      body: JSON.stringify(data),
    }).then(res => {return res.json()});

    if(response.correct){
      document.querySelector("#answer-prompt").innerHTML = "plaintext:";
      addToHistory(`correct ciphertext`);
      addToHistory(' ');
    }else{
      addToHistory(`incorrect ciphertext: ${ans}`);
      addToHistory(' ');
      document.querySelector("#answer-prompt").innerHTML = "> ";
      document.querySelector("#answer-input").onsubmit = (evt) => {
        evt.preventDefault();
        onCommand();
      };
    }
  }

  async function sendWrittenAnswer(ans){
    let data = JSON.stringify({
      answer: ans,
    });

    addToHistory(`Attempting guess: "${ans}"...`);

    let response = await fetch(`${window.location.origin}/check-plain`, {
      method: "POST",
      body: data,
    }).then((r) => {return r.json()});

    if(!response.correct){
      // handle incorrect response
      addToHistory('Incorrect guess\n ');
      return;
    }

    addToHistory('Correct passphrase\nFetching stored intercept...\n  ');
    let intercept = "", interceptLine = "";
    for(c of response.message.data){
      interceptLine += String.fromCharCode(c);
      if(c === '\n'.charCodeAt(0)){
        addToHistory(interceptLine);
        intercept = interceptLine;
        interceptLine = "";
      }
    }

    console.log(intercept);
    addToHistory(' ');
  }

  function addToHistory(line){
    let lineHTML = document.createElement("pre");
    lineHTML.innerText = line;
    document.querySelector("#history").prepend(lineHTML);
  }

  function writeHelp(){
    addToHistory("help    -  this help menu");
    addToHistory("sites   -  links of importance");
    addToHistory("solve   -  attempt to guess the passphrase");
    addToHistory(" ");
  }

  function writeSites(){
    addToHistory("http://momandpopsflags.ca");
    addToHistory("http://omniflags.com");
    addToHistory(" ");
  }

  document.querySelector("#answer-input").onsubmit = (evt) => {
    evt.preventDefault();
    onCommand();
  };

  let controlPressed = false
  window.addEventListener("keydown", (evt) => {
    if(evt.key.includes("Arrow")){
      return;
    }

    if(evt.key === "Control" || controlPressed){
      controlPressed = true;
      return;
    }
    document.querySelector("#answer").focus();
  });

  window.addEventListener("keyup", (evt) => {
    if(controlPressed && evt.key === "Control"){
      controlPressed = false;
    }
  });
}

window.addEventListener("load", () => {f()});
