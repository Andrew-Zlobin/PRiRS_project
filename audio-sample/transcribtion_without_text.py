import torch
import torchaudio
import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from phonemizer import phonemize

# Load the pretrained Wav2Vec2 ASR model
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

# Load and preprocess the audio file
audio_path = "example_2.wav"
waveform, sample_rate = librosa.load(audio_path, sr=16000)

# Convert to tensor
input_values = processor(waveform, return_tensors="pt", sampling_rate=16000).input_values

# Get ASR output (word transcription)
with torch.no_grad():
    logits = model(input_values).logits

# Decode the transcription
predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.batch_decode(predicted_ids)[0]

# Convert text to phonemes
phoneme_transcription = phonemize(transcription, language="en-us", backend="espeak")

print("Transcribed Text:", transcription)
print("Phoneme Transcription:", phoneme_transcription)