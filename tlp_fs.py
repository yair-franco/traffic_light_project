import numpy as np
import matplotlib.pyplot as plt

def calc_Mc_b(mag,plot=0):
    nNumberMagnitude=np.floor(mag.max()*10)+1
    xx=np.linspace(np.floor(mag.min()*10)/10,mag.max(),int((np.floor(mag.max()*10)/10-
                                                            np.floor(mag.min()*10)/10)*10)+1)
    vhist,vMagBins=np.histogram(mag,bins=xx)
    iMc = np.where(vhist==vhist.max())[0][-1]
    fMc=vMagBins[iMc]
    hist = vhist[iMc:][::-1]
    bins = vMagBins[iMc:][::-1]
    cum_hist = hist.cumsum()
    log_cum_sum = np.log10(cum_hist)
    bins = bins[1:]
    b,a = np.polyfit(bins, log_cum_sum, 1)
    if plot==1:
        plt.figure()
        plt.subplot(211)
        plt.bar(vMagBins[:-1]+0.05,vhist,0.1)
        plt.axvline(x=fMc,c='r',lw=2)
        plt.title('Mc:'+ "{:.2f}".format(fMc)+'  '+'b value:'+  "{:.2f}".format(-b))
        plt.xlim(-1,8)
        plt.ylabel('Event number')
        plt.subplot(212)
        plt.plot(bins,np.log10(cum_hist))
        plt.plot(bins,a + b*bins)
        plt.xlim(-1,8)
        plt.xlabel('Magnitude')
        plt.ylabel('log10(CDF)')
        plt.show()
        
    return fMc, a, -b

def appendB(arrayName,bval,dates,firstEQ=0,lastEQ=1,plot=0): #adds b values to given array and can also plot
    if plot==0:
        arrayName.append(bval)
    
    elif plot==1:
        xrange = len(arrayName)
        x = dates
        
        print(len(x),len(arrayName))
        
        #a,b = np.polyfit(x,arrayName,1)
        
        bMed = np.median(arrayName)
        YLBuffer = 0.1 * bMed
            
        plt.axhspan(0,bMed-YLBuffer,0,xrange,color="red",alpha=0.5)
        plt.axhspan(bMed-YLBuffer,bMed+YLBuffer,0,xrange,color="yellow",alpha=0.5)
        plt.axhspan(bMed+YLBuffer,np.max(arrayName)+0.5,0,xrange,color="green",alpha=0.5)
        #arbitrary range for colors for now, need to read up more on how to choose these.
        
        plt.axhline(y = bMed, color = 'black', linestyle = '--',label=f"Median ({np.around(bMed,3)})")
        #plt.plot(x,arrayName,'b-',label="b-value")
        plt.plot(x,arrayName,'b.-',label="b-value",markersize=3,linewidth=0.25)

        #plt.plot(x,a*x+b,'r',label=f"Best fit line")
        
        plt.xlabel(f"Year")
        plt.ylabel('')
        plt.legend()
        plt.ylim(0,np.max(arrayName)+0.5)
        plt.xticks(np.arange(np.around(firstEQ), np.around(lastEQ), step=3))  # Set label locations.
        #plt.xticks([0,1,2],[firstEQ,"middle",lastEQ])
        #plt.rc('xtick', labelsize=3)


def read_catalog(filename): #takes data from Italian catalog and parses into a dataframe
    with open(filename, 'r') as f:
        # read header
        header = f.readline().strip().split()
        # read data
        data = []
        for line in f:
            fields = line.strip().split('|')
            fields[1] = pd.to_datetime(fields[1])
            data.append(fields)
    # create pandas dataframe
    df = pd.DataFrame(data, columns=['EventID', 'Time', 'Latitude', 'Longitude', 'Depth/Km', 'Author', 'Catalog', 'Contributor', 'ContributorID', 'MagType', 'Magnitude', 'MagAuthor', 'EventLocationName', 'EventType'])
    # convert latitude, longitude, depth, and magnitude columns to numeric format
    df[['Latitude', 'Longitude', 'Depth/Km', 'Magnitude']] = df[['Latitude', 'Longitude', 'Depth/Km', 'Magnitude']].apply(pd.to_numeric)
    df = df.rename(columns={'EventID': 'ID'})
    df = df.rename(columns={'Latitude': 'Lat'})
    df = df.rename(columns={'Longitude': 'Long'})
    df = df.rename(columns={'Depth/Km': 'Depth'})
    df = df.rename(columns={'Magnitude': 'Mag'})
    return df