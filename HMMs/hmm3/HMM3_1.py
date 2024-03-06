import sys
import math

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
    matrix =[[0]*cols for x in range(0, rows)]
    for i in range(0, rows):
        for j in range(0, cols):
            matrix[i][j]=nums[(cols*i)+j+2]
    return matrix

def matrixToString(matrix):
    string = str(len(matrix)) + " "
    string += str(len(matrix[0]))
    for row in matrix: 
        for value in row:
            string += " {:.6f}".format(value)
    return string

def alphapass(m1, m2, ispd, seq):
    T = len(seq)
    N = len(m1)

    # Initialize
    alpha = [[0]*N for x in range(0, T)]
    c = [0]*T
    for i in range(0, N):
        alpha[0][i] = ispd[0][i] * m2[i][seq[0]]
        c[0] += alpha[0][i]

    c[0] = 1/c[0]
    for i in range(0, N):
        alpha[0][i] = c[0] * alpha[0][i]
    
    # Compute rest of alpha
    for t in range(1, T):
        c[t] = 0
        for i in range(0, N):
            alpha[t][i] = 0
            for j in range(0, N):
                alpha[t][i] += alpha[t-1][j] * m1[j][i]
            alpha[t][i] = alpha[t][i] * m2[i][seq[t]]
            c[t] += alpha[t][i]
        
        c[t] = 1/c[t]
        for i in range(0, N):
            alpha[t][i] = c[t] * alpha[t][i]
    return alpha, c

def betapass(m1, m2, seq, c):
    T = len(seq)
    N = len(m1)

    beta = [[0]*N for x in range(0, T)]

    # Initialize
    for i in range(0, N):
        beta[T-1][i] = c[T-1]
    
    # Compute rest of beta
    for t in range(T-2, -1, -1):
        for i in range(0, N):
            beta[t][i] = 0
            for j in range(0, N):
                beta[t][i] += m1[i][j] * m2[j][seq[t+1]] * beta[t+1][j]
            beta[t][i] = c[t] * beta[t][i]

    return beta

def baumWelch(m1, m2, ispd, seq):
    maxIters = 150
    iters = 0
    oldLogProb = float("-inf")
    N = len(m1)
    T = len(seq)

    # Initialize gamma and diGamma matrices
    gamma = [[0] * N for x in range(T)]
    diGamma = [[[0] * N for x in range(N)] for t in range(T - 1)]

    while True:
        alpha, c = alphapass(m1, m2, ispd, seq)
        beta = betapass(m1, m2, seq, c)

        # Compute gamma and diGamma matrix
        for t in range(0, T - 1):
            for i in range(0, N):
                gamma[t][i] = 0
                for j in range(0, N):
                    diGamma[t][i][j] = (alpha[t][i] * m1[i][j] * m2[j][seq[t + 1]] * beta[t + 1][j])
                    gamma[t][i] += diGamma[t][i][j]

        for i in range(0, N):
            gamma[T-1][i] = alpha[T-1][i]

        # Re-estimate ispd
        for i in range(0, N):
            ispd[0][i] = gamma[0][i]

        # Re-estimate m1 
        for i in range(0, N):
            denom = 0.0000001
            for t in range(0, T - 1):
                denom += gamma[t][i]

            for j in range(0, N):
                numer = 0
                for t in range(0, T - 1):
                    numer += diGamma[t][i][j]

                m1[i][j] = numer / denom

        # Re-estimate m2 
        for i in range(0, N):
            denom = 0.0000001  
            for t in range(0, T):
                denom += gamma[t][i]

            for j in range(0, len(m2[0])):
                numer = 0
                for t in range(0, T):
                    if seq[t] == j:
                        numer += gamma[t][i]

                m2[i][j] = numer / denom

        # Calculate logProb
        logProb = 0
        for i in range(0, T):
            logProb += math.log(c[i])

        logProb = (-logProb)

        # Iterate until convergence or maximum iterations
        iters += 1
        if iters < maxIters and logProb > oldLogProb:
            oldLogProb = logProb
        else:
            return ispd, m1, m2


def main():
    m1, m2, ispd ,seq = readInp()
    newIspd, newM1, newM2 = baumWelch(m1, m2, ispd, seq)
    print(matrixToString(newM1))
    print(matrixToString(newM2))

if __name__ == "__main__":
    main()