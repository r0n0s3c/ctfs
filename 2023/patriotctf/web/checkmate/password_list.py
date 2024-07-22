import itertools

letters = ["a","b","c","d","e","f","g","h","i", "j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
f = open("pass.txt", "w+")

'''
combinations = []
for a in range(len(letters)):
    string = letters[a]
    for b in range(len(letters)):
        string = string + letters[b]
        for c in range(len(letters)):
            string = string + letters[c]
            for d in range(len(letters)):
                string = string + letters[d]
                for e in range(len(letters)):
                    string = string + letters[e]
                    for f in range(len(letters)):
                        string = string + letters[f]

'''


# Generate all possible 6-letter words
all_possible_words = [''.join(p) for p in itertools.combinations_with_replacement(letters, 6)]
for word in all_possible_words:
    if word == "aabcae":
        print("found")
    #print(word)

'''
combinations = map(''.join, (itertools.combinations_with_replacement(letters, 6)))
for string in combinations:
    f.write(string + "\n")
    
    if((ord(string[0]) & ord(string[2])) == int(0x60)):
        if((ord(string[1]) | ord(string[4])) == int(0x61)):
            if((ord(string[3]) ^ ord(string[5])) == int(0x6)):
                print(string)
                f.write(string + "\n")
'''   