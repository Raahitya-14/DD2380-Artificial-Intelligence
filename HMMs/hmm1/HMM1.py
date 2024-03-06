import sys

def readInp():
    transitionM = strToMatrix(sys.stdin.readline())
    emissionM = strToMatrix(sys.stdin.readline())
    ispd = strToMatrix(sys.stdin.readline())
    emmissionSeq = []
    for x in sys.stdin.readline().split():
        emmissionSeq.append(int(x))
    return transitionM, emissionM, ispd, emmissionSeq[1:]
    
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

def alphapass(m1, m2, ispd, seq):
    alphaM = [[0]*len(m1) for x in range(0, len(seq))]
    for i in range(0, len(seq)):
        for j in range(0, len(m1)):
            if i == 0:
                alphaM[i][j] = ispd[0][j] * m2[j][seq[0]]
            else:
                aSum = 0
                for k in range(0, len(m1)):
                    aSum += alphaM[i-1][k] * m1[k][j]
                alphaM[i][j] = m2[j][seq[i]] * aSum 
    finalProb = 0
    for i in alphaM[len(alphaM)-1]:
        finalProb += i
    return finalProb

def main():
    A, B, Pi, seq = readInp()
    result = alphapass(A, B, Pi, seq)
    print(result)

if __name__ == "__main__":
    main()