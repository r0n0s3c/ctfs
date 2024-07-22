const seedrandom = require('seedrandom')
const crypto = require('crypto')

let users = {}

SERVER_SEED = "832c277599063d98395d8862d1cf747b897ff562160051b16d627de6f8d152f3"
CLIENT_SEED = "f93f1d351615a2abc1594fc86c3acfbc91a84bda2e8db1c60f0be070a4ac9e12"
NONCE = 7

let username = "asçldkaçlskdçaksdç"
let password = "testas"

users[username] = {
    username,
    password,
    balance: 1000,
    nonce: NONCE,
    serverSeed: SERVER_SEED
}



let roll = (seedrandom(JSON.stringify({
    serverSeed: SERVER_SEED,
    CLIENT_SEED,
    nonce: users[username].nonce++
})).int32() >>> 0) % 6 + 1

console.log(roll)