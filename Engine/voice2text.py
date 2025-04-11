import os
import sounddevice as sd
import scipy.io.wavfile as wav
from groq import Groq
from Engine.driver import load_config

config = load_config('llm_config.yaml')
GROQ_API_KEY = config['groq']['api']['key5']


MODEL = config['groq']['model']['whisper-large-v3'].replace("groq/", "")

def record_audio(filename: str = "recording.wav", duration: int = 10, fs: int = 44100) -> str:
    """
    Records audio from the microphone for a given duration and saves it as a WAV file.
    """
    print(f"🎙️ Recording for {duration} seconds... Speak now!")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, fs, recording)
    print(f"✅ Audio saved to: {filename}")
    return filename

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes an audio file using Groq Whisper and returns the text.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    print("🔐 Connecting to Groq Whisper...")
    client = Groq(api_key=GROQ_API_KEY)

    with open(file_path, "rb") as f:
        response = client.audio.transcriptions.create(
            file=(os.path.basename(file_path), f.read()),
            model=MODEL,
            response_format="verbose_json"
        )

    print("✅ Transcription complete.")
    return response.text

def main():
    print("🎤 Voice Recorder + Transcriber")
    duration = int(input("⏱️ Enter recording duration (seconds): "))
    audio_path = record_audio(duration=duration)
    transcript = transcribe_audio(audio_path)
    print("\n📝 Transcribed Text:\n")
    print(transcript)

if __name__ == "__main__":
    main()
