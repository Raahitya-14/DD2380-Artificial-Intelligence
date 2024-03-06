#!/usr/bin/env python3
import sys

def readInp():
    transitionM = strToMatrix(sys.stdin.readline())
    emissionM = strToMatrix(sys.stdin.readline())
    ispd = strToMatrix(sys.stdin.readline())
    return transitionM, emissionM, ispd

def strToMatrix(line):
    nums = [float(n) for n in line.split()] 
    rows = int(nums[0])
    cols = int(nums[1])
    matrix =[[0]*cols for x in range(rows)]
    for i in range(0, rows):
        for j in range(0, cols):
            matrix[i][j]=nums[(cols*i)+j+2]
    return matrix

def matrixToStr(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    mStr = str(rows) + " " + str(cols)
    for i in range(0, rows):
        for j in range(0, cols):
            mStr += " " + str(matrix[i][j])
    return mStr

def matrixMul(m1, m2):
    rows = len(m1)
    cols = len(m2[0])
    productM = [[0]*cols for x in range(rows)]
    for i in range(0, len(m1)):
        for j in range(0, len(m2[0])):
            p = 0
            for k in range(0, len(m2)):
                p += m1[i][k] * m2[k][j]
            productM[i][j] = p
    return productM

def main():
    A, B, Pi = readInp()
    resM = matrixMul(matrixMul(Pi, A), B)
    print(matrixToStr(resM))
    
if __name__ == "__main__":
    main()