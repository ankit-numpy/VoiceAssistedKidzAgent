"""
LLM helper utilities using Azure Copilot.
"""
import os
from openai import AzureOpenAI

def get_llm_client():
    """Initialize Azure OpenAI client."""
    return AzureOpenAI(
        api_key=os.getenv("AZURE_API_KEY"),
        api_version="2024-02-15-preview",
        azure_endpoint=os.getenv("AZURE_ENDPOINT")
    )

def get_correction_and_explanation(expected_word: str, spoken_word: str, is_correct: bool):
    """
    Get AI-generated correction and kid-friendly explanation.
    
    Args:
        expected_word: The word in the passage
        spoken_word: The word the child spoke
        is_correct: Whether the child read it correctly
    
    Returns:
        tuple: (correction, explanation)
    """
    if is_correct:
        return "", ""
    
    client = get_llm_client()
    
    prompt = f"""You are a friendly reading tutor for 5-8 year old children. 
    
A child tried to read the word "{expected_word}" but said "{spoken_word}" instead.

Please provide:
1. A VERY SHORT, kid-friendly correction (1-2 sentences max): how to pronounce the word correctly
2. A VERY SHORT, kid-friendly explanation (1-2 sentences max): what the word means

Format your response as JSON with keys "correction" and "explanation". Use simple words only. Be encouraging!

Example:
{{"correction": "It's pronounced 'but-er-fly'", "explanation": "A butterfly is a pretty insect with colorful wings!"}}"""
    
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4"),
            messages=[
                {"role": "system", "content": "You are a helpful tutor for young children. Keep responses very short, encouraging, and use only simple words."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        import json
        response_text = response.choices[0].message.content
        data = json.loads(response_text)
        return data.get("correction", ""), data.get("explanation", "")
    
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return "", ""

def generate_encouragement(child_name: str, accuracy: float):
    """
    Generate personalized encouragement message.
    
    Args:
        child_name: Child's name
        accuracy: Reading accuracy percentage (0-100)
    
    Returns:
        str: Encouraging message
    """
    if accuracy >= 90:
        message = f"Amazing work, {child_name}! You read with great accuracy!"
    elif accuracy >= 75:
        message = f"Excellent job, {child_name}! You're a strong reader!"
    elif accuracy >= 60:
        message = f"Great effort, {child_name}! You're improving every day!"
    else:
        message = f"Keep practicing, {child_name}! You're doing great!"
    
    return message

def answer_question(question: str, age: int, context: str = "") -> str:
    """
    Generate an age-appropriate answer to a question using Azure Copilot.
    
    Args:
        question: The question asked by the child
        age: Detected or provided age (5-12)
        context: Optional context or previous messages
        
    Returns:
        str: Age-appropriate answer
    """
    from app.utils.age_detector import get_age_category, get_age_description
    
    age_category = get_age_category(age)
    age_description = get_age_description(age)
    
    # Age-specific prompts
    age_prompts = {
        "early_reader": "Use very simple words (1-2 syllables). Use short sentences. Include analogies to toys, animals, or everyday objects.",
        "elementary": "Use simple words and short sentences. Include 1-2 examples. Avoid complex abstract concepts.",
        "middle_elementary": "Use clear explanations with concrete examples. Can include some more complex ideas with analogies.",
        "upper_elementary": "Provide detailed explanations. Include examples and interesting facts. Can discuss more abstract concepts."
    }
    
    system_prompt = f"""You are a friendly, helpful tutor for children ages {age} ({age_description}).
{age_prompts.get(age_category, "Use simple, clear language.")}

Answer questions in a way that is:
- Age-appropriate and engaging
- Encouraging and positive
- Factually accurate but simplified
- Never scary, violent, or inappropriate
- Curious and fun

Keep your answer to 2-4 sentences maximum."""

    client = get_llm_client()
    
    try:
        messages = []
        if context:
            messages.append({"role": "system", "content": context})
        
        messages.append({"role": "user", "content": question})
        
        response = client.chat.completions.create(
            model=os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4"),
            messages=messages,
            system=system_prompt,
            temperature=0.7,
            max_tokens=200
        )
        
        answer = response.choices[0].message.content.strip()
        
        from app.utils.content_filter import sanitize_ai_response
        return sanitize_ai_response(answer)
    
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "That's a great question! I'm thinking about the best way to explain it to you."
