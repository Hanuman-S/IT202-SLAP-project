import wave
import matplotlib.pyplot as plt
import numpy as np

obj = wave.open("test.wav", "rb")

print("time" , obj.getnframes() / obj.getframerate())

sampleFreq = obj.getframerate()
nSamples = obj.getnframes()

signalWave = obj.readframes(-1)
nChannels = obj.getnchannels()

signalArr = np.frombuffer(signalWave, dtype=np.int16)

if nChannels == 2:
    signalArr = signalArr.reshape(-1, 2)
    signalArr = signalArr[:,0]
    
times = np.linspace(0, nSamples/ sampleFreq, num = len(signalArr))

plt.figure(figsize=(15,3.755))
plt.plot(times, signalArr)
plt.title("Audio Signal")
plt.ylabel("Signal Wave")
plt.xlabel("Times (s)")
plt.xlim(0, nSamples/sampleFreq)

plt.show()