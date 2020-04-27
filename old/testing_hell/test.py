import wave
from struct import pack, unpack
from math import sin, pi, sqrt
import os
import time
import pprint
import array
SHORT_MAX = 32767
GAIN = 2


def rms_wave(filepath):

    RATE= 44100
    chunk = 512


    f = wave.open(filepath,"rb")  
    print("\n  opening: "+filepath)
    print("  samplerate: "+str(f.getframerate()))
    print("  frames: "+str(f.getnframes()))
    print("  channels: "+str(f.getnchannels()))
    print("  sample width: "+str(f.getsampwidth()))

    ## GENERATE STEREO FILE ##
    wv = wave.open('temp.wav', 'w')
    wv.setparams((2, 2, RATE, 0, 'NONE', 'not compressed'))
    maxVol=2**14-1.0 #maximum amplitude
    wvData=""
    sourceData = [] # source wav
    ampData = []
    amp = 0
    i = 0
    t = 0

    for i in range(0, f.getnframes()):
        # populate sourceData with f sample data

        

        if (i%chunk == 0):
            # get amplitude data -----------
            # for every 512 samples of 
            startChunk = i
            endChunk = i+chunk
            for s in range(0,chunk):
                try:
                    frameSample = f.readframes(1)     
                    shortSample = unpack('h',frameSample)
                    sourceData.append(shortSample[0])
                except:
                    sourceData.append(0)

            try:
                subsamples = sourceData[startChunk:endChunk]
            except:
                # out of index range, so we are at the end
                subsamples = sourceData[startChunk:len(f.getnframes()-1)]

            amp = RMS(subsamples)
    
        ampData.append(amp)
    
    print("len of amp data: ",len(ampData),"len of source: ",len(sourceData))

    for k in    range(0,len(ampData)):
        
        sine = GAIN*ampData[k]*sin(t*2*pi*(140.0/RATE))
        if sine < 0:
            sine = max(sine,(SHORT_MAX-1)*-1)
        if sine > 0:
            sine = min(sine,(SHORT_MAX-1))
        # -- write source wav file in mono audio
        wvData += pack('h', sourceData[k])
        wvData += pack('h', sine)

        t += 1
   
    wv.writeframes(wvData)
    wv.close()





def RMS(dataArray):
    sum = 0
    for d in dataArray:
        sum += d**2
    mean = sum/float(len(dataArray))
    return sqrt(mean)

rms_wave("1_sack_vf_f.wav")