"""
Utilities package initialization.
"""
from app.utils.llm_helper import get_correction_and_explanation, generate_encouragement, answer_question
from app.utils.content_filter import is_safe_for_children, sanitize_ai_response, filter_reading_passage
from app.utils.speech_helper import transcribe_audio, validate_audio_format
from app.utils.age_detector import detect_age_from_voice, get_age_category, get_age_description

__all__ = [
    'get_correction_and_explanation',
    'generate_encouragement',
    'answer_question',
    'is_safe_for_children',
    'sanitize_ai_response',
    'filter_reading_passage',
    'transcribe_audio',
    'validate_audio_format',
    'detect_age_from_voice',
    'get_age_category',
    'get_age_description',
]
