words = open("words.txt", "r")
list_words = [word.strip() for word in words.readlines()]

methods = open("methods.txt", "r")
list_methods = [method.strip() for method in methods.readlines()]

extensions = open("/home/w0rth/SecLists/Discovery/Web-Content/web-extensions.txt", "r")
list_extentions = [extension.strip() for extension in extensions.readlines()]

wordlist = open("wordlist.txt", "w+")
for i in list_methods:
    for j in list_words:
        for k in list_extentions:
            wordlist.write(f"{i}-{j}{k}\n")