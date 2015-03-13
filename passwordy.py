#!/usr/bin/python
"""
Password permutation tool.  Nick Besant 2013 hwf@fesk.net

Given a single word or a file containing a list of words, output a list of
common permutations of the word or all words within the file.

Licenced under the simplified BSD licence;
Copyright (c) 2013, Nick Besant hwf@fesk.net
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
import re
import string
import os

def usage():
    print 'Usage: python passwordy.py [-options] WORDORFILENAME1 WORDORFILENAME2 ...\n\n'\
    'where each WORDORFILENAMEx is EITHER a single word (in single quotes) or is a file with '\
    'one-per-line lists of words (usernames, passwords etc.)\n\n'\
    'At least one file must be given\n\n'\
    ' Valid options:\n'\
    '   a  - allow single-character words\n'\
    '   l  - display licence text\n'\
    '   0  - DO NOT include suffixes of 0-9 (default is to include)'\
    '   4  - include suffixes of 0-9999'\
    '   6  - include suffixes of 0-999999'\
    '   i  - placeholder - use if you have a filename beginning with a dash and add filename as normal after options.\n'\
    '\n e.g. "$ python passwordy.py -a myfile.txt"\n'
    '\n e.g. "$ python passwordy.py -a \'MY_password\'"\n'\
    '\n\n'
    sys.exit()

def _gettrans(wrd,tranlist):
    return wrd.translate(string.maketrans(tranlist[0],tranlist[1]))

def _getcasevariants(wrd,caselist):
    return [wrd.upper(),
            wrd.lower(),
            _gettrans(wrd,caselist)
            ]

def _getsuffixlist(wrd,suffixlist,do1digit=True,do4digit=False,do6digit=False):
    rl=[]
    for s in suffixlist:
        rl.append('{0}{1}'.format(wrd,s))
    domore=False
    if do1digit: domore=9
    if do4digit: domore=9999
    if do6digit: domore=999999
    if domore:
        for s in range(0,domore):
            rl.append('{0}{1}'.format(wrd,s))
            rl.append('{0}{1}'.format(wrd,s).capitalize())
    
    return list(set(rl))


def getsimilarwords(w,suffixlen):

    individualsubs=[['5','s'],
                    ['aA','44'],
                    ['bB','88'],
                    ['eE','33'],
                    ['iI','11'],
                    ['lL','11'],
                    ['oO','00'],
                    ['sS','55'],
                    ['tT','77'],
                    ]
    
    caseflipsubs=['aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ','AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz']
    
    fullnumbersubs=['5aAbBeEiIlLoOsStT','s4488331111005577']
    
    symbolsubs=[['cCiIlLsS','<<||||$$'],
                ['11iIlL','!!!!!!'],
                [' ','_'],
                [' ','.'],
                [' ','-'],
                
                ]
    
    suffixlist=['!',' ','?','=','#']
    stripchars=' aeiou'

    def __getmangled(w,tranlist):
        rl=[]
        rw=_gettrans(w,tranlist)
        rl.append(rw)
        rl.append(rw.capitalize())
        rl.extend(_getcasevariants(rw,caseflipsubs))
        if suffixlen==4:
            rl.extend(_getsuffixlist(rw,suffixlist,do4digit=True))
        elif suffixlen==6:
            rl.extend(_getsuffixlist(rw,suffixlist,do6digit=True))
        elif suffixlen==0:
            rl.extend(_getsuffixlist(rw,suffixlist,do1digit=False))
        else:
            rl.extend(_getsuffixlist(rw,suffixlist))
            
        return rl
    
    # Add the word
    sw=[w]
    # ..and its upper/lower and flipped case versions
    sw.extend(_getcasevariants(w,caseflipsubs))
    # ..and a squashed-up version
    sw.append(w.translate(None,stripchars))
    sw.extend(_getcasevariants(w.translate(None,stripchars),caseflipsubs))

    # First - any digits at the end of the word?
    endre = re.search(r'\d+$', w)
    endno = int(endre.group()) if endre else None
    if endno: 
        # add the word with no end number to the list
        w=w[0:sw.index(endre.group())].strip()
        sw.append(w)
        sw.extend(_getcasevariants(w,caseflipsubs))
    
    # Next - any at the beginning?
    startre = re.search(r'^\d+', w)
    startno = int(startre.group()) if startre else None
    if startno:
        # add the word with no prefix number to the list
        w=w[len(endre.group()):]
        sw.append(w)
        sw.extend(_getcasevariants(w,caseflipsubs))
        
    # w should now not start or end with any digits
    
    # Add version with all common number subs first
    sw.extend(__getmangled(w,fullnumbersubs))
    
    for ns in individualsubs:
        sw.extend(__getmangled(w,ns))
        
    for ss in symbolsubs:
        sw.extend(__getmangled(w,ss))
        
    return list(set(sw))


def main(args):
    
    wordlist=[]
    inputlen=0
    filecount=0
    excludesingle=True
    suffixlen=1
    
    if len(args)<2:
        usage()
    
    # load list
    
    if args[1][0]=='-':
        opts=args[1][1:]
        flist=args[2:]
        if len(flist)==0 and 'l' not in opts: usage()
    else:
        opts=None
        flist=args[1:]
    
    if opts:
        if 'l' in opts.lower():
            print '\npasswordy.py - written by Nick Besant 2013 hwf@fesk.net\n'\
                'Released under the simplified BSD licence (see passwordy.LICENCE)\n\n'
            try:
                print ''.join(open('{0}.LICENCE'.format(args[0].split('.')[0]),'r').readlines())
            except:
                print 'Error: licence file not found.  Please view source for licence.'
                sys.exit()

            sys.exit()
        if 'a' in opts.lower():
            excludesingle=False
        if '0' in opts:
            suffixlen=0
        if '4' in opts:
            suffixlen=4
        if '6' in opts:
            suffixlen=6

    for f in flist:
        filecount+=1
        if os.access(f,os.F_OK):
            wlf=open(f,'r')
        else:
            wlf=f
            
        if isinstance(wlf,file):
            for wordline in wlf:
                wordline=wordline.strip()
                if len(wordline)>1 or not excludesingle:
                    wordlist.extend(getsimilarwords(wordline,suffixlen))
                inputlen+=1
            wlf.close()
        else:
            if len(wlf)>1 or not excludesingle:
                wordlist.extend(getsimilarwords(wlf,suffixlen))
            inputlen+=1

    sys.stdout.flush()
    
    print '\n'.join(wordlist)
    

if __name__ == "__main__":
    main(sys.argv)
