import requests
import os
from tqdm import tqdm

def parse_fasta_file(file_path):
    sequences = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):
            header = lines[i].strip()
            sequence = lines[i + 1].strip()
            domain_id = header.split('|')[-1].split('/')[0]
            sequences[domain_id] = sequence
    return sequences


def filter_sequences(sequences, max_length=100):
    return {k: v for k, v in sequences.items() if len(v) <= max_length}


def download_pdb_files(sequences, output_dir, timeout=10):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_url = "http://www.cathdb.info/version/v4_3_0/api/rest/id/"
    failed_downloads = []

    with tqdm(total=len(sequences), desc="Downloading PDB files") as pbar:
        for domain_id in sequences.keys():
            url = f"{base_url}{domain_id}.pdb"
            try:
                response = requests.get(url, timeout=timeout)
                response.raise_for_status()  # Check if the request was successful
                with open(os.path.join(output_dir, f"{domain_id}.pdb"), 'wb') as file:
                    file.write(response.content)
            except (requests.exceptions.RequestException, requests.exceptions.Timeout):
                print(f"Failed to download {domain_id}")
                failed_downloads.append(domain_id)

            # 每下载一个文件，更新进度条
            pbar.update(1)

    return failed_downloads


def save_filtered_sequences(sequences, output_file):
    with open(output_file, 'w') as file:
        for domain_id, sequence in sequences.items():
            file.write(f">cath|4_3_0|{domain_id}\n")
            file.write(f"{sequence}\n")


def save_failed_downloads(failed_downloads, failed_file):
    with open(failed_file, 'w') as file:
        for domain_id in failed_downloads:
            file.write(f"{domain_id}\n")


def main(input_file, output_file, pdb_output_dir, failed_file):
    sequences = parse_fasta_file(input_file)
    filtered_sequences = filter_sequences(sequences)
    save_filtered_sequences(filtered_sequences, output_file)
    failed_downloads = download_pdb_files(filtered_sequences, pdb_output_dir)
    save_failed_downloads(failed_downloads, failed_file)


# 输入输出路径
input_file = 'cath-domain-seqs.fa'
output_file = 'filtered.fa'
pdb_output_dir = 'pdb_files'
failed_file = 'failed_downloads.txt'

main(input_file, output_file, pdb_output_dir, failed_file)


