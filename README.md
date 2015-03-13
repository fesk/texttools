text tools
========

Python - tools for analysing and manipulating text.

_passwordy.py_ - Given a single word or a file containing a list of words, output a list of
common permutations of the word or all words within the file.

_wordliststats.py_ - Given one or more files containing lists of words (one per line, such as username or password lists),
output top ten most frequent words and letters.


*Usage*


```
$ python passwordy.py [-options] WORDORFILENAME1 WORDORFILENAME2 ...

where each WORDORFILENAMEx is EITHER a single word (in single quotes) or is a file with one-per-line lists of words (usernames, passwords etc.)

At least one file must be given

 Valid options:
   a  - allow single-character words
   l  - display licence text
   0  - DO NOT include suffixes of 0-9 (default is to include)   4  - include suffixes of 0-9999   6  - include suffixes of 0-999999   i  - placeholder - use if you have a filename beginning with a dash and add filename as normal after options.

 e.g. "$ python passwordy.py -a myfile.txt"

 ```
 
 ```
$ python wordliststats.py [-options] FILENAME1 FILENAME2 ...

where each FILENAMEx is a file with one-per-line lists of words (usernames, passwords etc.)

At least one file must be given

 Valid options:
   a  - include single-character words
   l  - display licence text
   i  - placeholder - use if you have a filename beginning with a dash and add filename as normal after options.
   s  - silence word count output (increases speed)

 e.g. "$ python wordliststats.py -as myfile.dic"
 
 ```