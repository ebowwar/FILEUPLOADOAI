
import os
import openai
import httpx
from sys import argv
import traceback
from tqdm import tqdm
import io

class ProgressUploadFile(io.IOBase):
    def __init__(self, filename):
        self.file = open(filename, 'rb')
        self.size = os.path.getsize(filename)
        self.progress_bar = tqdm(total=self.size, unit='iB', unit_scale=True)

    def read(self, size=-1):
        data = self.file.read(size)
        self.progress_bar.update(len(data))
        return data

    def close(self):
        self.progress_bar.close()
        self.file.close()

def upload_file_to_openai(file_path):
    try:
        # Retrieve API key from environment variable for security
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("API key not found. Set the OPENAI_API_KEY environment variable.")

        # Initialize the OpenAI client with the API key
        client = openai.OpenAI(api_key=api_key)

        # Upload the file with streaming and progress bar
        with ProgressUploadFile(file_path) as file_to_upload:
            response = client.files.create(
                file=file_to_upload,
                purpose="fine-tune"
            )
        return response
    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()

if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: python upload_openai.py <file_path>")
    else:
        file_path = argv[1]
        result = upload_file_to_openai(file_path)
        if result:
            print("File uploaded successfully. Response:", result)
