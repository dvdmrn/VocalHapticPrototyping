import GenerateSine
import ProcessSpeech
import os
import sys

FILEPATH = "sounds/rec.wav"

def main():
	global FILEPATH
	
	if len(sys.argv) > 1:
		FILEPATH = sys.argv[1]
	fileInfo = ProcessSpeech.soundInfo(FILEPATH)
	speech = ProcessSpeech.getData(FILEPATH)
	GenerateSine.makeSine(speech,fileInfo)
	os.system("aplay temp.wav")

main()