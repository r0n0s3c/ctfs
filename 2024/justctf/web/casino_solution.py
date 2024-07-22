const seedrandom = require('seedrandom')
const crypto = require('crypto')


for(var i = 10; i < 20; i++) {
    var SERVER_SEED = "8addeebe654ef7c877a9ded64de654d7ca40d5fdf3e3a3350d231169f647803a"
    var CLIENT_SEED = "aaaaaaaaaÊÊaaaaaaaaaaaa" + "\"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00aa" 
    var NONCE = i

    const SERVER_SEED_HASH = "737a40279ae04a6af8ac6ec3a03a055a9f8b944dc440c69570f540fc520b8587"


    if(crypto.createHash("sha256").update(SERVER_SEED).digest("hex") != SERVER_SEED_HASH) {
        console.log("Server seed hash doesn't match server seed hashs")
    }

    let roll = (seedrandom(JSON.stringify({
        serverSeed: SERVER_SEED,
        clientSeed: CLIENT_SEED,
        nonce: NONCE
    })).int32() >>> 0) % 6 + 1

    console.log(NONCE, "Roll result:", roll)
}

for(var i = 20; i < 30; i++) {
    var SERVER_SEED = "8addeebe654ef7c877a9ded64de654d7ca40d5fdf3e3a3350d231169f647803a"
    var CLIENT_SEED = "aaaaaaaaaååaaaaaaaaaaaa" + "\"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00aa" 
    var NONCE = i

    const SERVER_SEED_HASH = "737a40279ae04a6af8ac6ec3a03a055a9f8b944dc440c69570f540fc520b8587"


    if(crypto.createHash("sha256").update(SERVER_SEED).digest("hex") != SERVER_SEED_HASH) {
        console.log("Server seed hash doesn't match server seed hashs")
    }

    let roll = (seedrandom(JSON.stringify({
        serverSeed: SERVER_SEED,
        clientSeed: CLIENT_SEED,
        nonce: NONCE
    })).int32() >>> 0) % 6 + 1

    console.log(NONCE, "Roll result:", roll)
}