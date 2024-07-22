// Node.js program to demonstrate the
// process.argv Property
   
// Include process module
const process = require('process');

var letters = ["a","b","c","d","e","f","g","h","i", "j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

function checkName(name){
    var check  = name.split("").reverse().join("");
    return check === "uyjnimda" ? !0 : !1;
}

function checkLength(pwd){
     return (password.length % 6 === 0 )? !0:!1;
    }

function checkValidity(password){
    const arr = Array.from(password).map(ok);
    console.log(arr)
    function ok(e){ 'password is letters only'
        if (e.charCodeAt(0)<= 122 && e.charCodeAt(0) >=97 ){
        return e.charCodeAt(0);
    }}

    let sum = 0;
    for (let i = 0; i < arr.length; i+=6){
        var add = arr[i] & arr[i + 2]; 
        console.log(add)
        var or = arr[i + 1] | arr[i + 4];
        console.log(or)
        var xor = arr[i + 3] ^ arr[i + 5];
        console.log(xor)
        if (add === 0x60   && or === 0x61   && xor === 0x6) sum += add + or - xor; 
    }
    console.log(sum)
   return  sum === 0xbb ? !0 : !1;
}

var args = process.argv;
var username = args[2]
var password = args[3]
console.log(username)
console.log(password)


if(!(checkName(username))){         
    console.log('Incorrect Name! 😥😥')
}
else{
      console.log('Correct Name! 🙂🙂')
}

console.log(!checkLength(password))
if(!checkValidity(password) && !checkLength(password)){
    console.log('Incorrect Password! 😥😥')
}
else{
    console.log('Correct Password! 🙂🙂')
}


