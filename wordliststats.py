#!/usr/bin/python
"""
Word list summary information tool.  Nick Besant 2013 hwf@fesk.net

Given one or more files containing lists of words (one per line, such as username or password lists),
output top ten most frequent words and letters.

Licenced under the simplified BSD licence;
Copyright 2013, Nick Besant hwf@fesk.net
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies, 
either expressed or implied, of the FreeBSD Project.
"""
import sys
import time

wordlist=[]
letterlist={}
countedwords={}
wordlistlen=0
filecount=0
excludesingle=True
starttime=time.clock()
noisy=True

def usage():
    print 'Usage: python wordliststats.py [-options] FILENAME1 FILENAME2 ...\n\n'\
    'where each FILENAMEx is a file with one-per-line lists of words (usernames, passwords etc.)\n\n'\
    'At least one file must be given\n\n'\
    ' Valid options:\n'\
    '   a  - include single-character words\n'\
    '   l  - display licence text\n'\
    '   i  - placeholder - use if you have a filename beginning with a dash and add filename as normal after options.\n'\
    '   s  - silence word count output (increases speed)\n'\
    '\n e.g. "$ python wordliststats.py -as myfile.dic"\n'
    '\n\n'
    sys.exit()

def analyse(w):
    # split word up into letters to create a count
    if len(w)<2 and excludesingle: return
    for l in w:
        if letterlist.has_key(l):
            letterlist[l]+=1
        else:
            letterlist[l]=1
    # add word to a list and increment count
    if countedwords.has_key(w):
        countedwords[w]+=1
    else:
        countedwords[w]=1

if len(sys.argv)<2:
    usage()

# load list

if sys.argv[1][0]=='-':
    opts=sys.argv[1][1:]
    flist=sys.argv[2:]
    if len(flist)==0 and 'l' not in opts: usage()
else:
    opts=None
    flist=sys.argv[1:]

if opts:
    if 'l' in opts.lower():
        print '\nwordliststats.py - written by Nick Besant 2014-2015 hwf@fesk.net\n'\
            'Released under the simplified BSD licence (see wordliststats.LICENCE)\n\n'
        sys.exit()
    if 'a' in opts.lower():
        excludesingle=False
    if 's' in opts.lower():
        noisy=False

try:
    for f in flist:
        filecount+=1
        wlf=open(f,'r')
        print 'Analysing {0}...'.format(f)
        sys.stdout.flush()
        for wordline in wlf:
            wordline=wordline.strip()
            analyse(wordline)
            wordlistlen+=1
            if noisy: sys.stdout.write('\r{0}'.format(wordlistlen))
        wlf.close()
        print '\rdone ({0}s)\n'.format(time.clock())
        sys.stdout.flush()
except Exception,e:
    print 'Error opening file: {0}'.format(e)
    sys.exit()

print '{0} files(s) loaded, total {1} words\n------------------------\n'.format(filecount,wordlistlen)

print 'Sorting lists...',
sys.stdout.flush()

# sort letter list
sortedletters=sorted(letterlist.items(), key=lambda x: x[1],reverse=True)[0:10]
# sort word list
sortedwords=sorted(countedwords.items(), key=lambda x: x[1],reverse=True)[0:10]
print 'done ({0}s)\n'.format(time.clock())

print 'Total word count: {0}, unique words {1}'.format(wordlistlen,len(countedwords))
print 'Top ten most frequent words;'
for w in sortedwords:
    print ' "{0}" ({1})'.format(w[0],w[1])
print '\nTop ten most frequent letters;'
for l in sortedletters:
    print ' {0} ({1})'.format(l[0],l[1])
print '\nFinished ({0}s)'.format(time.clock())