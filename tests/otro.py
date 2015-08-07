#!/usr/bin/python

def getPermutations(string, prefix=""):
    if len(string) == 1:
        yield prefix + string
    else:
        for i in range(len(string)):
            for perm in getPermutations(string[:i] + string[i+1:], prefix+string[i]):
                yield perm


for i in getPermutations('lac'):
	print i