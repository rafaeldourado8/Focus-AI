"""Dataset Preparation for Fine-Tuning"""
import json
from pathlib import Path
from typing import List, Dict
from datasets import Dataset


class DatasetPreparator:
    """Prepares training data for HuggingFace fine-tuning"""
    
    def __init__(self, input_file: str, output_dir: str = "data/prepared"):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def load_jsonl(self) -> List[Dict]:
        """Load JSONL training data"""
        examples = []
        with open(self.input_file, "r", encoding="utf-8") as f:
            for line in f:
                examples.append(json.loads(line))
        return examples
    
    def format_for_training(self, examples: List[Dict]) -> List[Dict]:
        """Format examples for instruction fine-tuning"""
        formatted = []
        for ex in examples:
            messages = ex["messages"]
            
            # Convert to text format for training
            text = ""
            for msg in messages:
                role = msg["role"]
                content = msg["content"]
                
                if role == "system":
                    text += f"<|system|>\n{content}\n"
                elif role == "user":
                    text += f"<|user|>\n{content}\n"
                elif role == "assistant":
                    text += f"<|assistant|>\n{content}\n"
            
            formatted.append({
                "text": text,
                "metadata": ex.get("metadata", {})
            })
        
        return formatted
    
    def split_dataset(self, examples: List[Dict], train_ratio: float = 0.9):
        """Split into train and validation sets"""
        split_idx = int(len(examples) * train_ratio)
        return examples[:split_idx], examples[split_idx:]
    
    def prepare(self, train_ratio: float = 0.9):
        """Prepare complete dataset"""
        print(f"📥 Loading data from {self.input_file}")
        examples = self.load_jsonl()
        print(f"✅ Loaded {len(examples)} examples")
        
        print("🔄 Formatting for training...")
        formatted = self.format_for_training(examples)
        
        print("✂️ Splitting dataset...")
        train_data, val_data = self.split_dataset(formatted, train_ratio)
        print(f"📊 Train: {len(train_data)}, Val: {len(val_data)}")
        
        # Save as HuggingFace datasets
        train_dataset = Dataset.from_list(train_data)
        val_dataset = Dataset.from_list(val_data)
        
        train_path = self.output_dir / "train"
        val_path = self.output_dir / "val"
        
        train_dataset.save_to_disk(str(train_path))
        val_dataset.save_to_disk(str(val_path))
        
        print(f"✅ Saved to {self.output_dir}")
        
        return {
            "train_path": str(train_path),
            "val_path": str(val_path),
            "train_size": len(train_data),
            "val_size": len(val_data)
        }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python dataset_preparation.py <input_jsonl>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    preparator = DatasetPreparator(input_file)
    result = preparator.prepare()
    
    print("\n📋 Dataset Summary:")
    print(f"  Train: {result['train_size']} examples")
    print(f"  Val: {result['val_size']} examples")
    print(f"  Train path: {result['train_path']}")
    print(f"  Val path: {result['val_path']}")
