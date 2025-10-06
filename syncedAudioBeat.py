import pygame
import wave
import pyaudio
import threading
import numpy as np
import soundfile as sf
import scipy.signal as signal
import time
import keyboard

def beat_visualizer(filename):
    # --- Load audio ---
    y, sr = sf.read(filename)
    if len(y.shape) > 1:
        y = np.mean(y, axis=1)

    onset_env = np.abs(y)
    b, a = signal.butter(2, 0.01)
    onset_env_smooth = signal.filtfilt(b, a, onset_env)
    peaks, _ = signal.find_peaks(
        onset_env_smooth,
        height=np.max(onset_env_smooth) * 0.3,
        distance=sr * 0.2
    )
    beat_times = peaks / sr
    print(f"Detected {len(beat_times)} beats.")

    # --- Shared state ---
    stop_flag = False
    frames_played = 0
    beat_index = 0

    # --- Audio thread ---
    def play_audio():
        nonlocal frames_played, beat_index, stop_flag
        wf = wave.open(filename, 'rb')
        p_audio = pyaudio.PyAudio()
        stream = p_audio.open(
            format=p_audio.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )
        chunk = 1024
        try:
            while not stop_flag:
                wf.rewind()
                frames_played = 0
                beat_index = 0
                data = wf.readframes(chunk)
                while data and not stop_flag:
                    stream.write(data)
                    frames_played += len(data) // wf.getsampwidth() // wf.getnchannels()
                    data = wf.readframes(chunk)
        finally:
            stream.stop_stream()
            stream.close()
            p_audio.terminate()
            wf.close()

    # --- Visualization ---
    pygame.init()
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Beat Visualizer")
    clock = pygame.time.Clock()
    circle_radius = 50
    pulse = 0

    def visualize_beats():
        nonlocal pulse, beat_index, frames_played, stop_flag
        while not stop_flag:
            if beat_times.size > 0:
                playback_time = frames_played / sr
                if beat_index < len(beat_times) and playback_time >= beat_times[beat_index]:
                    pulse = 1.5
                    beat_index += 1
            screen.fill((0, 0, 0))
            radius = int(circle_radius * (1 + 0.5 * pulse))
            color_intensity = min(255, int(255 * pulse))
            pygame.draw.circle(
                screen,
                (color_intensity, 50, 255 - color_intensity),
                (WIDTH // 2, HEIGHT // 2),
                radius
            )
            pulse *= 0.9
            pygame.display.flip()
            clock.tick(60)

    # --- Stop listener ---
    def listen_stop():
        nonlocal stop_flag
        keyboard.wait('q')
        stop_flag = True
        print("\n'q' pressed. Stopping visualizer...")

    # --- Threads ---
    audio_thread = threading.Thread(target=play_audio)
    visual_thread = threading.Thread(target=visualize_beats)
    stop_thread = threading.Thread(target=listen_stop)

    audio_thread.start()
    visual_thread.start()
    stop_thread.start()

    try:
        running = True
        while running and not stop_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_flag = True
                    running = False
            time.sleep(0.05)
    except KeyboardInterrupt:
        stop_flag = True

    audio_thread.join()
    visual_thread.join()
    stop_thread.join()
    pygame.quit()
    print("Playback and visualization stopped.")
