# Phase 5: Fine-Tuning - Data Collection Guide

## Overview

Phase 5 focuses on collecting 50,000 high-quality training examples to fine-tune a custom Cerberus AI model.

## Architecture

```
User Interaction
    ↓
ConversationLogger (anonymized)
    ↓
JSONL Files (data/training_logs/)
    ↓
FeedbackCollector (user ratings)
    ↓
DataCurator (quality filtering)
    ↓
Training Dataset (data/curated/)
```

## Components

### 1. ConversationLogger
Logs all user-AI interactions with anonymization:
- Hashes user IDs (SHA-256)
- Removes PII from messages
- Stores in daily JSONL files
- Tracks metadata (language, framework, complexity)

### 2. FeedbackCollector
Collects user feedback:
- 1-5 star ratings
- Optional comments
- Links feedback to conversation IDs

### 3. DataCurator
Filters and exports training data:
- Quality criteria: feedback ≥4 stars, response length ≥50 chars
- Statistics dashboard
- JSONL export for fine-tuning

## Integration

### Backend Integration

Add to `process_question` use case:

```python
from src.infrastructure.training.conversation_logger import ConversationLogger

logger = ConversationLogger()

# After generating response
example_id = logger.log_conversation(
    user_id=user.id,
    session_id=session.id,
    user_message=question.content,
    assistant_message=answer.content,
    context=session.context,
    language=detect_language(question.content),
    framework=detect_framework(question.content),
    complexity=answer.complexity
)

# Return example_id to frontend for feedback
```

### Frontend Integration

Add feedback UI to Chat component:

```jsx
const [feedbackId, setFeedbackId] = useState(null);

// After receiving response
setFeedbackId(response.example_id);

// Feedback UI
<div className="feedback">
  <span>Was this helpful?</span>
  {[1,2,3,4,5].map(score => (
    <button onClick={() => submitFeedback(feedbackId, score)}>
      ⭐ {score}
    </button>
  ))}
</div>
```

### API Endpoint

Add to `public_routes.py`:

```python
@router.post("/v1/feedback")
async def submit_feedback(
    example_id: str,
    score: int,
    comment: Optional[str] = None
):
    collector = FeedbackCollector(logger)
    collector.submit_feedback(example_id, score, comment)
    return {"status": "success"}
```

## CLI Usage

### View Statistics
```bash
python -m src.infrastructure.training.curator_cli stats
```

### Export Training Data
```bash
python -m src.infrastructure.training.curator_cli export --output training_v1.jsonl
```

### Check Progress
```bash
python -m src.infrastructure.training.curator_cli progress
```

## Data Quality Criteria

High-quality examples must meet:
1. **Feedback Score**: ≥4 stars (or no feedback)
2. **Response Length**: ≥50 characters
3. **No PII**: Anonymized user data
4. **Complete Context**: User message + assistant response

## Privacy & Compliance

### Anonymization
- User IDs hashed (SHA-256, 16 chars)
- No email addresses stored
- No IP addresses logged
- Session IDs anonymized

### GDPR Compliance
- Users can request data deletion
- Opt-out mechanism available
- Data retention: 90 days before curation
- Curated data: fully anonymized

### Data Storage
```
data/
├── training_logs/          # Raw logs (90 days retention)
│   ├── conversations_2024-01-15.jsonl
│   ├── feedback.jsonl
│   └── comments.jsonl
└── curated/                # Curated datasets (permanent)
    └── training_data.jsonl
```

## Progress Tracking

### Goal: 50,000 Examples

**Estimated Timeline:**
- 100 users × 10 conversations/day = 1,000 examples/day
- 50,000 examples ÷ 1,000/day = **50 days**

**Quality Rate:**
- Assume 60% high-quality rate
- Need 83,333 total conversations
- **83 days** to reach goal

### Milestones
- ✅ 0-1k: Infrastructure setup
- [ ] 1k-5k: Initial dataset
- [ ] 5k-10k: First fine-tuning experiment
- [ ] 10k-25k: Model v1 training
- [ ] 25k-50k: Production model

## Next Steps (Phase 5 Continuation)

After collecting 50k examples:

1. **Model Selection**
   - CodeLlama 13B (code-focused)
   - Mistral 7B (general purpose)
   - Phi-3 (efficient, small)

2. **Infrastructure**
   - GPU: A100 (40GB) or H100 (80GB)
   - Training framework: HuggingFace Transformers
   - Distributed training: DeepSpeed

3. **Fine-Tuning**
   - LoRA (Low-Rank Adaptation) for efficiency
   - 3-5 epochs
   - Learning rate: 2e-5
   - Batch size: 4-8

4. **Evaluation**
   - Hold-out test set (10%)
   - Metrics: Perplexity, BLEU, CodeBLEU
   - Human evaluation

5. **Deployment**
   - Serve with vLLM or TGI
   - A/B testing vs current models
   - Gradual rollout (10% → 50% → 100%)

## Monitoring

Track these metrics:
- **Collection Rate**: Examples/day
- **Quality Rate**: High-quality %
- **Feedback Rate**: Users providing feedback %
- **Language Distribution**: Python, JS, etc.
- **Framework Coverage**: FastAPI, React, etc.

## Cost Estimation

### Storage
- 1 example ≈ 2KB (JSON)
- 50k examples ≈ 100MB
- **Cost**: Negligible (local storage)

### Fine-Tuning (Future)
- A100 GPU: $1.50/hour
- Training time: 24-48 hours
- **Cost**: $36-72 per training run

### Inference (Future)
- A100 GPU: $1.50/hour
- 24/7 operation: $1,080/month
- Alternative: Serverless (RunPod, Modal)

---

**Cerberus AI** - Developer Assistant by Focus AI
