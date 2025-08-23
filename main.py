import wave


obj = wave.open("test.wav", "rb")

print("Number of Channels" , obj.getnchannels())
print("Sample Width" , obj.getsampwidth())
print("Number of frames" , obj.getnframes())
print("frame rate" , obj.getframerate())
print(obj.getparams())

print("time" , obj.getnframes() / obj.getframerate())

frames = obj.readframes(-1)
print(type(frames), type(frames[0]))
print(len(frames))

obj.close()

objWrite = wave.open("writeTest.wav", "wb")

objWrite.setnchannels(2)
objWrite.setsampwidth(2)
objWrite.setframerate(48000)

objWrite.writeframes(frames)

objWrite.close()


