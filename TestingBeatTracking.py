import soundfile as sf
import numpy as np
import scipy.signal as signal
import time

filename = "output.wav"
y, sr = sf.read(filename)

if len(y.shape) > 1:
    y = np.mean(y, axis=1)

onset_env = np.abs(y)
b, a = signal.butter(2, 0.01)
onset_env_smooth = signal.filtfilt(b, a, onset_env)

peaks, _ = signal.find_peaks(onset_env_smooth, height=np.max(onset_env_smooth)*0.3, distance=sr*0.2)
beat_times = peaks / sr

print("Detected beat times (seconds):", beat_times)

print("\nTracking beats in real time... Press Ctrl+C to stop.\n")
start_time = time.time()

try:
    beat_index = 0
    while beat_index < len(beat_times):
        current_time = time.time() - start_time
        if current_time >= beat_times[beat_index]:
            print("Beat detected!")
            beat_index += 1
        else:
            time.sleep(0.01)
except KeyboardInterrupt:
    print("\nBeat tracking stopped.")
