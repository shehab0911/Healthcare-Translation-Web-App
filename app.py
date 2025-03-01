import whisper
import gradio as gr
import time
from faster_whisper import WhisperModel as FasterWhisperModel
from transformers import MarianMTModel, MarianTokenizer
from TTS.api import TTS
import torch
import tempfile
import os
import re

# Initialize TTS engine
tts_engine = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False, gpu=False)

# Load Faster Whisper Model
device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if device == "cuda" else "int8"
model_faster_whisper = FasterWhisperModel("small", device=device, compute_type=compute_type)

# Cache translation models
translation_model_cache = {}

def load_translation_model(src_lang, tgt_lang):
    """Load and cache translation models for faster performance."""
    cache_key = f"{src_lang}-{tgt_lang}"
    if cache_key not in translation_model_cache:
        model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name).to(device)
        translation_model_cache[cache_key] = (model, tokenizer)
    return translation_model_cache[cache_key]

def split_text(text, max_length=512):
    """Split long text into smaller chunks to avoid token overflow in translation."""
    sentences = re.split(r'(?<=[.!?])\s+', text)  # Split by sentence
    chunks, current_chunk = [], ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def translate_text(text, src_lang, tgt_lang):
    """Efficient translation with text chunking to prevent token limit issues."""
    if src_lang == tgt_lang or not text.strip():
        return text

    model, tokenizer = load_translation_model(src_lang, tgt_lang)

    text_chunks = split_text(text)
    translated_chunks = []

    for chunk in text_chunks:
        inputs = tokenizer([chunk], return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
        translated_tokens = model.generate(**inputs, num_beams=1)  # Use greedy decoding for speed
        translated_text = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        translated_chunks.append(translated_text)

    return " ".join(translated_chunks)

# Mapping full language names to codes
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Russian": "ru",
    "Chinese": "zh",
    "Japanese": "ja",
    "Arabic": "ar",
    "Portuguese": "pt",
    "Italian": "it",
    "Korean": "ko",
    "Dutch": "nl",
}

def transcribe(audio, use_faster, input_lang_full, output_lang_full):
    """Transcribe, translate, and convert speech to text efficiently for long audio files."""
    try:
        audio_data = whisper.load_audio(audio)
    except Exception as e:
        return f"Error loading audio: {e}", None, None, None

    # Convert full language names to codes
    input_lang = LANGUAGES.get(input_lang_full, "en")
    output_lang = LANGUAGES.get(output_lang_full, "en")

    # Transcription
    start_time = time.time()
    if use_faster:
        segments, _ = model_faster_whisper.transcribe(audio_data, language=input_lang)
        transcription = " ".join([seg.text for seg in segments]).strip()
    else:
        model = whisper.load_model("small")
        result = model.transcribe(audio_data, language=input_lang)
        transcription = result["text"].strip()
    inference_time = time.time() - start_time

    # Translation (handles long text)
    translated_text = translate_text(transcription, input_lang, output_lang)

    # Generate translated speech
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            audio_output_path = temp_audio_file.name

            if output_lang not in tts_engine.languages:
                output_lang = "en"
                print(f"Output language '{output_lang}' is not supported. Falling back to English.")

            speaker = tts_engine.speakers[0] if tts_engine.speakers else None
            if not speaker:
                raise ValueError("No available speakers found in TTS engine.")

            tts_engine.tts_to_file(
                text=translated_text,
                speaker=speaker,
                language=output_lang,
                file_path=audio_output_path
            )

    except Exception as e:
        return f"TTS Error: {e}", None, None, None

    return transcription, inference_time, translated_text, audio_output_path

# Gradio Interface
interface = gr.Interface(
    title="Healthcare Translation Web App",
    fn=transcribe,
    inputs=[
        gr.Audio(type="filepath"),
        gr.Checkbox(label="Use Faster-Whisper"),
        gr.Dropdown(list(LANGUAGES.keys()), label="Input Language", value="English"),
        gr.Dropdown(list(LANGUAGES.keys()), label="Output Language", value="English"),
    ],
    outputs=[
        gr.Textbox(label="Transcription"),
        gr.Number(label="Inference Time (seconds)"),
        gr.Textbox(label="Translated Text"),
        gr.Audio(label="Translated Audio"),
    ],
    live=False  # Processes only when the "Submit" button is clicked
)

interface.launch()
