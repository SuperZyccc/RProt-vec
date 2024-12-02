import requests
import os
from tqdm import tqdm

def read_failed_downloads(failed_file):
    """
    读取失败下载的域 ID 列表
    :param failed_file: 失败下载文件路径
    :return: 失败下载的域 ID 列表
    """
    with open(failed_file, 'r') as file:
        failed_downloads = file.read().splitlines()
    return failed_downloads


def retry_failed_downloads(failed_downloads, output_dir, timeout=10):
    """
    重新尝试下载失败的 PDB 文件
    :param failed_downloads: 失败下载的域 ID 列表
    :param output_dir: 输出目录
    :param timeout: 请求超时时间
    :return: 仍然失败的域 ID 列表
    """
    base_url = "http://www.cathdb.info/version/v4_3_0/api/rest/id/"
    still_failed_downloads = []

    # 使用 tqdm 创建进度条
    with tqdm(total=len(failed_downloads), desc="Retrying failed downloads") as pbar:
        for domain_id in failed_downloads:
            url = f"{base_url}{domain_id}.pdb"
            try:
                response = requests.get(url, timeout=timeout)
                response.raise_for_status()  # Check if the request was successful
                with open(os.path.join(output_dir, f"{domain_id}.pdb"), 'wb') as file:
                    file.write(response.content)
            except (requests.exceptions.RequestException, requests.exceptions.Timeout):
                print(f"Failed to download {domain_id} again")
                still_failed_downloads.append(domain_id)

            # 每下载一个文件，更新进度条
            pbar.update(1)

    return still_failed_downloads


def save_failed_downloads(failed_downloads, failed_file):
    """
    保存失败下载的域 ID 列表
    :param failed_downloads: 失败下载的域 ID 列表
    :param failed_file: 失败下载文件路径
    """
    with open(failed_file, 'w') as file:
        for domain_id in failed_downloads:
            file.write(f"{domain_id}\n")


# 主函数
def main_retry(failed_file, pdb_output_dir):
    failed_downloads = read_failed_downloads(failed_file)
    still_failed_downloads = retry_failed_downloads(failed_downloads, pdb_output_dir)
    if still_failed_downloads:
        print(f"Failed to download the following files after retrying: {still_failed_downloads}")
        save_failed_downloads(still_failed_downloads, failed_file)
    else:
        print("All files downloaded successfully on retry.")


# 输入路径和输出目录
failed_file = 'failed_downloads.txt'
pdb_output_dir = 'pdb_files'

# 运行主函数
main_retry(failed_file, pdb_output_dir)
