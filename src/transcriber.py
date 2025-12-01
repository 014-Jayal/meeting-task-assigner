import speech_recognition as sr
import os

def transcribe_audio(file_path):
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    # Validation: Check if file exists
    if not os.path.exists(file_path):
        return "Error: Audio file not found."

    print(f"Loading audio file: {file_path}")
    
    try:
        # Load the audio file
        with sr.AudioFile(file_path) as source:
            print("Processing audio...")
            # Record the data from the file
            audio_data = recognizer.record(source)
            
            print("Transcribing via Google Web Speech API...")
            # Send to Google for transcription
            text = recognizer.recognize_google(audio_data)
            return text
            
    except sr.UnknownValueError:
        return "Error: Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Error: Could not request results from Google Service; {e}"
    except ValueError:
        return "Error: Audio file format not supported. Please use .wav files."
