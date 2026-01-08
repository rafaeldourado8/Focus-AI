# Phase 5: Model Base Setup Guide

## ✅ Decisions Made

### Model Selection
**Mistral 7B Instruct v0.2** - Best balance of performance, cost, and efficiency

### GPU Choice
**NVIDIA A100 80GB** via RunPod ($1.89/hour)

### Framework
**HuggingFace Transformers** with PEFT (LoRA)

---

## Setup Steps

### 1. Provision GPU Instance

#### RunPod (Recommended)
```bash
# Go to runpod.io
# Select: A100 80GB PCIe
# Template: PyTorch 2.1
# Cost: $1.89/hour
```

#### AWS Alternative
```bash
aws ec2 run-instances \
  --instance-type p4d.24xlarge \
  --image-id ami-0c55b159cbfafe1f0 \
  --key-name your-key
```

### 2. Install Dependencies

```bash
# Clone repository
git clone https://github.com/your-org/cerberus-ai.git
cd cerberus-ai/backend

# Run setup script
chmod +x scripts/setup_gpu.sh
./scripts/setup_gpu.sh
```

Or manually:
```bash
pip install -r requirements-gpu.txt
```

### 3. Verify GPU

```bash
python -c "
import torch
print(f'CUDA: {torch.cuda.is_available()}')
print(f'GPU: {torch.cuda.get_device_name(0)}')
print(f'Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB')
"
```

Expected output:
```
CUDA: True
GPU: NVIDIA A100-PCIE-80GB
Memory: 80.00 GB
```

### 4. Download Model

```bash
python -c "
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = 'mistralai/Mistral-7B-Instruct-v0.2'
print('Downloading model...')

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map='auto',
    torch_dtype='auto'
)

print('✅ Model ready')
print(f'Parameters: {model.num_parameters() / 1e9:.2f}B')
"
```

### 5. Prepare Dataset

```bash
# Export curated data
python -m src.infrastructure.training.curator_cli export \
  --output data/curated/training_data.jsonl

# Prepare for training
python -m src.infrastructure.training.dataset_preparation \
  data/curated/training_data.jsonl
```

Output:
```
📥 Loading data from data/curated/training_data.jsonl
✅ Loaded 50000 examples
🔄 Formatting for training...
✂️ Splitting dataset...
📊 Train: 45000, Val: 5000
✅ Saved to data/prepared
```

---

## Dataset Requirements

### Minimum Viable
- **Examples**: 10,000
- **Quality Rate**: 60%+
- **Languages**: 3+ (Python, JavaScript, TypeScript)

### Production Ready
- **Examples**: 50,000
- **Quality Rate**: 70%+
- **Languages**: 5+ (Python, JS, TS, Java, Go)
- **Frameworks**: 10+ (FastAPI, React, Django, etc.)

### Format
```json
{
  "messages": [
    {"role": "system", "content": "You are Cerberus AI..."},
    {"role": "user", "content": "How to use FastAPI?"},
    {"role": "assistant", "content": "FastAPI is a modern..."}
  ],
  "metadata": {
    "language": "python",
    "framework": "fastapi",
    "complexity": 5
  }
}
```

---

## Cost Estimation

### Training (One-time)
```
GPU: A100 80GB @ $1.89/hour
Duration: 24 hours
Total: $45.36
```

### Storage
```
Model: 14GB (FP16)
Dataset: 100MB
Checkpoints: 50GB
Total: ~65GB @ $0.023/GB/month = $1.50/month
```

### Inference (Monthly)
```
GPU: RTX 4090 @ $0.34/hour
Uptime: 24/7
Total: $244.80/month
```

---

## Next Steps

After setup is complete:

1. ✅ GPU provisioned
2. ✅ Dependencies installed
3. ✅ Model downloaded
4. ✅ Dataset prepared
5. ⏭️ Configure LoRA (next task)
6. ⏭️ Run fine-tuning
7. ⏭️ Evaluate model
8. ⏭️ Deploy to production

---

## Troubleshooting

### Out of Memory
```python
# Use 4-bit quantization
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_4bit=True,
    device_map='auto'
)
```

### Slow Download
```bash
# Use HF mirror
export HF_ENDPOINT=https://hf-mirror.com
```

### CUDA Not Found
```bash
# Verify CUDA installation
nvcc --version
nvidia-smi

# Reinstall PyTorch
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

---

**Status**: Model Base Setup Ready ✅
**Next**: Fine-Tuning Configuration
