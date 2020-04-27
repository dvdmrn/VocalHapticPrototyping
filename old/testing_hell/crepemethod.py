import crepe
from scipy.io import wavfile

sr, audio = wavfile.read("1_sack_vf_f.wav")
time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True)

for i in range(0,len(time)):
	print("t: ",time[i], "Hz: ",frequency[i], "conf: ", confidence[i])