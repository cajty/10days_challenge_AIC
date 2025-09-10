
# SmolLM Fine-Tuning Notebook

This README explains how to use the notebook which demonstrates fine-tuning the SmolLM2-135M-Instruct model using Supervised Fine-Tuning (SFT) with the TRL library on a reasoning dataset.

## Overview

This notebook fine-tunes the **SmolLM2-135M-Instruct** model (135M parameters) on the **Deepthink-Reasoning** dataset to improve its reasoning capabilities. The model is a small, efficient language model optimized for instruction-following tasks.

## What the notebook does

1. **Installs dependencies**: Sets up required libraries (transformers, datasets, trl, torch, accelerate, bitsandbytes, wandb)
2. **Loads the base model**: Downloads SmolLM2-135M-Instruct from Hugging Face
3. **Sets up chat format**: Configures the model for chat-based interactions
4. **Loads training data**: Uses the "prithivMLmods/Deepthink-Reasoning" dataset
5. **Fine-tunes the model**: Performs supervised fine-tuning with optimized training parameters
6. **Saves the model**: Exports the fine-tuned model and tokenizer

## Requirements

- **Python 3.8+**
- **CUDA-compatible GPU** (recommended: Tesla T4 or better)
- **Internet connection** for downloading models and datasets
- **Sufficient disk space** (~2-3GB for model and training artifacts)

## Hardware Requirements

- **GPU Memory**: Minimum 8GB VRAM (Tesla T4 with 15GB recommended)
- **System RAM**: 16GB+ recommended
- **Storage**: 5GB+ free space

## Installation

The notebook automatically installs required packages:

```bash
pip install transformers datasets trl torch accelerate bitsandbytes wandb
```

## Usage Instructions

### 1. Environment Setup
Run the first cell to install dependencies:
```python
!pip install transformers datasets trl torch accelerate bitsandbytes wandb
```

### 2. Import Libraries and Check Resources
```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, pipeline
from datasets import load_dataset
from trl import SFTConfig, SFTTrainer, setup_chat_format
import torch
import os
```

### 3. Load and Test Base Model
The notebook loads the SmolLM2-135M-Instruct model and tests it with a sample prompt:
```python
model_name = "HuggingFaceTB/SmolLM2-135M-Instruct"
model = AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path=model_name)
tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=model_name)
```

### 4. Prepare Training Data
The notebook uses the Deepthink-Reasoning dataset and applies chat formatting:
```python
ds = load_dataset("prithivMLmods/Deepthink-Reasoning")
```

### 5. Configure Training Parameters
Key training settings:
- **Batch size**: 2 per device
- **Gradient accumulation**: 4 steps
- **Learning rate**: 5e-5
- **Max steps**: 70
- **Optimizer**: AdamW 8-bit
- **Precision**: BF16 (if supported) or FP16

### 6. Start Training
```python
trainer.train()
```

### 7. Save and Download Model
The fine-tuned model is saved locally and packaged for download.

## Training Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| Model | SmolLM2-135M-Instruct | Base model (135M parameters) |
| Dataset | Deepthink-Reasoning | Reasoning-focused training data |
| Batch Size | 2 | Per-device training batch size |
| Gradient Accumulation | 4 | Effective batch size = 8 |
| Learning Rate | 5e-5 | Optimized for small models |
| Max Steps | 70 | Quick fine-tuning for demonstration |
| Precision | BF16/FP16 | Memory optimization |
| Optimizer | AdamW 8-bit | Memory-efficient optimization |

## Dataset Information

- **Name**: prithivMLmods/Deepthink-Reasoning
- **Type**: Instruction-response pairs for reasoning tasks
- **Format**: Chat-formatted prompts and responses
- **Purpose**: Improves model's reasoning and problem-solving capabilities

## Model Information

- **Base Model**: HuggingFaceTB/SmolLM2-135M-Instruct
- **Parameters**: 135 million
- **Architecture**: Transformer-based causal language model
- **Specialization**: Instruction-following and reasoning
- **Size**: ~500MB (base model)

## Expected Training Time

- **Tesla T4**: ~10-15 minutes for 70 steps
- **V100**: ~5-8 minutes for 70 steps
- **A100**: ~3-5 minutes for 70 steps

*Times may vary based on dataset size and system configuration.*

## Output and Results

After training, you'll get:
1. **Fine-tuned model** in `/content/my_model/`
2. **Model weights** and configuration files
3. **Tokenizer** files
4. **Zipped archive** for easy download

## Customization Options

### Modify Training Parameters
```python
training_args = TrainingArguments(
    per_device_train_batch_size=4,  # Increase for more VRAM
    max_steps=200,                  # More training steps
    learning_rate=3e-5,            # Adjust learning rate
    warmup_steps=10,               # More warmup steps
)
```

### Use Different Dataset
```python
ds = load_dataset("your-dataset-name")
```

### Change Model
```python
model_name = "microsoft/DialoGPT-medium"  # Different base model
```

## Troubleshooting

### Common Issues

1. **CUDA Out of Memory**
   - Reduce `per_device_train_batch_size` to 1
   - Increase `gradient_accumulation_steps`
   - Use `fp16=True` instead of `bf16`

2. **Slow Training**
   - Ensure GPU is being used (`device=0`)
   - Check GPU utilization with `nvidia-smi`
   - Consider using a more powerful GPU

3. **Model Not Loading**
   - Check internet connection
   - Verify Hugging Face model name
   - Ensure sufficient disk space

4. **Training Crashes**
   - Reduce batch size
   - Check system memory
   - Verify dataset format

### Performance Optimization

- **Use BF16** if your GPU supports it (better than FP16)
- **Enable 8-bit optimization** for memory efficiency
- **Adjust batch size** based on available VRAM
- **Use gradient checkpointing** for very large models

## Monitoring Training

The notebook includes basic logging. For advanced monitoring:

```python
training_args = TrainingArguments(
    # ... other args ...
    report_to="wandb",  # Enable Weights & Biases
    logging_steps=1,
    save_steps=10,
)
```

## Model Evaluation

After training, test your model:

```python
# Load your fine-tuned model
model = AutoModelForCausalLM.from_pretrained("/content/my_model")
tokenizer = AutoTokenizer.from_pretrained("/content/my_model")

# Test with a prompt
prompt = "Solve this step by step: What is 15% of 200?"
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
print(pipe(prompt, max_new_tokens=150))
```

## Next Steps

1. **Evaluate performance** on reasoning tasks
2. **Compare** with base model responses
3. **Fine-tune further** with domain-specific data
4. **Deploy** the model for inference
5. **Share** on Hugging Face Hub

## References

- [SmolLM2 Model Card](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct)
- [TRL Library Documentation](https://huggingface.co/docs/trl/)
- [Transformers Documentation](https://huggingface.co/docs/transformers/)
- [Deepthink-Reasoning Dataset](https://huggingface.co/datasets/prithivMLmods/Deepthink-Reasoning)

