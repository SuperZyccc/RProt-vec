# Protein Similarity Training

This project provides a deep learning model (based on GRU, CNN, and self-attention) for predicting protein structural similarity. The model leverages a pre-trained T5 encoder for feature extraction from protein sequences, followed by multiple GRU layers, convolutional layers, and a self-attention mechanism to fuse the extracted features, ultimately generating embeddings for similarity assessment.

---

## Table of Contents

- [Environment Requirements](#environment-requirements)
- [Data Preparation](#data-preparation)
- [Model Description](#model-description)
- [Training Procedure](#training-procedure)
- [Hyperparameters](#hyperparameters)
- [Checkpoints and Logging](#checkpoints-and-logging)
  
---

## Environment Requirements
Before running this project, please ensure the following dependencies are installed:
- **Python 3.7+** (3.8 or higher recommended)
- [**PyTorch**](https://pytorch.org/) (version compatible with your CUDA setup, 1.10+ recommended)
- [**Transformers**](https://github.com/huggingface/transformers)
- [**pandas**](https://pandas.pydata.org/)
- [**numpy**](https://numpy.org/)
- [**tensorboard**](https://pypi.org/project/tensorboard/)

---
## Data Preparation

### CSV File

- By default, the script reads data from `../data/data.csv`.
- The CSV file should have three columns: `seq1`, `seq2`, and `similarity_score`.
- The script splits the dataset into 95% for training and 5% for validation.

### Pre-trained T5 Model Files

- The code uses a pre-trained ProtT5 (`../prot_t5_xl_uniref50`) for sequence feature extraction.
- Make sure the paths in `main.py`:
  ```python
  self.tokenizer = T5Tokenizer.from_pretrained("../prot_t5_xl_uniref50")
  self.t5model = T5EncoderModel.from_pretrained("../prot_t5_xl_uniref50")
  ```
---

## Model Description

### Architecture Overview

- **Feature Extraction with ProtT5**  
  Converts protein sequences into tokens and extracts hidden embeddings using a pre-trained T5 encoder.

- **GRU Layers**  
  Two layers of bidirectional GRUs to capture sequential dependencies.

- **Self-Attention (MultiheadAttention)**  
  Applies self-attention for global context learning among the hidden states.

- **Convolutional Layers (Conv1D)**  
  Uses multiple convolution kernels (size=3, 7) to extract local features. Combines outputs with residual connections.

- **Pooling & MLP**  
  Applies adaptive average pooling, followed by an MLP to map the pooled features into the final embedding space.

- **Cosine Similarity & L1 Loss**  
  During training, a cosine similarity is computed between the embeddings of two sequences, and an L1 loss is used to align it with the ground-truth similarity score (e.g., TM-score).

---

## Training Procedure

### Load Dataset
- Reads the CSV file (`../data/data.csv`), then splits it into training (95%) and validation (5%) sets.

### Model and Optimizer Setup
- Instantiates the `GRU_CNN_Block` model and moves it to the GPU if available.
- Uses the `Adam` optimizer with an initial learning rate of `1e-4`.
- Employs `ReduceLROnPlateau` to monitor validation loss and reduce the learning rate if no improvement is observed.

### Training & Validation

#### Training
- Forward pass to compute loss, then backpropagate to update weights.
- Records each iteration’s loss in TensorBoard.

#### Validation
- Evaluates the model on the validation set, computing the loss to track generalization.

### Checkpointing
- After each epoch, if the validation loss is lower than all previous epochs, the model is saved to `checkpoints/`.
- After all epochs, a final model is saved to `final_model.pth`.

---

## Hyperparameters

Key hyperparameters and their default values (can be adjusted in `main.py`):

- **Batch size**: 64  
- **Learning rate**: 0.0001  
- **GRU hidden size**: 256  
- **Num layers (GRU)**: 1  
- **Dropout**: 0.1  
- **Epochs**: 2 (you can change this in `main()`)  
- **Train / Validation split**: 95% / 5%

---

## Checkpoints and Logging

### Checkpoints
- During training, checkpoints are saved in the `checkpoints/` directory with filenames like `model_epoch_{E}_loss_{val_loss}.pth`.
- A limited number of checkpoints is retained (`num_checkpoints=1` by default), deleting older ones.

### TensorBoard Logs
- Training and validation losses are logged in `../../tf-logs/Training` by default (configurable in `main.py`).
- To visualize in TensorBoard:
  ```bash
  tensorboard --logdir=../../tf-logs/Training
  ```
- Then access http://localhost:6006 in your browser to see real-time curves.

---






