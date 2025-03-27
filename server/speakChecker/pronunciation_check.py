import torch
import torchaudio
import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from phonemizer import phonemize

from pydub import AudioSegment
import io
import numpy as np
from difflib import SequenceMatcher

def compare_phonemes(reference: str, checked: str):

    ref_words = reference.split()
    checked_words = checked.split()
    
    # ref_words = list(reference)
    # checked_words = list(checked)

    matcher = SequenceMatcher(None, ref_words, checked_words)
    print(matcher.get_opcodes())
    differences = []
    expected_words_with_errors = []
    recived_words_with_errors = []
    error_types = []
    indexes_of_errors = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != 'equal':
            differences.append((tag, ref_words[i1:i2], checked_words[j1:j2]))
            expected_words_with_errors.extend(ref_words[i1:i2])
            recived_words_with_errors.extend(checked_words[j1:j2])


    for word in expected_words_with_errors:
        indexes_of_errors.append(ref_words.index(word))
    for exp, rec in zip(expected_words_with_errors, recived_words_with_errors):
        error_types_matcher = SequenceMatcher(None, exp, rec)
        error_counter = {"replace" : 0,
                         "delete" : 0,
                         "insert" : 0
                         }
        for tag, i1, i2, j1, j2 in error_types_matcher.get_opcodes():
            if tag != "equal":
                error_counter[tag] += 1
        error_types.append(max(error_counter, key=error_counter.get))
    return {"expected_words_with_errors" : expected_words_with_errors,
            "recived_words_with_errors" : recived_words_with_errors,
            "error_types" : error_types,
            "indexes_of_errors" : indexes_of_errors,}




class PronunciationModel:
    def __init__(self):
        # Load the pretrained Wav2Vec2 ASR model
        self.processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
        self.model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")


    def get_transcribtion(self, waveform):

        input_values = self.processor(waveform, return_tensors="pt", sampling_rate=16000).input_values

        with torch.no_grad():
            logits = self.model(input_values).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]
        print("processed transcription" , transcription)
        phoneme_transcription = phonemize(transcription, language="en-us", backend="espeak")
        return phoneme_transcription

    def evaluate_task(self, correct_sentence, recived_audio):
        print("try to reformat audio")

        audio_segment = AudioSegment.from_file(io.BytesIO(recived_audio), format="webm")
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        
        audio_path = "output.wav"
        with open(audio_path, "wb") as f:
            f.write(wav_io.getvalue())
        # Load into librosa
        wav_io.seek(0)  # Reset buffer position
        waveform, sr = librosa.load(wav_io, sr=16000)
        print("try to get transcribtion")

        user_phoneme = self.get_transcribtion(waveform)
        correct_phoneme = phonemize(correct_sentence, language="en-us", backend="espeak")
        print("user Transcription:", user_phoneme)
        print("correct text: ", correct_sentence)
        print("correct text: ", correct_phoneme)
        return compare_phonemes(correct_phoneme, user_phoneme)