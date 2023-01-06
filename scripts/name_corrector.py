import os
import sys
stringToMatch = 'getme'
directory = 'ft_fun'
sys.setrecursionlimit(10000)
history = ["ok","ok"]
for filename in os.listdir(directory):
    fd = open(directory+'/'+filename, 'r');
    with fd as file:
        for line in file:
            if  "//file" in line:
                print("mv "+ filename + " " + line.replace('//file', ''))