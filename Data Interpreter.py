import matplotlib.pyplot as Plot
from numpy import *


# r"E:\Uni\Project\1stDataSet\190129 Cu initial\190129 Cu AES initial 2000eV"

def load_directory(dirname, num_files):
    all_data = []
    all_times = []
    for idx in range(num_files):
        filepath = r"E:\Uni\Project\1stDataSet\190129 Cu initial\190129 Cu AES initial 2000eV 1.aes"
        # all_times.append(read_time(filepath))
        tmp = genfromtxt(filepath, skip_footer=1, skip_header=4)
        all_data.append(tmp)
    return all_data, all_times


def compoundLineGenerator(x1, x2, x3, y1, y2, y3):
    compoundLineY = []
    compoundLineX = []
    if (len(x1) < len(x2) and len(x1) < len(x3)):
        length = len(x1)
    elif (len(x2) < len(x1) and len(x2) < len(x3)):
        length = len(x2)
    else:
        length = len(x3)
    for i in range(length):
        # averages the three lines to form one line
        xCur = ((x1[i] + x2[i] + x3[i]) / 3)
        yCur = ((y1[i] + y2[i] + y3[i]) / 3)
        compoundLineX.append(xCur)
        compoundLineY.append(yCur)
    return compoundLineX, compoundLineY


def sorter(x, dirtyarrayy):
    newarray = []
    xnew = []
    k = dirtyarrayy[0]
    j = dirtyarrayy[1]
    i = 1
    length = len(dirtyarrayy)
    # Removes the initial charging effect
    while (j > k or k < 0) or x[i] < 200:
        k = j
        j = dirtyarrayy[i]
        i += 1
    for l in range(i - 1, length):
        newarray.append(dirtyarrayy[l])
        xnew.append(x[l])
    return (xnew, newarray)


def splitArr(data):
    length = len(data)
    x = []
    y = []
    for i in range(1, length):
        tmp = data[i]
        x.append(tmp[0])
        y.append(tmp[1])
    x, y = sorter(x, y)
    return (x, y)


def changeSearch(sample, count):
    for i in range(count):
        if not (sample[i] == sample[i + 1]):
            change = True
            peak = 0
        else:
            change = False
            peak = i
    return (change, peak)


def peakDetector(y):
    peakLocation = []
    correctedPeakY = []
    change = False
    pCount = 0
    i = 0
    zeroPoint = 0
    max = len(y)
    print(max)
    # cleans noise from the curve, highlighting the peaks
    while i != max-1:
        print(i)
        counter = 3
        if not y[i] == y[i + 1]:
            change = True
            while change:
                change, peak = changeSearch(y, counter)
                counter += 2
            if counter < 5:
                correctedPeakY.append(zeroPoint)
                i = i+counter
            else:
                for j in range (counter):
                    correctedPeakY.append(y[j])
                i = i+counter
            peakLocation.append(y[i + peak])
            #if y[i] != zeroPoint:
             #   i += 1
        else:
            zeroPoint = y[i]
            correctedPeakY.append(y[i])
            change = False
            i += 1
    correctedPeakY.append(zeroPoint)
    return (peakLocation, correctedPeakY)


data1 = genfromtxt(r"E:\Uni\Project\1stDataSet\190129 Cu initial\190129 Cu AES initial 2500eV 1.aes", skip_footer=1,
                   skip_header=4)
data2 = genfromtxt(r"E:\Uni\Project\1stDataSet\190129 Cu initial\190129 Cu AES initial 2500eV 2.aes", skip_footer=1,
                   skip_header=4)
data3 = genfromtxt(r"E:\Uni\Project\1stDataSet\190129 Cu initial\190129 Cu AES initial 2500eV 3.aes", skip_footer=1,
                   skip_header=4)
x1, y1 = splitArr(data1)
x2, y2 = splitArr(data2)
x3, y3 = splitArr(data3)
compoundX, compoundY = compoundLineGenerator(x1, x2, x3, y1, y2, y3)
correctedPeak, correctedPeakY = peakDetector(compoundY)
print(correctedPeakY)
print(len(compoundX),"; ",len(correctedPeakY))
Plot.figure(1)
Plot.plot(compoundX, compoundY, label="Compound Line")
Plot.plot(compoundX, correctedPeakY)
Plot.figure(2)
Plot.plot(x1, y1, alpha=0.5, label="Data Set 1")
Plot.plot(x2, y2, alpha=0.5, label="Data Set 2")
Plot.plot(x3, y3, alpha=0.5, label="Data Set 3")
Plot.legend()
Plot.show()
