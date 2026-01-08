#!/bin/bash
# GPU Setup Script for Cerberus AI Fine-Tuning
# Target: A100 80GB (RunPod, AWS, or GCP)

set -e

echo "🚀 Cerberus AI - GPU Training Environment Setup"

# System info
echo "📊 System Information:"
nvidia-smi
python --version

# Install PyTorch with CUDA
echo "📦 Installing PyTorch with CUDA 11.8..."
pip install torch==2.1.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install HuggingFace ecosystem
echo "📦 Installing HuggingFace Transformers..."
pip install transformers==4.36.0
pip install datasets==2.16.0
pip install accelerate==0.25.0
pip install peft==0.7.1
pip install bitsandbytes==0.41.3
pip install trl==0.7.4

# Install evaluation metrics
echo "📦 Installing evaluation tools..."
pip install evaluate==0.4.1
pip install rouge-score==0.1.2
pip install sacrebleu==2.3.1

# Install monitoring
echo "📦 Installing monitoring tools..."
pip install wandb==0.16.1
pip install tensorboard==2.15.1

# Download Mistral 7B
echo "📥 Downloading Mistral 7B Instruct v0.2..."
python -c "
from transformers import AutoTokenizer, AutoModelForCausalLM
model_name = 'mistralai/Mistral-7B-Instruct-v0.2'
print(f'Downloading {model_name}...')
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map='auto')
print('✅ Model downloaded successfully')
"

# Verify GPU
echo "✅ Verifying GPU setup..."
python -c "
import torch
print(f'CUDA Available: {torch.cuda.is_available()}')
print(f'CUDA Version: {torch.version.cuda}')
print(f'GPU Count: {torch.cuda.device_count()}')
if torch.cuda.is_available():
    print(f'GPU Name: {torch.cuda.get_device_name(0)}')
    print(f'GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB')
"

echo "✅ Setup complete! Ready for fine-tuning."
