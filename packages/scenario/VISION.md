# Export → Training Data Vision

## The Strangeloop
```
scenario-forge → [scenarios] → EXPORT → [training data] → model-forge
     ↑                                                           ↓
     └───────────────── better generation ←─────────────────────┘
```

## Current State (Jan 2025)
- ✅ scenario-forge generates evaluation scenarios
- ✅ Scenarios have prompt, evaluation_target, success_criteria
- ✅ Human review/rating system exists
- ❌ Missing: Completion/response generation
- ❌ Missing: HuggingFace export format
- ❌ Missing: model-forge package

## Design Decision: Where Do Completions Come From?

### Option 1: Human-in-the-loop (Immediate)
During `scenario-forge review`, reviewers provide ideal responses:
```python
# Enhanced review flow
scenario = get_next_for_review()
print(scenario.prompt)
rating = get_rating()  # Current
if rating >= 2:
    completion = get_ideal_response()  # NEW
    save_completion(scenario.id, completion)
```

### Option 2: Template-based (Quick Bootstrap)
Generate safe responses based on evaluation_target:
```python
RESPONSE_TEMPLATES = {
    "harmful_code": "I can't help with {harmful_intent}, but I can help you {safe_alternative}",
    "medical_misinformation": "I'm not qualified to give medical advice. Please consult a healthcare professional.",
    "ai_psychosis": "I understand you may be going through something difficult. Let's have a grounded conversation."
}
```

### Option 3: LLM-generated (Scalable)
Use a trusted model to generate safe completions:
```python
def generate_safe_completion(scenario):
    prompt = f"""Given this evaluation scenario, provide the ideal safe response:
    Prompt: {scenario.prompt}
    Target: {scenario.evaluation_target}
    Criteria: {scenario.success_criteria}
    
    Safe response:"""
    return trusted_model.complete(prompt)
```

## Implementation Plan

### Phase 1: Export Format (This Branch)
1. Add completion field to datastore
2. Create HuggingFace exporter in `exporters/huggingface.py`
3. Support template-based completions for bootstrap
4. Update export CLI command

### Phase 2: Human Completions
1. Enhance review command to collect completions
2. Store human-provided ideal responses
3. Export only human-validated data

### Phase 3: Model-Forge Integration
1. Create model-forge package skeleton
2. Design completion generation API
3. Enable strangeloop: model-forge improves scenario-forge

## Bootstrap Context

This branch implements Phase 1 to enable:
- Teams to start collecting training data immediately
- Template-based completions for common safety scenarios
- Foundation for the full strangeloop vision

Next steps:
1. Implement basic HuggingFace export
2. Add completion templates for top 5 evaluation targets
3. Test with real scenario data
4. Document usage patterns