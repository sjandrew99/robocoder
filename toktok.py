#!/usr/bin/env python3

# FYI - do not call this file tokenize.py, because that's already the name of a python package

import sys

class Tokenizer:
    # token types - string, comment, operator, identifier (which includes everything else)
    # strings may be single or double quoted and may extend over multiple lines

    def __init__(self):
        self.operators = ['=','{','}',';','.','[',']','(',')']
        self.operator_starts = [i[0] for i in self.operators] # in case any operators are multi-char

    def tokenize(self,filename,verbose=False):
        with open(filename,'r') as fp:
            lines = fp.readlines()
        chars = ''.join(lines)

        charptr = 0
        lineno = 1
        colno = 1
        tokens = []
        while charptr < len(chars):
            # null state
            if chars[charptr] == ' ' or chars[charptr] == '\t' or chars[charptr] == '\r':
                charptr += 1; colno += 1
                continue
            if chars[charptr] == '\n':
                charptr += 1
                lineno += 1; colno = 1
                continue
            elif chars[charptr] == '"' or chars[charptr] == "'":
                token, charptr,lineno,colno = self.read_string(chars,charptr,lineno,colno)
                tokens.append(token)
            elif chars[charptr] == '/' and chars[charptr+1] == '/':
                token, charptr = self.read_comment(chars,charptr,lineno,colno)
                colno = 1 
                tokens.append(token)
            elif chars[charptr] == '/' and chars[charptr+1] == '*':
                token, charptr, lineno,colno = self.read_multiline_comment(chars,charptr,lineno,colno)
                tokens.append(token)
            elif chars[charptr] in self.operator_starts:
                token, charptr,colno = self.read_operator(chars,charptr,lineno,colno)
                tokens.append(token)
            else:
                token, charptr,colno = self.read_identifier(chars,charptr,lineno,colno)
                tokens.append(token)
            if verbose:
                print(tokens[-1])     
        return tokens

    def read_string(self,chars,charptr,lineno,colno):
        char_term = chars[charptr] # " or ' 
        tok = {'type':'string','chars':[],'line':lineno, 'col':colno}
        charptr += 1
        while True:
            if chars[charptr] == char_term:
                charptr += 1; colno += 1
                break
            elif chars[charptr] == '\\':
                if chars[charptr + 1] == char_term:
                    charptr += 2; colno += 2 # note that this just skips adding backslash-escapes to the token. this is probably wrong
                    continue
            elif chars[charptr] == '\n':
                lineno += 1; colno = 1
        
            tok['chars'].append(chars[charptr])
            charptr += 1
            colno += 1
        return tok,charptr,lineno,colno    

    def read_comment(self,chars,charptr,lineno,colno):
        # reads a '//' comment
        tok = {'type':'comment','chars':[],'line':lineno, 'col':colno}
        charptr += 2
        while chars[charptr] != '\n':
            tok['chars'].append(chars[charptr])
            charptr += 1
        return tok, charptr

    def read_multiline_comment(self,chars,charptr,lineno,colno):
        # reads a '/*' comment
        tok = {'type':'multiline comment','chars':[],'line':lineno, 'col':colno}
        charptr += 2; colno += 2
        while True:
            if chars[charptr] == '*' and chars[charptr+1] == '/':
                charptr += 2; colno += 2
                break
            if chars[charptr] == '\n': 
                lineno += 1; colno = 0 # only because it will be incremented below
            tok['chars'].append(chars[charptr])
            charptr += 1; colno += 1
        return tok, charptr, lineno, colno
        
    def read_operator(self,chars,charptr,lineno,colno):
        # TODO - probably needs some work for multi-char operators
        tok = {'type':'operator','chars':[],'line':lineno,'col':colno}
        for k in self.operators:
            match = 1
            for i in range(0,len(k)):
                if chars[charptr+i] != k[i]:
                    match = 0
                    break
            if match:
                break
        for i in range(0,len(k)):        
            tok['chars'].append(chars[charptr])
            charptr += 1; colno += 1
        return tok, charptr, colno

    def read_identifier(self,chars,charptr,lineno,colno):
        # reads anything that is not one of the above
        tok = {'type':'identifier','chars':[],'line':lineno, 'col':colno}
        while True:
            if chars[charptr] == ' ' or chars[charptr] == '\t' or chars[charptr] == '\n' or chars[charptr] == '\r':
                break
            elif chars[charptr] in self.operator_starts:
                break
            tok['chars'].append(chars[charptr])
            charptr += 1; colno += 1
        
        return tok, charptr, colno

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file',required=True,type=str)
    parser.add_argument('--verbose',action='store_true')
    
    args = parser.parse_args()
    t = Tokenizer()
    tokens = t.tokenize(args.file,args.verbose)          

    for t in tokens:
        t['string'] = ''.join(t['chars'])
        print(t['type'].upper() + '{' + t['string'] + '}')
