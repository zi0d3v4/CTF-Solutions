#!/usr/bin/env python
#Saudi Arabia National Cybersecurity CTF 2021 - ILoveReverse
#python3 code 

key="E`am]Ht`Ws"
ans=[]

for i in range(len(key)):
    a=hex(ord(key[i])+(6-i))
    ans.append(a[2:])

print(bytes.fromhex(''.join(ans)).decode('utf-8'))
exit()
