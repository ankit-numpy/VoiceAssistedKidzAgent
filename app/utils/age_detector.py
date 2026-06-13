"""
Age detection helper utilities.
"""
import os
from openai import AzureOpenAI

def detect_age_from_voice(audio_sample: str, voice_features: dict = None) -> tuple:
    """
    Detect approximate age from voice sample.
    Uses multiple heuristics: pitch, speech pattern, word choice.
    
    Args:
        audio_sample: Transcribed text or audio features
        voice_features: Optional dict with extracted voice characteristics
        
    Returns:
        tuple: (detected_age, confidence_score) where age is 5-12, confidence is 0-1
    """
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_API_KEY"),
        api_version="2024-02-15-preview",
        azure_endpoint=os.getenv("AZURE_ENDPOINT")
    )
    
    prompt = f"""Analyze the following text and estimate the speaker's age range. 
The speaker is likely between 5-12 years old. Base your estimate on:
- Vocabulary complexity
- Sentence structure
- Grammar patterns
- Word choices
- Speech formality

Text: "{audio_sample}"

Respond with JSON: {{"age": <single number 5-12>, "confidence": <float 0-1>, "reasoning": "<brief explanation>"}}

Be conservative - when unsure, default to middle range (7-8)."""

    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4"),
            messages=[
                {"role": "system", "content": "You are an age detection expert analyzing children's speech patterns. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=150
        )
        
        import json
        response_text = response.choices[0].message.content
        data = json.loads(response_text)
        
        age = max(5, min(12, int(data.get("age", 7))))  # Clamp to 5-12
        confidence = float(data.get("confidence", 0.5))
        
        return age, confidence
    
    except Exception as e:
        print(f"Error detecting age: {e}")
        return 7, 0.3  # Default to middle age with low confidence

def get_age_category(age: int) -> str:
    """
    Get age category for content filtering.
    
    Args:
        age: Detected or provided age (5-12)
        
    Returns:
        str: Category name (early_reader, elementary, upper_elementary)
    """
    if age <= 6:
        return "early_reader"  # Preschool/K-1st grade
    elif age <= 8:
        return "elementary"     # 2nd-3rd grade
    elif age <= 10:
        return "middle_elementary"  # 4th-5th grade
    else:
        return "upper_elementary"   # 6th+ grade

def get_age_description(age: int) -> str:
    """Get human-readable age description."""
    if age <= 6:
        return "Early Reader (K-1st Grade)"
    elif age <= 8:
        return "Elementary Reader (2nd-3rd Grade)"
    elif age <= 10:
        return "Middle Elementary (4th-5th Grade)"
    else:
        return "Upper Elementary (6th+ Grade)"
