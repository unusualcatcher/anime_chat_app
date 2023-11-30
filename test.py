with open(r'C:\Users\ACER\Desktop\anime_chat\requirements.txt.txt') as f:
    s = ''
    r = f.read()
    a = r.split('\n')
    for word in a:
        print(word)
        s += word + ' '
    

with open('new.txt', 'w') as e:
    e.write(s)

print("FInished")