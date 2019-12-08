import GenerateSine
import ProcessSpeech

FILEPATH = "sounds/vst.wav"

def main():
	fileInfo = ProcessSpeech.soundInfo(FILEPATH)
	speech = ProcessSpeech.getData(FILEPATH)
	GenerateSine.makeSine(speech,fileInfo)

main()