import speech_recognition as sr
from phonemizer import phonemize
import jiwer  # For phoneme comparison

# Load and transcribe audio
recognizer = sr.Recognizer()
audio_file = "example.wav"

with sr.AudioFile(audio_file) as source:
    audio_data = recognizer.record(source)
    text = recognizer.recognize_google(audio_data)  # Convert speech to text

# Convert to phonemes (CMU or eSpeak)
phonemes_spoken = phonemize(text, language="en-us", backend="espeak")

# Define the correct pronunciation (ground truth)
correct_text = "what I'm wasting my life on"  # Replace with correct text
correct_phonemes = phonemize(correct_text, language="en-us", backend="espeak")

print("Spoken Text:", text)
print("Spoken Phonemes:", phonemes_spoken)
print("Correct Phonemes:", correct_phonemes)

from jiwer import wer

# Compute Word Error Rate (WER) for phoneme comparison
phoneme_error_rate = wer(correct_phonemes, phonemes_spoken)

print(f"Phoneme Error Rate: {phoneme_error_rate:.2f}")


# Spoken Text: what I'm wasting my life on
# Spoken Phonemes: wʌt aɪm weɪstɪŋ maɪ laɪf ɑːn 
# Correct Phonemes: wʌt aɪm weɪstɪŋ maɪ laɪf ɑːn 
# Phoneme Error Rate: 0.00