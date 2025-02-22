# Rprot-vec

## Overview
Rprot-Vec is a deep learning approach for fast protein structure similarity calculation. This repository includes:
- Training and testing code for the Rprot-Vec model.
- Scripts to download and prepare PDB data from the CATH dataset.
- Instructions on how to generate the dataset used for training/testing.
  
---

## Code
- **Training Code**  
  The training code can be found in the [`Train`](./Train) folder.

- **Testing Code**  
  The testing code can be found in the [`Test`](./Test) folder.

---

## Additional Tools

### `download_pdb_cath`
This folder contains scripts that automatically batch-download the PDB structure files corresponding to the CATH dataset. Use these scripts if you need to obtain the raw data for further processing or for generating new datasets.

### `generate_dataset`
This folder contains scripts that make use of USAlign and PDB data to automatically generate a dataset compatible with the Rprot-Vec approach. You can adjust the parameters or input files to create custom datasets as needed.

---

## Dataset
Datasets are available at: [https://pan.baidu.com/s/1ArDnZNi2HvDtVKczZDLiRA](https://pan.baidu.com/s/1ArDnZNi2HvDtVKczZDLiRA)  
**Password:** `1y7y`

---

## Citation

If you find this repository useful for your research, please cite:

**Y. Zhang, W. Zhang.**  
*Rprot-Vec: A deep learning approach for fast protein structure similarity calculation.*  
bioRxiv: [10.1101/2025.01.25.634852](https://doi.org/10.1101/2025.01.25.634852)

---

Or in BibTeX format:
```bibtex
@article{Rprot-Vec,
  title   = {Rprot-Vec: A deep learning approach for fast protein structure similarity calculation},
  author  = {Yichuan Zhang and Wen Zhang},
  journal = {bioRxiv},
  year    = {2025},
  doi     = {10.1101/2025.01.25.634852},
}

