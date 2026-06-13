"""
Speech recognition helper utilities.
"""
import os
from google.cloud import speech_v1
from google.api_core.gapic_v1 import client_info as grpc_client_info

def transcribe_audio(audio_content: bytes, language_code: str = "en-US") -> str:
    """
    Transcribe audio using Google Cloud Speech-to-Text API.
    
    Args:
        audio_content: Raw audio bytes
        language_code: Language code (default: en-US)
    
    Returns:
        str: Transcribed text
    """
    try:
        client = speech_v1.SpeechClient()
        
        audio = speech_v1.RecognitionAudio(content=audio_content)
        config = speech_v1.RecognitionConfig(
            encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
        )
        
        response = client.recognize(config=config, audio=audio)
        
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript
        
        return transcript.strip()
    
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return ""

def validate_audio_format(audio_data: bytes) -> bool:
    """
    Validate if audio data is in acceptable format.
    
    Args:
        audio_data: Audio bytes to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    # Check if audio is at least 1KB (basic validation)
    return len(audio_data) >= 1000
