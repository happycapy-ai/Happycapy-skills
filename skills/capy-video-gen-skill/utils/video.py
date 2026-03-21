import logging
import requests
from tenacity import retry


@retry
def download_video(url, save_path):
    try:
        logging.info(f"Downloading video from {url} to {save_path}")

        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功
    
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        logging.info(f"Video downloaded successfully to {save_path}")
    
    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        raise e
