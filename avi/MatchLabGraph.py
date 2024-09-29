import av
from math import sqrt
import numpy as np

container = av.open("resources/lr1_3.AVI")

frameList = []

for frame in container.decode(video=0):
    frameList.append(frame.to_rgb())

height = frameList[0].height
width = frameList[0].width
size = height * width


def mat(a):
    return np.sum(a) / size


def dispers(a):
    M = mat(a)
    summ = 0
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            summ += (a[i][j] - M) ** 2
    return summ / size


YComp = np.zeros((len(frameList), height, width))
for n in range(len(frameList)):
    tmp = frameList[n].to_ndarray()
    for i in range(height):
        for j in range(width):
            YComp[n][i][j] = 0.299 * tmp[i][j][0] + 0.587 * tmp[i][j][1] + 0.114 * tmp[i][j][2]

correlation = np.zeros((len(frameList), len(frameList)))
for m in range(len(frameList)):
    for n in range(len(frameList)):
        a = YComp[m]
        b = YComp[n]
        Ma = mat(a)
        Mb = mat(b)
        sigmaA = sqrt(dispers(a))
        sigmaB = sqrt(dispers(b))
        summary = 0
        for i in range(height):
            for j in range(width):
                summary += (a[i][j] - Ma) * (b[i][j] - Mb)
        correlation[m][n] = summary / (width * height * sigmaA * sigmaB)

np.savetxt('resources/co.txt', correlation)

container.close()


