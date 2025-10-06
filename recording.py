import pyaudio
import wave
import keyboard

def record_audio(filename="output.wav"):
    FRAMES_PER_BUFFER = 3200
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER
    )

    print("Recording... Press 'q' to stop.")
    frames = []

    try:
        while True:
            data = stream.read(FRAMES_PER_BUFFER)
            frames.append(data)
            if keyboard.is_pressed('q'):
                print("\n'q' pressed. Stopping recording.")
                break
    except KeyboardInterrupt:
        print("\nRecording stopped manually.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()

    print(f"Recording saved as {filename}")
