import pyaudio
import wave
import os
import io
from pydub import AudioSegment
#set up the path for ffmpeg coverter
AudioSegment.converter = "./FFMPEG/bin/ffmpeg.exe"
#set up the path for google application credential(the json file) 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./GcloudAPIService/xxxxxxxxxx.json"

    

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000#44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
song = AudioSegment.from_wav(WAVE_OUTPUT_FILENAME)
song.export("test.flac",format = "flac")
os.remove(WAVE_OUTPUT_FILENAME)

def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,#44100,
        language_code='en-US')

    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print('Transcript: {}'.format(result.alternatives[0].transcript))
speech_file="test.flac"
transcribe_file(speech_file)
os.remove(speech_file)