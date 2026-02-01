import os
import shutil
import logging
from enum import Enum
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

class TaskType(Enum):
    SIMPLE_CHAT = 'simple_chat'
    SKILL_EXECUTION = 'skill_exec'
    BUSINESS_WRITING = 'writing'
    BUILDING = 'building'

def classify_task(prompt: str, skill_name: Optional[str] = None) -> TaskType:
    import re
    
    building_keywords = ['build', 'create app', 'create a ', 'make a', 'generate report',
                        'generate a ', 'write code', 'implement', 'deploy', 'install',
                        'monthly report', 'billing report', 'case report']
    simple_keywords = ['good morning', 'hello', 'what time', 'remind me',
                      "what's on my", 'schedule', 'weather', 'remember',
                      'what did we', 'yesterday', 'last time', 'show me my',
                      'how are you', 'thank', 'good night', 'good evening',
                      'what can you do']
    # Short keywords that need word-boundary matching to avoid false positives
    simple_word_keywords = ['hi', 'hey']
    
    prompt_lower = prompt.lower()
    
    if skill_name and not any(kw in prompt_lower for kw in building_keywords):
        return TaskType.SKILL_EXECUTION
    if any(kw in prompt_lower for kw in building_keywords):
        return TaskType.BUILDING
    if any(kw in prompt_lower for kw in simple_keywords):
        return TaskType.SIMPLE_CHAT
    if any(re.search(r'\b' + re.escape(kw) + r'\b', prompt_lower) for kw in simple_word_keywords):
        return TaskType.SIMPLE_CHAT
    return TaskType.BUSINESS_WRITING

def select_model(task_type: TaskType) -> str:
    gemini_key = os.getenv('GEMINI_API_KEY')
    claude_available = shutil.which('claude') is not None
    
    routing = {
        TaskType.SIMPLE_CHAT: 'gemini-flash' if gemini_key else 'claude',
        TaskType.SKILL_EXECUTION: 'gemini-flash' if gemini_key else 'claude',
        TaskType.BUSINESS_WRITING: 'gemini-pro' if gemini_key else 'claude',
        TaskType.BUILDING: 'claude' if claude_available else ('gemini-pro' if gemini_key else 'claude'),
    }
    
    selected = routing.get(task_type, 'gemini-flash' if gemini_key else 'claude')
    logger.info(f'Router: task_type={task_type.value} -> model={selected} (gemini_key={bool(gemini_key)}, claude={claude_available})')
    return selected

async def execute_gemini(
    prompt: str,
    model: str = 'gemini-2.0-flash',
    context: str = '',
    history: str = ''
) -> Tuple[Optional[str], bool]:
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.warning('No GEMINI_API_KEY set, falling back to Claude')
            return None, False
        
        genai.configure(api_key=api_key)
        model_instance = genai.GenerativeModel(model)
        
        full_prompt = ''
        if context:
            full_prompt += context + '\n\n'
        if history:
            full_prompt += history + '\n\n'
        full_prompt += prompt
        
        logger.info(f'Executing via Gemini model={model}, prompt_length={len(full_prompt)}')
        
        response = await model_instance.generate_content_async(full_prompt)
        
        if response and response.text:
            logger.info(f'Gemini response received, length={len(response.text)}')
            return response.text, True
        else:
            logger.warning('Gemini returned empty response, falling back to Claude')
            return None, False
            
    except Exception as e:
        logger.error(f'Gemini execution failed: {e}, falling back to Claude')
        return None, False
