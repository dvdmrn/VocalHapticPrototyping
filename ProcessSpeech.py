import parselmouth
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import math
import tqdm
import sys
from scipy.interpolate import interp1d

sns.set() # Use seaborn's default style to make attractive graphs
np.set_printoptions(threshold=sys.maxsize)
# Plot nice figures using Python's "standard" matplotlib library

def draw_spectrogram(spectrogram, dynamic_range=70):
    X, Y = spectrogram.x_grid(), spectrogram.y_grid()
    sg_db = 10 * np.log10(spectrogram.values)
    plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap='plasma')
    plt.ylim([spectrogram.ymin, spectrogram.ymax])
    plt.xlabel("time [s]")
    plt.ylabel("frequency [Hz]")

def draw_intensity(intensity):
    plt.plot(intensity.xs(), intensity.values.T, linewidth=3, color='w')
    plt.plot(intensity.xs(), intensity.values.T, linewidth=1)
    plt.grid(False)
    plt.ylim(0)
    plt.ylabel("intensity [dB]")

def draw_pitch(pitch, interpolated=False):
    # Extract selected pitch contour, and
    # replace unvoiced samples by NaN to not plot
    if(interpolated):
        pitch_values = pitch
    else:
        pitch_values = pitch.selected_array['frequency']
        pitch_values[pitch_values==0] = np.nan
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=5, color='w')
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=2)
    plt.grid(False)
    plt.ylim(0, pitch.ceiling)
    plt.ylabel("fundamental frequency [Hz]")

def draw_pitch_linear_interp(snd,pitch_interp, pitch):
    # Extract selected pitch contour, and
    # replace unvoiced samples by NaN to not plot
    pitch_values = pitch_interp
    # else:
    #     pitch_values = pitch.selected_array['frequency']
    #     pitch_values[pitch_values==0] = np.nan
    # plt.plot(snd.xs(), pitch_values, 'o', markersize=5, color='w')
    
    plt.plot(snd.xs(), pitch_values, '-', markersize=4,color='w')
    plt.grid(False)
    plt.ylim(0, pitch.ceiling)
    plt.ylabel("fundamental frequency [Hz]")

# def draw_pitch_cubic(pitch,pitch_interp,snd):
#     x = np.linspace(0,snd.xs()[len(snd.xs())-1])
#     # print(x)
#     plt.plot(x,pitch_interp(snd.xs()), "--")
#     plt.ylim(0, pitch.ceiling)
#     plt.ylabel("fundamental frequency [Hz]")


# If desired, pre-emphasize the sound fragment before calculating the spectrogram
def showGraph(snd,pitch):
    pre_emphasized_snd = snd.copy()
    pre_emphasized_snd.pre_emphasize()
    spectrogram = pre_emphasized_snd.to_spectrogram(window_length=0.03, maximum_frequency=8000)
    print("speclen",len(spectrogram.xs()))
    plt.figure()
    draw_spectrogram(spectrogram)
    plt.twinx()
    draw_pitch(pitch)
    plt.xlim([snd.xmin, snd.xmax])
    plt.show() # or plt.savefig("spectrogram_0.03.pdf")


def showGraphInterp(snd,pitch_interp,pitch):
    pre_emphasized_snd = snd.copy()
    pre_emphasized_snd.pre_emphasize()
    spectrogram = pre_emphasized_snd.to_spectrogram(window_length=0.03, maximum_frequency=8000)
    print("speclen",len(spectrogram.xs()))
    plt.figure()
    draw_spectrogram(spectrogram)
    plt.twinx()
    draw_pitch_linear_interp(snd,pitch_interp,pitch)
    plt.xlim([snd.xmin, snd.xmax])
    plt.show() # or plt.savefig("spectrogram_0.03.pdf")


def soundInfo(path):
    snd = parselmouth.Sound(path)
    sound = {"length":snd.duration,
             "sampleRate":snd.sampling_frequency,
             "n_frames":snd.n_frames
    }
    return sound


def getData(path):

    print("reading file")
    snd = parselmouth.Sound(path)
    rms = [math.sqrt(x**2) for x in snd.values.T]

    print("len rms: ",len(rms))
    print(snd.duration)

    # init structured array ------------
    keys = dtype=[('time', 'f4'),('f0_Hz', 'f4'), ('frame', 'u4'), ('rms', 'f4')]
    analysis = np.zeros(snd.n_frames, keys)
    # ----------------------------------
    print("sample rate:", snd.sampling_frequency)


    # now we add PITCH analysis
    # in consants it is sometimes hard to discern pitch, so we do not have pitch values
    # for those phonemes.
    print("analyzing pitch...")
    pitch = snd.to_pitch()

    pitch_values = pitch.selected_array['frequency']

    freqX = np.core.records.fromarrays([pitch.xs(),pitch_values],names="x,Hz")
    pruned_arr = freqX[freqX["Hz"]!=0]
    interpolated_pitch = np.interp(snd.xs(),pruned_arr["x"],pruned_arr["Hz"])

    showGraphInterp(snd,interpolated_pitch,pitch)
    # draw_pitch_linear_interp(pitch, interpolated_pitch, snd)

    # cubic bois (doesn't work yet) ---------------------------------------------------\\
    # interpolated_pitch = interp1d(pruned_arr["x"],pruned_arr["Hz"], kind="cubic")
    # draw_pitch_cubic(pitch, interpolated_pitch, snd)
    # ---------------------------------------------------------------------------------\\
    

    # showGraph(snd,pitch)

    # fill array with sound data --------------------------------------------------------
    print("creating sound object")
    for i in tqdm.tqdm(range(0,snd.n_frames)):
        analysis[i]["frame"] = i
        analysis[i]["time"] = i/snd.sampling_frequency
        analysis[i]["f0_Hz"] = interpolated_pitch[i]
        analysis[i]["rms"] = rms[i]

    np.savetxt("output.csv",analysis,delimiter=",",header="time,f0,frame,rms",comments="")
    return(analysis)

# getData()