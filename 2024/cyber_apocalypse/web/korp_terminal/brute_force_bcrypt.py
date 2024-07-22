import bcrypt
import sys

hash_file = open(sys.argv[1], 'r')
hash_to_crack = hash_file.readline()

file = open(sys.argv[2],'r', encoding='latin-1')
for password in file.readlines():
    #hash_pass = bcrypt.generate_password_hash(password)
    hash_pass = bcrypt.hashpw(password.encode('latin-1'), hash_to_crack.encode('latin-1'))
    print(hash_pass.decode("utf-8") + " - " + password)
    print(str(hash_to_crack))
    if hash_pass.decode("utf-8") in hash_to_crack:
        #same = bcrypt.check_password_hash(hash_pass, 'hunter2') # returns True
        #bcrypt.hashpw(password.encode('latin-1'), hash.encode('latin-1'))
        print("We found it!")
        break    
