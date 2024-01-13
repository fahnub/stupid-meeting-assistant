import streamlit as st
import pyaudio
import wave
import threading
import os

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
OUTPUT_FILENAME = 'output.wav'

def record_audio():
    print("Starting recording thread...")
    try:
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        frames = []
        print("Recording for 5 seconds...")
        for _ in range(0, int(RATE / CHUNK * 5)):  # Record for 5 seconds
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        file_path = os.path.abspath(OUTPUT_FILENAME)
        print(f"Saving recording to {file_path}")
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        print(f"Recording saved successfully to {file_path}")
    except Exception as e:
        print(f"Error in recording: {e}")

def main():
    st.title("Audio Recorder")

    if st.button('Start Recording'):
        threading.Thread(target=record_audio).start()

    st.write("Press the button to start a 5-second recording.")

if __name__ == "__main__":
    main()
