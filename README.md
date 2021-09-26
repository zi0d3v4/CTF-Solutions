# Reversing Solutions

Here I put my RE solutions and write-ups
-----
  Saudi Arabia National Cybersecurity CTF 2021
  ---
  I didn't participate in the CTF in person but I received below challenge from the CTf in the day following to the CTF's deadline (The challenge was more than this but I just recieved the RE part of it which is the final stage to get the flag). It is more of a Crypto than RE (it seems CTF organizers either do not understand what Reverse Engineering is all about or they do not know how to create real RE challenges rather than Crypto ROTx-like / pwn stuff). Enough of wasting E-Inks :d, Let's begin:
  
  File command is my first go to for files :)
  ![image](https://user-images.githubusercontent.com/75640323/134824159-ffdc467f-275b-40a9-b8fb-7ed550c033bc.png)
  
  x64 ELF, not stripped, dynamically linked. 
  
  Let's take a binwalk:
![image](https://user-images.githubusercontent.com/75640323/134824665-1551b571-addc-43b6-aaaf-afc3b21e624a.png)
 //I tried `dd bs=13612 skip=1 if=ILoveReverse of=iluvre` to strip the include file but ended up following a rabbit hole.
  
  and do a checksec :
  
  ![image](https://user-images.githubusercontent.com/75640323/134824228-cd25351f-e548-4b7b-bead-0c7069cbe932.png)

  We got NX & PIE enabled. Let's not panik ... yet
  
  It is dynamically linked, isn't it?
  ![image](https://user-images.githubusercontent.com/75640323/134824904-2085bff4-6cc3-4b97-ba7b-c2d17d458616.png)

  I will gather some strings now.
  
<!-----
/lib64/ld-linux-x86-64.so.2
puts
printf
strlen
__cxa_finalize
__libc_start_main
libc.so.6
GLIBC_2.2.5
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
u/UH
[]A\A]A^A_
Need exactly one argument.
E`am]Ht`Ws
____            ____
_,',--.`-.      _,',--.`-.
<_ ( () )  >  ( <_ ( () )  >
`-:__;,-'    \  `A:__:,-'
\ / \
((  )
\-'
\
\
(           )
`-'"`-----'
.-'''/.\ 
(_.--'  |      <<< Your flag is: flag{%s}
|  ==  |
o-._ .--..--. _.-o
|   ||   |
;--|`--:
|. |   |
|  ;_ .|
|_____ |
/|     '|\
//`----'\\
////|  |  \\
/   |  |    \
/|  |\
/ \  / \
/   \/   \
/          \
|          |
||    /\    ||
||   ,  .   || 
;*3$"
GCC: (Debian 9.3.0-18) 9.3.0
/usr/lib/gcc/x86_64-linux-gnu/9/include
/usr/include/x86_64-linux-gnu/bits
/usr/include/x86_64-linux-gnu/bits/types
/usr/include
Enjoy_rev.cpp
stddef.h
types.h
struct_FILE.h
FILE.h
stdio.h
sys_errlist.h
_IO_buf_end
Enjoy_rev.cpp
_old_offset
_IO_save_end
short int
size_t
_IO_write_ptr
_flags
_IO_buf_base
_markers
_IO_read_end
_freeres_buf
GNU C++14 9.3.0 -mtune=generic -march=x86-64 -g -fasynchronous-unwind-tables
_sys_errlist
stderr
_lock
long int
_cur_column
_sys_nerr
argv
_IO_FILE
unsigned char
argc
_IO_marker
_shortbuf
_IO_write_base
_unused2
_IO_read_ptr
short unsigned int
main
_freeres_list
/root/Desktop
correct
__pad5
_IO_codecvt
long unsigned int
_IO_write_end
__off64_t
__off_t
_chain
_IO_wide_data
_IO_backup_base
stdin
_flags2
_mode
_IO_read_base
_vtable_offset
_IO_save_base
_fileno
stdout
_IO_lock_t
crtstuff.c
deregister_tm_clones
__do_global_dtors_aux
completed.7454
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
Enjoy_rev.cpp
__FRAME_END__
__init_array_end
_DYNAMIC
__init_array_start
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_csu_fini
_ITM_deregisterTMCloneTable
puts@@GLIBC_2.2.5
_edata
strlen@@GLIBC_2.2.5
printf@@GLIBC_2.2.5
__libc_start_main@@GLIBC_2.2.5
__data_start
__gmon_start__
__dso_handle
_IO_stdin_used
__libc_csu_init
__bss_start
main
__TMC_END__
_ITM_registerTMCloneTable
__cxa_finalize@@GLIBC_2.2.5
.symtab
.strtab
.shstrtab
.interp
.note.gnu.build-id
.note.ABI-tag
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.plt.got
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.dynamic
.got.plt
.data
.bss
.comment
.debug_aranges
.debug_info
.debug_abbrev
.debug_line
.debug_str
!------>

There are many interesting info. 
 [Need exactly one argument.
 E`am]Ht`Ws
<<< Your flag is: flag{%s}
Enjoy_rev.cpp] 
these are the most interesting strings to me.
I know we need exactly one argv, interesting string (some sort of key), flage is %s (maybe a format string vuln but cant happen within one arg!!) or maybe just a printf string format parameter %s (which means our input is inserted between flag{ and }) , and a cpp file.

I was thinking maybe embedded file ? 

![image](https://user-images.githubusercontent.com/75640323/134825164-ab6ab64b-34bf-43d6-b854-6a878d46c298.png)


I objdumped it but got no clues (sorry for my laziness), Same with GDB, I found main is not loaded in functions but rather is called from within the c++ file. I tried to play with gdb but I got bored and lazy (long work-day :( so, I went ahead in the process and fired up ghidra and went for the main function pseudo code.

![image](https://user-images.githubusercontent.com/75640323/134825736-8cfea1d4-18aa-41e8-979f-26a7eabf6815.png)

a very simple easy flag wavering in the sky here.
1) our interesting Key string of length of 10 bytes.
2) check len(input)==len(key)==10 bytes/chars
  2.1) Yes ==> check foreach (((char in key) + 6) - current position) == corresponding char in INPUT
    2.1.1) No ==> Big No face
    2.1.2) yes ==> Print("flag is: flag{OUR_INPUT}")  (squre#3)
  2.2) No ==> Big No face
  2.3) else (No input) ==> msg(Need an arg)
  
  
  So, after understanding the code flow let's build a decryptor (YES IT IS A STUPID CRYPTO rather than a RE challenge)
  
  Givings:
    key="E`am]Ht`Ws"
    algorithm => key[i]+6-i = answer[i]
    
  Methodology:
  a) convert Ascii to Hex
  b) apply algorithm to each byte
  c) insert result in an array 
  d) print array as a string to be our input
  
  Code: Python3
  
  ![image](https://user-images.githubusercontent.com/75640323/134826215-f0a436ae-fa24-4923-b9f1-1c84768b7bb1.png)

  Solution:
  ![image](https://user-images.githubusercontent.com/75640323/134826271-242fd60c-bef1-4119-a9e2-104195313a8f.png)





