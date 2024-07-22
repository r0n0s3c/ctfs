const seedrandom = require('seedrandom')
const crypto = require('crypto')

// provide values for server seed, client seed and nonce
const SERVER_SEED = "832c277599063d98395d8862d1cf747b897ff562160051b16d627de6f8d152f3" // to get your current server seed click reveal
const CLIENT_SEED = "f93f1d351615a2abc1594fc86c3acfbc91a84bda2e8db1c60f0be070a4ac9e12" 
const NONCE = 6

// provide server seed hash
const SERVER_SEED_HASH = "8e960b44d799ccaa5912ab8e244bc3f4d207109fd19d1894c59acacf341f2c74" 

if(crypto.createHash("sha256").update(SERVER_SEED).digest("hex") != SERVER_SEED_HASH) {
    console.log("Server seed hash doesn't match server seed hashs")
}

let roll = (seedrandom(JSON.stringify({
    serverSeed: SERVER_SEED,
    clientSeed: CLIENT_SEED,
    nonce: NONCE
})).int32() >>> 0) % 6 + 1

console.log("Roll result:", roll)