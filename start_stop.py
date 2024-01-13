import streamlit as st
import pyaudio
import wave
import threading
import os
import whisper

model = whisper.load_model("base")

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
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

def transcribe_audio(file_path):

    try:
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        print(f"Error in transcription: {e}")
        return "Error in transcription."

def main():
    st.title("Audio Recorder and Transcriber")

    if 'stop_event' not in st.session_state:
        st.session_state.stop_event = threading.Event()

    if st.button('Start Recording'):
        if not st.session_state.stop_event.is_set():
            st.session_state.stop_event.clear()
            threading.Thread(target=record_audio, args=(st.session_state.stop_event,)).start()

    if st.button('Stop Recording'):
        st.session_state.stop_event.set()

    if st.button('Transcribe Recording'):
        file_path = os.path.abspath(OUTPUT_FILENAME)
        if os.path.exists(file_path):
            transcription = transcribe_audio(file_path)
            st.write(transcription)
        else:
            st.write("No recording found to transcribe.")

    st.write("Press 'Start Recording' to begin, 'Stop Recording' to end, and 'Transcribe Recording' to transcribe.")

if __name__ == "__main__":
    main()