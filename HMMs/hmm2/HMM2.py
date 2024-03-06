import sys

def readInp():
    transitionM = strToMatrix(sys.stdin.readline())
    emissionM = strToMatrix(sys.stdin.readline())
    ispd = strToMatrix(sys.stdin.readline())
    line = list(map(int, sys.stdin.readline().split()))
    numEmi = line[0]
    seq = line[1:]
    return transitionM, emissionM, ispd, numEmi, seq

def strToMatrix(line):
    nums = [float(n) for n in line.split()] 
    rows = int(nums[0])
    cols = int(nums[1])
    matrix =[[0]*cols for x in range(rows)]
    for i in range(0, rows):
        for j in range(0, cols):
            matrix[i][j]=nums[(cols*i)+j+2]
    return matrix

def viterbi(m1, m2, ispd, numEmi, seq):
    deltaM = [[0] * len(m1) for x in range(0, numEmi)]
    idxM = [[0] * len(m1) for x in range(0, numEmi)]
    for i in range(0, len(m1)): 
        deltaM[0][i] = ispd[0][i] * m2[i][seq[0]]

    for i in range(1, numEmi):
        for j in range(0, len(m1)):
            prob, idx = 0, 0
            for k in range(0, len(m1)):
                d = m1[k][j] * deltaM[i-1][k] * m2[j][seq[i]]
                if d > prob:
                    prob = d
                    idx = k
            deltaM[i][j] = prob
            idxM[i][j] = idx

    prob, idx = 0, 0
    for i in range(0, len(m1)):
        p = deltaM[numEmi-1][i]
        if p > prob:
            prob = p
            idx = i

    states = [idx]
    for i in range(numEmi-1, 0, -1):
        idx = idxM[i][idx]
        states.append(idx)
    return states[::-1]

def main():
    A, B, Pi, numEmi, seq = readInp()
    states = viterbi(A, B, Pi, numEmi, seq)
    output = ""
    for i in range(0, len(states)):
        if i == 0:
            output += str(states[i])
        else:
            output += " "+str(states[i])
    print(output)

if __name__ == "__main__":
    main()