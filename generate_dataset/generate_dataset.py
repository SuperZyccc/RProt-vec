import os
import subprocess
import csv
from tqdm import tqdm
from itertools import combinations

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

def get_pdb_files(directory):
    pdb_files = [f for f in os.listdir(directory) if f.endswith('.pdb')]
    return pdb_files

def run_us_align(pdb1, pdb2):
    try:
        result = subprocess.run(['./USalign/USalign', pdb1, pdb2], capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running US-align for {pdb1} and {pdb2}: {e}")
        return None

def parse_tm_score(output):
    if output:
        for line in output.splitlines():
            if "TM-score=" in line:
                return float(line.split('=')[1].split()[0])
    return None

def save_results_to_csv(results, output_file):
    try:
        with open(output_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in results:
                writer.writerow(row)
        print(f"Results saved to {output_file}")
    except Exception as e:
        print(f"Error saving results to {output_file}: {e}")

def record_progress(pdb1, pdb2, progress_file):
    try:
        with open(progress_file, 'w') as file:
            file.write(f'{pdb1},{pdb2}\n')
        print(f"Progress recorded at {pdb1} and {pdb2}")
    except Exception as e:
        print(f"Error recording progress: {e}")

def read_progress(progress_file):
    if not os.path.exists(progress_file):
        return None, None
    try:
        with open(progress_file, 'r') as file:
            last_line = file.readline().strip()
            if last_line:
                pdb1, pdb2 = last_line.split(',')
                return pdb1, pdb2
    except Exception as e:
        print(f"Error reading progress: {e}")
    return None, None

def main(sequence_file, pdb_dir, output_dir, progress_file, write_interval=10000, max_records_per_file=10000000):
    sequences = parse_fasta_file(sequence_file)
    pdb_files = get_pdb_files(pdb_dir)
    total_pairs = len(pdb_files) * (len(pdb_files) - 1) // 2
    results = []
    current_record_count = 0
    current_file_index = 0

    # Read progress
    last_pdb1, last_pdb2 = read_progress(progress_file)
    print(last_pdb1, last_pdb2)
    start = False if last_pdb1 or last_pdb2 else True

    pbar = tqdm(total=total_pairs, desc="Calculating TM-scores")

    for i in range(len(pdb_files)):
        for j in range(i + 1, len(pdb_files)):
            pdb1 = pdb_files[i]
            pdb2 = pdb_files[j]

            # Skip until we reach the progress point
            if not start:
                if pdb1 == last_pdb1 and pdb2 == last_pdb2:
                    start = True
                continue

            try:
                output = run_us_align(os.path.join(pdb_dir, pdb1), os.path.join(pdb_dir, pdb2))
                if output is None:
                    continue

                tm_score = parse_tm_score(output)

                if tm_score is not None:
                    domain1 = os.path.splitext(pdb1)[0]
                    domain2 = os.path.splitext(pdb2)[0]
                    sequence1 = sequences.get(domain1, "")
                    sequence2 = sequences.get(domain2, "")
                    results.append((sequence1, sequence2, tm_score))
                    current_record_count += 1

                # Write results to CSV and record progress every write_interval pairs
                if len(results) >= write_interval:
                    output_file = os.path.join(output_dir, f'results_batch_{current_file_index}.csv')
                    save_results_to_csv(results, output_file)
                    results = []

                    # Check if current CSV file reaches max_records_per_file
                    if current_record_count >= max_records_per_file:
                        current_file_index += 1
                        current_record_count = 0

                    record_progress(pdb1, pdb2, progress_file)

            except Exception as e:
                print(f"Error processing {pdb1} and {pdb2}: {e}")

            pbar.update(1)

    # Save any remaining results
    if results:
        output_file = os.path.join(output_dir, f'results_batch_{current_file_index}.csv')
        save_results_to_csv(results, output_file)
        record_progress(pdb1, pdb2, progress_file)

    pbar.close()

sequence_file = 'filtered.fa'
pdb_dir = 'pdb_files'
output_dir = 'output'
progress_file = 'progress.txt'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

main(sequence_file, pdb_dir, output_dir, progress_file)
