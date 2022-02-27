var plaintext = "this_is{a_test.string}";

function isPrime(num) {
    for(var i = 2; i < Math.sqrt(num); i++)
      if(num % i === 0) return false;
    return num > 1;
  }

function encrypt(plain) {
    var encoded = [];
    rand_prime = Math.floor((Math.random() * 9000) + 1000);
    while (isPrime(rand_prime) !== true) {
        rand_prime = Math.floor((Math.random() * 9000) + 1000);
    }
    for (var n = 0, l = plain.length; n < l; n ++) {
        rand_int = rand_prime * Math.floor((Math.random() * 6) + 1);
        var uni = plain.charCodeAt(n) + rand_int;
        encoded.push(String.fromCharCode(uni));
    }
    return [encoded.join(""), rand_prime];
}

function decrypt(ciphertext, prime) {
    var decoded = [];
    for (var n = 0, l = ciphertext.length; n < l; n ++) {
        var char = ciphertext.charCodeAt(n) % prime;
        decoded.push(String.fromCharCode(char));
    }
    return decoded.join("");
}

const fs = require('fs');

const buffer = fs.readFileSync("./new_vbscnstrct.py");

const fileContent = buffer.toString();
// console.log(fileContent);

var test_python = encrypt(fileContent); 
var decrypted_test = decrypt(test_python[0], test_python[1]); 

console.log(test_python[0]); // Uncomment to print encrypted python text
// console.log(decrypted_test); // Uncomment to print decrypted python text
