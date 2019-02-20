import matplotlib.pyplot as Plot
from numpy import *


# r"D:\Callum Price\Documents\Comp Phys\Python\pycham\1stDataSet\190129 Cu initial"

def load_directory(dirname, num_files):
    all_data = []
    all_times = []
    for idx in range(num_files):
        filepath = r"D:\Callum Price\Documents\Comp Phys\Python\pycham\1stDataSet\Cu Data\Cu data-20190219T094147Z-001\Cu data\130219 AES\190129 Cu AES initial 2000eV 1.aes"
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
    while (j > k or k < 0) or x[i] < 50:
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
            #if y[i] != zeroPoint:
             #   i += 1
        else:
            zeroPoint = y[i]
            correctedPeakY.append(y[i])
            change = False
            i += 1
    correctedPeakY.append(zeroPoint)
    return (peakLocation, correctedPeakY)


data1 = genfromtxt(r"D:\Callum Price\Documents\Comp Phys\Python\pycham\1stDataSet\Cu Data\Cu data-20190219T094147Z-001\Cu data\130219 AES\130219 Cu001 2250eV 1.aes", skip_footer=1,
                   skip_header=4)
data2 = genfromtxt(r"D:\Callum Price\Documents\Comp Phys\Python\pycham\1stDataSet\Cu Data\Cu data-20190219T094147Z-001\Cu data\130219 AES\130219 Cu001 2250eV 2.aes", skip_footer=1,
                   skip_header=4)
data3 = genfromtxt(r"D:\Callum Price\Documents\Comp Phys\Python\pycham\1stDataSet\Cu Data\Cu data-20190219T094147Z-001\Cu data\130219 AES\130219 Cu001 2250eV 3.aes", skip_footer=1,
                   skip_header=4)
data4 = genfromtxt(r"D:\Callum Price\Documents\Comp Phys\Python\pycham\1stDataSet\Cu Data\Cu data-20190219T094147Z-001\Cu data\140219 AES\140219 Cu001 AES 2250ev 1.aes", skip_footer=1,
                   skip_header=4)
data5 = genfromtxt(r"D:\Callum Price\Documents\Comp Phys\Python\pycham\1stDataSet\Cu Data\Cu data-20190219T094147Z-001\Cu data\140219 AES\140219 Cu001 AES 2250ev 2.aes", skip_footer=1,
                   skip_header=4)
data6 = genfromtxt(r"D:\Callum Price\Documents\Comp Phys\Python\pycham\1stDataSet\Cu Data\Cu data-20190219T094147Z-001\Cu data\140219 AES\140219 Cu001 AES 2250ev 3.aes", skip_footer=1,
                   skip_header=4)
data7 = genfromtxt(r"D:\Callum Price\Documents\Comp Phys\Python\pycham\1stDataSet\Cu Data\Cu data-20190219T094147Z-001\Cu data\190219 AES\190219 Cu001 AES 2250ev 1.aes", skip_footer=1,
                   skip_header=4)
data8 = genfromtxt(r"D:\Callum Price\Documents\Comp Phys\Python\pycham\1stDataSet\Cu Data\Cu data-20190219T094147Z-001\Cu data\190219 AES\190219 Cu001 AES 2250ev 2.aes", skip_footer=1,
                   skip_header=4)
data9 = genfromtxt(r"D:\Callum Price\Documents\Comp Phys\Python\pycham\1stDataSet\Cu Data\Cu data-20190219T094147Z-001\Cu data\190219 AES\190219 Cu001 AES 2250ev 3.aes", skip_footer=1,
                   skip_header=4)
x1, y1 = splitArr(data1)
x2, y2 = splitArr(data2)
x3, y3 = splitArr(data3)
compoundXA, compoundYA = compoundLineGenerator(x1, x2, x3, y1, y2, y3)
x4, y4 = splitArr(data4)
x5, y5 = splitArr(data5)
x6, y6 = splitArr(data6)
compoundXB, compoundYB = compoundLineGenerator(x4, x5, x6, y4, y5, y6)
x7, y7 = splitArr(data4)
x8, y8 = splitArr(data5)
x9, y9 = splitArr(data6)
compoundXC, compoundYC = compoundLineGenerator(x7, x8, x9, y7, y8, y9)
#correctedPeak, correctedPeakY = peakDetector(compoundYA)
#print(correctedPeakY)
#print(len(compoundXA),"; ",len(correctedPeakY))
Plot.figure(1)
Plot.plot(compoundXA, compoundYA, label="Compound Line Before Cleaning")
Plot.plot(compoundXB, compoundYB, label="Compound Line After Cleaning")
Plot.plot(compoundXC, compoundYC, label="Compound Line After Cleaning Second TIme")
#Plot.plot(compoundXA, correctedPeakY, label="Corrected Line")
Plot.legend()
Plot.figure(2)
Plot.plot(x1, y1, alpha=0.5, label="Data Set 1 Before")
Plot.plot(x2, y2, alpha=0.5, label="Data Set 2 Before")
Plot.plot(x3, y3, alpha=0.5, label="Data Set 3 Before")
Plot.plot(x4, y4, alpha=0.5, label="Data Set 1 After 1")
Plot.plot(x5, y5, alpha=0.5, label="Data Set 2 After 1")
Plot.plot(x6, y6, alpha=0.5, label="Data Set 3 After 1")
Plot.plot(x7, y7, alpha=0.5, label="Data Set 1 After 2")
Plot.plot(x8, y8, alpha=0.5, label="Data Set 2 After 2")
Plot.plot(x9, y9, alpha=0.5, label="Data Set 3 After 2")
Plot.legend()
Plot.show()
