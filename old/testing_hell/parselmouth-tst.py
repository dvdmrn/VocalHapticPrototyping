import parselmouth

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time



sns.set() # Use seaborn's default style to make attractive graphs

# Plot nice figures using Python's "standard" matplotlib library
snd = parselmouth.Sound("sounds/144[kb]i_need_a_dj.mp3")

print(snd)
print("rms: ",snd.get_rms())


# for v in snd.values.T:
#     print("snd vals: ",v)
# plt.figure()
# plt.plot(snd.xs(), snd.values.T)
# plt.xlim([snd.xmin, snd.xmax])
# plt.xlabel("time [s]")
# plt.ylabel("amplitude")
# plt.show() # or plt.savefig("sound.png"), or plt.savefig("sound.pdf")

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

# intensity = snd.to_intensity()
# spectrogram = snd.to_spectrogram()
# plt.figure()
# draw_spectrogram(spectrogram)
# plt.twinx()
# draw_intensity(intensity)
# plt.xlim([snd.xmin, snd.xmax])
# plt.show() # or plt.savefig("spectrogram.pdf")


def draw_pitch(pitch):
    # Extract selected pitch contour, and
    # replace unvoiced samples by NaN to not plot
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values==0] = np.nan
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=5, color='w')
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=2)
    plt.grid(False)
    plt.ylim(0, pitch.ceiling)
    plt.ylabel("fundamental frequency [Hz]")

pitch = snd.to_pitch()


# !!! gets frequency below
# for p in pitch.selected_array['frequency']:
#     print("pitch info: ", p)
# 169 frames
# duration: 1.72185 (prob seconds)

# If desired, pre-emphasize the sound fragment before calculating the spectrogram
pre_emphasized_snd = snd.copy()
pre_emphasized_snd.pre_emphasize()
spectrogram = pre_emphasized_snd.to_spectrogram(window_length=0.03, maximum_frequency=8000)
plt.figure()
draw_spectrogram(spectrogram)
plt.twinx()
draw_pitch(pitch)
plt.xlim([snd.xmin, snd.xmax])
plt.show() # or plt.savefig("spectrogram_0.03.pdf")