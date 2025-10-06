import os
from recording import record_audio
from syncedAudioBeat import beat_visualizer

def main():
    print("=== Beat Visualizer ===")
    print("1. Record your own audio")
    print("2. Use preset example: Low Beats.wav")
    print("3. Use preset example: High Beats.wav")
    choice = input("Choose an option (1-3): ")

    if choice == '1':
        record_audio("output.wav")
        file_to_play = "output.wav"
    elif choice == '2':
        file_to_play = "Low Beats.wav"
    elif choice == '3':
        file_to_play = "High Beats.wav"
    else:
        print("Invalid choice.")
        return

    if not os.path.exists(file_to_play):
        print(f"File {file_to_play} not found!")
        return

    beat_visualizer(file_to_play)

if __name__ == "__main__":
    main()
