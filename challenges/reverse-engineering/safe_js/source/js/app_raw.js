/**
 * This is the unobfuscated code to app.js
 *
 * obfuscation was done through https://obfuscator.io
 *
 * key options changed to replicate the challenge:
 * String Transformations > String Array : Disabled
 * Other Transformations > Simplify : Disabled
 */

function f(){
  function typeNumKey(evt){
    var val = evt.target.innerText;
    if(val === "X"){
      document.querySelector("#pass-val").value = "";
      return;
    }

    if(val === "<"){
      document.querySelector("#pass-val").value = document.querySelector("#pass-val").value.slice(0, -1);
      return;
    }

    document.querySelector("#pass-val").value += val;
  }

  async function checkCode(){
    var val = document.querySelector("#pass-val").value;
    var codeCheck = await fetch(`${window.location.origin}/22709856e6053bd4949c64c956bf1ba1`, {
      method: 'POST',
      body: val,
    }).then((res) => {return res.json()});

    if(codeCheck.res){
      // open the safe and get the flag!
      await openSafe();
      return;
    }

    document.querySelector("#pass-val").value = "no";
    await new Promise(resolve => setTimeout(resolve, 1500));
    document.querySelector("#pass-val").value = "";
  }

  function hexToAscii(hex){
    hex = hex.split(' ').join('');
    let fullString = "";
    for(var n = 0; n < hex.length; n += 2){
      fullString += String.fromCharCode(parseInt(hex.substr(n, 2), 16));
    }

    return fullString;
  }

  function flipThemBits(value){
    return (Number.MAX_SAFE_INTEGER - value).toString(16).slice(-value.toString(16).length);
  }

  async function openSafe(){
    var flagJSON = await fetch(`${window.location.origin}/8d724b91d276b37b5e11080821a29624`, {
      method: "POST"
    }).then((res) => {return res.json()});
    var flagHex = "";
    flagJSON.base.forEach((val) => {
      flagHex += flipThemBits(val);
    });
    var flag = hexToAscii(flagHex);

    document.querySelector("#safe-door").classList.add("open");
    document.querySelector("#safe-inner").innerText = flag;
  }

  window["openSafe"] = openSafe;
  window["typeNumKey"] = typeNumKey;
  window["checkCode"] = checkCode;
  window["console.log"] = console.log;
}

window.addEventListener("load", () => {
  f();

  // populate the numpad with appropriate values.
  var buttons = [
    '1', '2', '3',
    '4', '5', '6',
    '7', '8', '9',
    'X', '0', '<',
  ];

  for(var button of buttons){
    let newButton = document.createElement("button");
    newButton.classList.add("numkey");
    newButton.innerText = button;
    newButton.addEventListener("click", (evt) => {typeNumKey(evt)});
    document.querySelector(".numpad").appendChild(newButton);
  }

  document.querySelector("#pass-submit").addEventListener("click", (evt) => {
    evt.preventDefault();
    checkCode()
  });
});
