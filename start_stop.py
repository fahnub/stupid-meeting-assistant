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

def record_audio(stop_event):
    print("Starting recording thread...")
    try:
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        frames = []
        while not stop_event.is_set():  # Check if stop event is signaled
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        file_path = os.path.abspath(OUTPUT_FILENAME)
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

    # Use threading.Event for signaling the recording thread
    if 'stop_event' not in st.session_state:
        st.session_state.stop_event = threading.Event()

    if st.button('Start Recording'):
        if not st.session_state.stop_event.is_set():
            st.session_state.stop_event.clear()  # Reset the event
            threading.Thread(target=record_audio, args=(st.session_state.stop_event,)).start()

    if st.button('Stop Recording'):
        st.session_state.stop_event.set()  # Signal the thread to stop

    st.write("Press 'Start Recording' to begin and 'Stop Recording' to end.")

if __name__ == "__main__":
    main()
