# Multi-Model Routing Spec

## Current State
- All tasks go through `execute_claude()` in executor.py
- Shells out to `claude` CLI subprocess
- Requires Claude subscription ($20-100/month)

## Target State
- Simple tasks → Gemini Flash API (FREE)
- Medium tasks → Gemini Pro API (cheap)
- Complex/building tasks → Claude CLI (existing path)
- Router decides based on task classification

## New Module: `model_router.py`

### Task Classification
```python
class TaskType(Enum):
    SIMPLE_CHAT = "simple_chat"       # greetings, Q&A, memory recall
    SKILL_EXECUTION = "skill_exec"    # pre-built skill triggers
    BUSINESS_WRITING = "writing"      # emails, letters, analysis
    BUILDING = "building"             # apps, reports, dashboards, code
    
def classify_task(prompt: str, skill_name: Optional[str] = None) -> TaskType:
    """Classify task to route to cheapest capable model."""
    
    # Building indicators
    building_keywords = ["build", "create app", "make a", "generate report", 
                        "write code", "implement", "deploy", "install"]
    
    # Simple chat indicators  
    simple_keywords = ["good morning", "hello", "hi", "what time", "remind me",
                      "what's on my", "schedule", "weather", "remember"]
    
    # If a skill is active, most skills work on Gemini
    if skill_name and not any(kw in prompt.lower() for kw in building_keywords):
        return TaskType.SKILL_EXECUTION
    
    if any(kw in prompt.lower() for kw in building_keywords):
        return TaskType.BUILDING
    
    if any(kw in prompt.lower() for kw in simple_keywords):
        return TaskType.SIMPLE_CHAT
    
    return TaskType.BUSINESS_WRITING  # default to medium tier
```

### Model Selection
```python
def select_model(task_type: TaskType) -> str:
    """Select the cheapest model that can handle this task type."""
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    claude_available = shutil.which("claude") is not None
    
    routing = {
        TaskType.SIMPLE_CHAT: "gemini-flash" if gemini_key else "claude",
        TaskType.SKILL_EXECUTION: "gemini-flash" if gemini_key else "claude",
        TaskType.BUSINESS_WRITING: "gemini-pro" if gemini_key else "claude",
        TaskType.BUILDING: "claude" if claude_available else "gemini-pro",
    }
    
    return routing.get(task_type, "gemini-flash" if gemini_key else "claude")
```

### Gemini Execution Path
```python
async def execute_gemini(
    prompt: str,
    model: str = "gemini-2.0-flash",  # or gemini-2.0-pro
    context: str = "",
    history: str = ""
) -> Tuple[str, bool]:
    """Execute via Gemini API (no CLI needed)."""
    
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    model_instance = genai.GenerativeModel(model)
    
    full_prompt = f"{context}\n\n{history}\n\n{prompt}"
    
    response = await model_instance.generate_content_async(full_prompt)
    return response.text, True
```

### Integration with executor.py

In `execute_claude()`, add routing at the top:
```python
# NEW: Route to cheapest capable model
from model_router import classify_task, select_model, execute_gemini

task_type = classify_task(prompt, skill_name)
model = select_model(task_type)

if model.startswith("gemini"):
    # Build context same as Claude path
    context = await _build_context(project)
    history = _format_history_for_prompt()
    gemini_model = "gemini-2.0-flash" if model == "gemini-flash" else "gemini-2.0-pro"
    return await execute_gemini(prompt, model=gemini_model, context=context, history=history)

# Otherwise fall through to existing Claude CLI path...
```

## Dependencies
- `pip install google-generativeai` (add to requirements.txt)
- GEMINI_API_KEY env var (already in .env.example)

## Config
- Users can override routing via KIYOMI_DEFAULT_MODEL env var
- If no Gemini key, falls back to Claude for everything
- If no Claude CLI, falls back to Gemini for everything
