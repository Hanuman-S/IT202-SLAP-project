import pyaudio
import wave
import keyboard

def loop_play(file):
    wf = wave.open(file, 'rb')
    
    p = pyaudio.PyAudio()
    
    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True
    )
    
    print("Playing in loop... Press 'q' to stop.")
    
    try:
        while True:
            wf.rewind()
            data = wf.readframes(1024)
            
            while data:
                stream.write(data)
                data = wf.readframes(1024)
                
                if keyboard.is_pressed('q'):
                    print("\n'q' pressed. Stopping playback.")
                    raise KeyboardInterrupt
    except KeyboardInterrupt:
        pass

    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()
    print("Playback stopped.")

if __name__ == "__main__":
    loop_play("output.wav")