
string = "aaaaaa"
string2 = "isrveawhobpnutfg"
wanted = "giants"
i = 1
res = ""
for count , c in enumerate(string):
    while (string2[ord(c) & 0xf] != wanted[count]):
        c = chr(ord(c) + 1)
    res = res + c

print (res)

