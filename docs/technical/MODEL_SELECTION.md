# Model Selection Guide - Cerberus AI Fine-Tuning

## Comparison Matrix

| Model | Size | Context | Strengths | Weaknesses | Cost/Hour | Recommendation |
|-------|------|---------|-----------|------------|-----------|----------------|
| **CodeLlama 13B** | 13B | 16K | Code-focused, Python/JS expert | General knowledge limited | $1.50 | ⭐ Best for code |
| **Mistral 7B** | 7B | 8K | Fast, efficient, good general | Less code-specific | $0.80 | ⭐ Best balance |
| **Phi-3 Mini** | 3.8B | 4K | Very fast, low memory | Limited context | $0.40 | ⭐ Best for cost |

## Decision: **Mistral 7B Instruct v0.2**

### Why Mistral?

1. **Balance**: Good at both code and general developer questions
2. **Efficiency**: 7B parameters = faster inference, lower cost
3. **Context**: 8K tokens sufficient for most code tasks
4. **Community**: Strong ecosystem, proven fine-tuning results
5. **License**: Apache 2.0 (commercial use allowed)

### Technical Specs

```yaml
Model: mistralai/Mistral-7B-Instruct-v0.2
Parameters: 7.24B
Architecture: Transformer decoder
Vocabulary: 32K tokens
Context Length: 8192 tokens
Precision: FP16 / BF16
Memory Required: ~14GB (FP16)
```

## GPU Requirements

### Minimum (Training)
- **GPU**: NVIDIA A100 40GB
- **VRAM**: 40GB
- **Training Time**: 24-48 hours
- **Cost**: $1.50/hour = $36-72 total

### Recommended (Training)
- **GPU**: NVIDIA A100 80GB or H100
- **VRAM**: 80GB
- **Training Time**: 12-24 hours
- **Cost**: $2.50/hour = $30-60 total

### Inference (Production)
- **GPU**: NVIDIA T4 (16GB) or A10G (24GB)
- **VRAM**: 16GB minimum
- **Throughput**: ~50 tokens/sec
- **Cost**: $0.50/hour = $360/month

## Cloud Provider Options

### AWS
```yaml
Training: p4d.24xlarge (8x A100 80GB)
Cost: $32.77/hour
Inference: g5.xlarge (A10G 24GB)
Cost: $1.006/hour
```

### Google Cloud
```yaml
Training: a2-highgpu-1g (A100 40GB)
Cost: $3.67/hour
Inference: g2-standard-4 (L4 24GB)
Cost: $0.89/hour
```

### RunPod (Recommended for Cost)
```yaml
Training: A100 80GB
Cost: $1.89/hour
Inference: RTX 4090 24GB
Cost: $0.34/hour
```

## Dataset Preparation

### Format (JSONL)
```json
{
  "messages": [
    {"role": "system", "content": "You are Cerberus AI..."},
    {"role": "user", "content": "How to use FastAPI?"},
    {"role": "assistant", "content": "FastAPI is..."}
  ]
}
```

### Requirements
- **Minimum**: 10,000 examples
- **Recommended**: 50,000 examples
- **Quality**: 60%+ high-quality rate
- **Diversity**: 5+ programming languages

### Validation Split
```python
train_size = 0.9  # 45,000 examples
val_size = 0.1    # 5,000 examples
```

## Next Steps

1. **Provision GPU**: RunPod A100 80GB ($1.89/hour)
2. **Install Dependencies**: HuggingFace Transformers, PEFT, bitsandbytes
3. **Download Model**: `mistralai/Mistral-7B-Instruct-v0.2`
4. **Prepare Dataset**: Export 50k examples from curator
5. **Configure LoRA**: Rank=16, Alpha=32, Dropout=0.05
6. **Train**: 3 epochs, learning_rate=2e-5
7. **Evaluate**: Perplexity, BLEU, human eval
8. **Deploy**: vLLM or TGI for inference

---

**Decision Made**: Mistral 7B Instruct v0.2 ✅
