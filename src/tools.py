import numpy as np
import pandas as pd
from time import time
import bitstring as bs

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