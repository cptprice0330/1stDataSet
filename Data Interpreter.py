from matplotlib.pyplot import plot, legend, axis, xlabel, ylabel, savefig, clf, title, grid, minorticks_on, scatter, subplots
from numpy import genfromtxt
from scipy.signal import find_peaks
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset



# r"D:\Callum Price\Documents\Comp Phys\Python\pycham\1stDataSet\190129 Cu initial"

def load_directory(dirname, num_files, energy):
    data = []
    for idx in range(num_files):
        fileidx = energy + " " + str(idx+1)+".aes"
        filepath = r"E:\Uni\Project\DATA\%s\%s" % (dirname, fileidx)
        tmp = genfromtxt(filepath, skip_footer=1, skip_header=4)
        data.append(tmp)
    return data


def compoundLineGenerator(data):
    x1, y1 = splitArr(data[0], True)
    x2, y2 = splitArr(data[1], True)
    x3, y3 = splitArr(data[2], True)
    compoundLine = []
    if (len(x1) <= len(x2) and len(x1) <= len(x3)):
        length = len(x1)
    elif (len(x2) <= len(x1) and len(x2) <= len(x3)):
        length = len(x2)
    elif (len(x3) <= len(x2) and len(x3) <= len(x1)):
        length = len(x3)
    #Debug code
    #print(len(x1))
    #print(len(x2))
    #print(len(x3))
    #print("Len: ", length)
    #print(x1[length-1])
    #print(x2[length-1])
    #print(x3[length-1])
    for i in range(length-1):
        # averages the three lines to form one line
        tmp = []
        xCur = ((x1[i] + x2[i] + x3[i]) / 3)
        yCur = ((y1[i] + y2[i] + y3[i]) / 3)
        tmp.append(xCur)
        tmp.append(yCur)
        compoundLine.append(tmp)
    return compoundLine





def sorter(x, dirtyarray):
    newarray = []
    xnew = []
    k = dirtyarray[0]
    j = dirtyarray[1]
    i = 1
    length = len(dirtyarray)
    # Removes the initial charging effect
    while (j > k or k < 0) or dirtyarray[i] >= 0.03:
        k = j
        j = dirtyarray[i]
        i += 1
    for l in range(i - 1, length):
        newarray.append(dirtyarray[l])
        xnew.append(x[l])
    return xnew, newarray


def splitArr(data, sort):
    length = len(data)
    x = []
    y = []
    for i in range(1, length):
        tmp = data[i]
        x.append(tmp[0])
        y.append(tmp[1])
    if sort:
        x, y = sorter(x, y)
    return x, y


def changeSearch(sample, count):
    for i in range(count):
        if not (sample[i] == sample[i + 1]):
            change = True
            peak = 0
        else:
            change = False
            peak = i
    return change, peak


def peakDetector(data,sort):
    peakX = []
    peakY = []
    Y = []
    x,y = splitArr(data,sort)
    #print(x,y)
    for i in range (len(y)):
        Y.append(abs(y[i]))
    peaks = find_peaks(Y, plateau_size=[None, 5],height= [0.00125,None], distance= 5)
    #print(peaks)
    peakLocal = peaks[0]
    for i in range (len(peakLocal)):
        peakX.append(x[peakLocal[i]])
        peakY.append(y[peakLocal[i]])
    peaks = find_peaks(y,plateau_size=[1, 5],height= [-0.0009], distance= 5)
    peakLocal = peaks[0]
    #print(peaks)
    for i in range (len(peakLocal)):
        peakX.append(x[peakLocal[i]])
        peakY.append(y[peakLocal[i]])
    #print(peakX)
    #print(peakY)
    return peakX, peakY

for k in range (0,4):
    compData = []
    if k == 0 :
        eng = "2000"
    if k == 1:
        eng = "2250"
    if k ==2:
        eng = "2500"
    if k ==3:
        eng = "2750"
    for j in range (0,6):
        data = load_directory(j + 1, 3, eng)
        for i in range (0,3):
            clf()
            #print(data[i])
            x,y = splitArr(data[i], True)
            px,py = peakDetector(data[i],True)
            ext = eng+"eV Graph " + str(i+1)
            savepath = r"E:\Uni\Project\Graphs\%s\%s.png" % (str(j+1), ext)
            axis(xmin = 0, xmax= 1100)
            grid(axis = "both", which = "both")
            plot(x,y, linewidth = 0.5,alpha = 1)#,  marker = 'o', markersize = 0.1)
            #z = []
            #for i in range (len(y)):
            #    z.append(abs(y[i]))
            #plot(x,z, linewidth = 0.5, alpha = 1)
            minorticks_on()
            scatter(px,py, alpha= 0.4, c = "red", marker= 'x')
            title(ext)
            xlabel("Auger Energy/eV")
            ylabel("Auger Signal/V")
            savefig(savepath, dpi = 900, bbox_inches = "tight")


        for i in range (0,3):
            clf()
            x,y = splitArr(data[i], False)
            ext = eng+"eV non-sorted Graph " + str(i+1)
            savepath = r"E:\Uni\Project\Graphs\%s\%s.png" % (str(j+1), ext)
            axis(xmin = 0, xmax= 1100)
            grid(axis = "both", which = "both")
            plot(x,y, linewidth = 0.5)
            minorticks_on()
            title(ext)
            xlabel("Auger Energy/eV")
            ylabel("Auger Signal/V")
            savefig(savepath, dpi = 900, bbox_inches = "tight")
        clf()
        ext = eng+"eV Average Graph"
        savepath = r"E:\Uni\Project\Graphs\%s\%s.png" % (str(j+1), ext)
        compline = compoundLineGenerator(data)
        x,y = splitArr(compline, False)
        px,py = peakDetector(compline,False)
        axis(xmin=0, xmax=1100)
        grid(axis="both", which="both", linewidth = 0.3)
        plot(x,y, linewidth = 0.5)
        scatter(px, py, alpha=0.4, c="red", marker='x')
        minorticks_on()
        xlabel("Auger Energy/eV")
        ylabel("Auger Signal/V")
        title(ext)
        savefig(savepath, dpi = 900, bbox_inches = "tight")
        compData.append(data)
    clf()
    ext = eng+"eV Comparison Graph"
    fig,ax = subplots(figsize = [5,4])
    x1, y1 = splitArr(compoundLineGenerator(compData[0]),False)
    #px1, py1 = peakDetector(compoundLineGenerator(compData[0]),False)
    x2, y2 = splitArr(compoundLineGenerator(compData[1]),False)
    #px2, py2 = peakDetector(compoundLineGenerator(compData[1]),False)
    x3, y3 = splitArr(compoundLineGenerator(compData[2]),False)
    #px3, py3 = peakDetector(compoundLineGenerator(compData[2]),False)
    x4, y4 = splitArr(compoundLineGenerator(compData[3]),False)
    #px4, py4 = peakDetector(compoundLineGenerator(compData[3]),False)
    x5, y5 = splitArr(compoundLineGenerator(compData[4]),False)
    #px5, py5 = peakDetector(compoundLineGenerator(compData[4]),False)
    x6, y6 = splitArr(compoundLineGenerator(compData[5]),False)
    #px6, py6 = peakDetector(compoundLineGenerator(compData[5]),False)
    axis(xmin=0, xmax=1100)
    grid(axis="both", which="both", linewidth = 0.3)
    minorticks_on()
    ax.plot(x1, y1, linewidth=0.7, alpha = 0.5, label = "Inital")
   #scatter(px1,py1, alpha=0.4, c="red", marker='x', label = "Peaks")
    ax.plot(x2, y2, linewidth=0.5, alpha = 0.5, label = "First Sputtering")
    #scatter(px2, py2, alpha=0.4, c="red", marker='x')
    ax.plot(x3, y3, linewidth=0.5, alpha = 0.5, label = "Second Sputtering")
    #scatter(px3, py3, alpha=0.4, c="red", marker='x')
    ax.plot(x4, y4, linewidth=0.5, alpha = 0.5, label = "Third Sputtering")
    #scatter(px4, py4, alpha=0.4, c="red", marker='x')
    ax.plot(x5, y5, linewidth=0.5, alpha = 0.5, label = "First Annealing")
    #scatter(px5, py5, alpha=0.4, c="red", marker='x')
    ax.plot(x6, y6, linewidth=0.5, alpha = 0.5, label = "Fourth Sputtering and Second Annealing")
    #scatter(px6, py6, alpha=0.4, c="red", marker='x')
    ax.legend(loc = 0, fontsize = 4)
    ax.set_title(ext)
    ax.set_ylabel("Auger Signal/V")
    ax.set_xlabel("Auger Energy/eV")
    axins = zoomed_inset_axes(ax, 2.5, loc= "center right")
    axins.plot(x1, y1, linewidth=0.7, alpha = 0.5)
    axins.plot(x2, y2, linewidth=0.5, alpha = 0.5)
    axins.plot(x3, y3, linewidth=0.5, alpha = 0.5)
    axins.plot(x4, y4, linewidth=0.5, alpha = 0.5)
    axins.plot(x5, y5, linewidth=0.5, alpha = 0.5)
    axins.plot(x6, y6, linewidth=0.5, alpha = 0.5)
    if eng == "2000" :
        xLim1,xLim2,yLim1,yLim2 = 350, 550, -0.00375, 0.00125
    if eng == "2250" :
        xLim1,xLim2,yLim1,yLim2 = 200, 350, -0.04, 0.01
    if eng == "2500" :
        xLim1,xLim2,yLim1,yLim2 = 250, 400, -0.05, 0.05
    if eng == "2750" :
        xLim1,xLim2,yLim1,yLim2 = 350, 500, -0.05, 0.05
    axins.set_xlim(xLim1,xLim2)
    axins.set_ylim(yLim1,yLim2)
    mark_inset(ax, axins, loc1=2, loc2=1, fc="None", ec = "0.5")
    axins.xaxis.set_visible(False)
    axins.yaxis.set_visible(False)
    savepath = r"E:\Uni\Project\Graphs\Comp\%s.png" % (ext)
    savefig(savepath, dpi=4000, bbox_inches="tight")

    clf()
    ext = eng+"eV Reduced Set Graph"
    axis(xmin=0, xmax=1100)
    grid(axis="both", which="both", linewidth = 0.3)
    minorticks_on()
    plot(x1, y1, linewidth=0.5, alpha=0.5, label="Inital")
    plot(x3, y3, linewidth=0.5, alpha=0.5, label="Second Sputtering")
    plot(x6, y6, linewidth=0.5, alpha=0.5, label="Fourth Sputtering and Second Annealing")
    legend()
    title(ext)
    ylabel("Auger Signal/V")
    xlabel("Auger Energy/eV")
    savepath = r"E:\Uni\Project\Graphs\Ssam\%s.png" % (ext)
    savefig(savepath, dpi=4000, bbox_inches="tight")

# data1 = genfromtxt(r"E:\Uni\Project\1stDataSet\190129 Cu initial\190129 Cu AES initial 2500eV 1.aes", skip_footer=1,
#                    skip_header=4)
# data2 = genfromtxt(r"E:\Uni\Project\1stDataSet\190129 Cu initial\190129 Cu AES initial 2500eV 2.aes", skip_footer=1,
#                    skip_header=4)
# data3 = genfromtxt(r"E:\Uni\Project\1stDataSet\190129 Cu initial\190129 Cu AES initial 2500eV 3.aes", skip_footer=1,
#                    skip_header=4)
# data4 = genfromtxt(r"E:\Uni\Project\1stDataSet\190129 Cu initial\190130 Cu AES After First Clean 2500eV 1.aes", skip_footer=1,
#                    skip_header=4)
# data5 = genfromtxt(r"E:\Uni\Project\1stDataSet\190129 Cu initial\190130 Cu AES After First Clean 2500eV 2.aes", skip_footer=1,
#                    skip_header=4)
# data6 = genfromtxt(r"E:\Uni\Project\1stDataSet\190129 Cu initial\190130 Cu AES After First Clean 2500eV 3.aes", skip_footer=1,
#                    skip_header=4)
# data7 = genfromtxt(r"E:\Uni\Project\1stDataSet\190219 AES\190219 Cu001 AES 2500ev 1 3rd irrad.aes", skip_footer=1,
#                    skip_header=4)
# data8 = genfromtxt(r"E:\Uni\Project\1stDataSet\190219 AES\190219 Cu001 AES 2500ev 2 3rd irrad.aes", skip_footer=1,
#                    skip_header=4)
# data9 = genfromtxt(r"E:\Uni\Project\1stDataSet\190219 AES\190219 Cu001 AES 2500ev 3 3rd irrad.aes", skip_footer=1,
#                    skip_header=4)
# data10 = genfromtxt(r"E:\Uni\Project\1stDataSet\230319 AES\2330319 Cu001 2500ev 1.aes", skip_footer=1, skip_header=4)
# data11 = genfromtxt(r"E:\Uni\Project\1stDataSet\230319 AES\2330319 Cu001 2500ev 2.aes", skip_footer=1, skip_header=4)
# data12 = genfromtxt(r"E:\Uni\Project\1stDataSet\230319 AES\2330319 Cu001 2500ev 3.aes", skip_footer=1, skip_header=4)
# x1, y1 = splitArr(data1)
# x2, y2 = splitArr(data2)
# x3, y3 = splitArr(data3)
# compoundXA, compoundYA = compoundLineGenerator(x1, x2, x3, y1, y2, y3)
# x4, y4 = splitArr(data4)
# x5, y5 = splitArr(data5)
# x6, y6 = splitArr(data6)
# compoundXB, compoundYB = compoundLineGenerator(x4, x5, x6, y4, y5, y6)
# x7, y7 = splitArr(data7)
# x8, y8 = splitArr(data8)
# x9, y9 = splitArr(data9)
# compoundXC, compoundYC = compoundLineGenerator(x7, x8, x9, y7, y8, y9)
# x10, y10 =splitArr(data10)
# x11, y11 =splitArr(data11)
# x12, y12 =splitArr(data12)
# compoundXD, compoundYD = compoundLineGenerator(x10, x11, x12, y10, y11, y12)
# #correctedPeak, correctedPeakY = peakDetector(compoundYA)
# #print(correctedPeakY)
# #print(len(compoundXA),"; ",len(correctedPeakY))
# figure(1)
# xlabel( "Auger Energy eV")
# ylabel("Auger Signal V")
# plot(compoundXA, compoundYA, label="Compound Line Before Cleaning", alpha = 0.6)
# plot(compoundXB, compoundYB, label="Compound Line After Cleaning", alpha = 0.7)
# plot(compoundXC, compoundYC, label="Compound Line After Cleaning Second Time", alpha = 0.8)
# plot(compoundXD, compoundYD, label = "Compound line after annealing", alpha = 0.8)
# #plot(compoundXA, correctedPeakY, label="Corrected Line")
# legend()
# figure(2)
# xlabel( "Auger Energy eV")
# ylabel("Auger Signal V")
# plot(x1, y1, alpha=0.5, label="Data Set 1 Before", linewidth = 0.5)
# plot(x2, y2, alpha=0.5, label="Data Set 2 Before", linewidth = 0.5)
# plot(x3, y3, alpha=0.5, label="Data Set 3 Before", linewidth = 0.5)
# plot(x4, y4, alpha=0.5, label="Data Set 1 After 1", linewidth = 0.5)
# plot(x5, y5, alpha=0.5, label="Data Set 2 After 1", linewidth = 0.5)
# plot(x6, y6, alpha=0.5, label="Data Set 3 After 1", linewidth = 0.5)
# plot(x7, y7, alpha=0.5, label="Data Set 1 After 2", linewidth = 0.5)
# plot(x8, y8, alpha=0.5, label="Data Set 2 After 2", linewidth = 0.5)
# plot(x9, y9, alpha=0.5, label="Data Set 3 After 2", linewidth = 0.5)
# savefig(r"E:\Uni\Project\1stDataSetGraph_1.png", dpi = 4000)
# legend()
# show()


