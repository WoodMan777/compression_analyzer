import numpy as np
import pandas as pd
from time import time
import bitstring as bs
import yaml

def getFastMarkovMatrix(binfile):
    count = np.zeros((2**8, 2**8), dtype = "float64")
    
    for i in range(len(binfile)-1):
        count[binfile[i]][binfile[i+1]] += 1
    
    return count / len(binfile)

def getMarkovMatrix(bits, blockSize):
    count = np.zeros((2**blockSize, 2**blockSize), dtype = "float64")
    
    padding = blockSize - len(bits)%(blockSize)
    bits += '0'*padding
    
    blockCount = len(bits) // blockSize
    
    for i in range(blockCount - 2):
        tmpa = bits[(blockSize)*i : (blockSize)*(i+1)]
        tmpb = bits[(blockSize)*(i+1) : (blockSize)*(i+2)]
        
        count[int(tmpa,2)][int(tmpb,2)] += 1
    
    return count / ((blockCount)-1)

def getSuperFastBinString(binf):
    return bs.BitArray(binf).bin

def getMarkovRandomness(matrix):
    threshold = np.percentile(matrix, 95)
    metric = 0
    for i in np.ravel(matrix):
        if i >= threshold:
            metric += i
    return metric

def cartesianMultiplication(a,b):
    res = []
    for i in a:
        for j in b:
            res.append(i+' '+j)
    return res

def generateAllCmdStrings(exepath, ymlfile):
    res = []
    for test in ymlfile.keys():
        params = {}
        for param in ymlfile[test].keys():
            if 'bool' in str(type(ymlfile[test][param])):
                params[param] = True
            elif ',' in ymlfile[test][param] and '-' in ymlfile[test][param]:
                print("ERR: One (or few) parameters contain ',' and '-' at the same time!")
                return None
            elif ',' in ymlfile[test][param]:
                tmp = ymlfile[test][param].split(',')
                tmp = list(map(lambda x: param+x, tmp))
                params[param] = tmp
            elif '-' in ymlfile[test][param]:
                tmp = ymlfile[test][param].split('-')
                tmp2 = []
                for i in range(int(tmp[0]),int(tmp[1])+1):
                    tmp2.append(f"{param}{i}")
                params[param] = tmp2
        
        singular = []
        for param in params.keys():
            if params[param] == True:
                singular.append(param)
        
        singular = ' '.join(singular)
        singular = [singular]
        
        for param in params.keys():
            if params[param] != True:
                singular = cartesianMultiplication(singular, params[param])
        
        res += singular
    res = list(map(lambda x: exepath+" "+x, res))
    return res