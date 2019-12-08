import wave
from struct import pack, unpack
from math import sin, pi, sqrt, ceil
import os
import time
import pprint
import array
import numpy as np
import tqdm

SHORT_MAX = 32767
GAIN = 100000


def makeSine(speech,soundInfo):

    RATE= int(soundInfo["sampleRate"])

    ## GENERATE STEREO FILE ##
    wv = wave.open('temp.wav', 'w')
    wv.setparams((2, 2, RATE, 0, 'NONE', 'not compressed'))
    maxVol=2**14-1.0 #maximum amplitude
    wvData= b""
    t = 0
    
    # relative freq. scaling
    # scaledFreq = 200*(speech["f0_Hz"] - np.min(speech["f0_Hz"]))/np.ptp(speech["f0_Hz"]) 
    
    # absolute freq scaling, 600Hz max f0
    scaledFreq = ((speech["f0_Hz"] - np.min(speech["f0_Hz"]))/500)

    print("writing haptic wav")
    for i in tqdm.tqdm(range(0,len(speech))):
        
        # sine = GAIN*speech[i]["rms"]*sin(t*2*pi*speech[i]["f0_Hz"]*(80.0/RATE))
        
        # scaling freq --------------------------
        # assume f0 goes up to 600Hz
        # but don't want more than 200Hz

        sine = GAIN*speech[i]["rms"]*sin(2*pi*t*(scaledFreq[i]/RATE))

        # print(sine)
        sine = ceil(sine)
        # time.sleep(0.5)

        if sine < 0:
            sine = max(sine,(SHORT_MAX-1)*-1)
        if sine > 0:
            sine = min(sine,(SHORT_MAX-1))
        # -- write source wav file in mono audio
        wvData += pack('h', sine)
        wvData += pack('h', sine)

        t += 1
   
    wv.writeframes(wvData)
    wv.close()



