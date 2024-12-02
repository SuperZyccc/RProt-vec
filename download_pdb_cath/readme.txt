How to use:
1. Replace cath-domain-seqs.fa with the fasta data of the sequence you want to download.
2. Open main.py, you can replace max_length with the longest sequence requirement you want to filter, change the input/output path, and run it.

input_file = 'cath-domain-seqs.fa'
output_file = 'filtered.fa'
pdb_output_dir = 'pdb_files'
failed_file = 'failed_downloads.txt'

The output file will generate a new fasta file based on your filtering requirements, and the corresponding protein 3D structure file will be downloaded to the pdb_output_dir folder
Due to network fluctuations, some of the protein names that failed to download will be recorded in the failed file. If you need to re download these files that failed to download, simply run 'fail pdbdownload.py'

