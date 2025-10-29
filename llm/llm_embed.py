'''
Generate an embedding given a piece of text.
'''

import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import pynvml

import config


class TextEncoder:
    # 'sentence-transformers/all-MiniLM-L6-v2'
    # 'sentence-transformers/all-mpnet-base-v2'

    error_msg_list = ['ERROR: No README data found!']

    def __init__(self, model_str, cuda_idx) -> None:
        local_path = ("huggingface/hub/models--sentence-transformers--all-mpnet-base-v2/snapshots"
                      "/12e86a3c702fc3c50205a8db88f0ec7c0b6b94a0/")
        if cuda_idx >= 0:
            print(f"TextEncoder set to use cuda:{cuda_idx}")
            dev_str = f"cuda:{cuda_idx}"
        else:
            print("TextEncoder set to use cpu")
            dev_str = "cpu"
        try:
            self.model = SentenceTransformer(model_str, device=dev_str)
        except Exception as e:
            print(f"unable to load model, try local: {config.get_config('model_dir_path')}/{local_path}")
            print(e)
            self.model = SentenceTransformer(
                f"{config.get_config('model_dir_path')}/{local_path}",
                local_files_only=True, device=dev_str)

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=256,
            chunk_overlap=50,
            length_function=len
        )
        self.dimension = -1

    def encode(self, text):
        if text == "" or text in TextEncoder.error_msg_list:
            return [[0 for _ in range(self.get_dimension())]]
        # the text can be very long, may need to split here
        sentences = self.text_splitter.split_text(text)
        res = self.model.encode(sentences)

        return res.tolist()

    def get_dimension(self):
        if self.dimension == -1:
            res = self.model.encode("This is a test sentence.")
            self.dimension = len(res)
        return self.dimension

    def mean_pooling(self, list_of_embeddings):
        return np.mean(list_of_embeddings, axis=0).tolist()

    def first_pooling(self, list_of_embeddings):
        return list_of_embeddings[0]


class EmbedPolicy:
    def __init__(self):
        self.encoder = TextEncoder('sentence-transformers/all-mpnet-base-v2', self.select_most_free_gpu_nvml())
        print(f"Dimension of embeddings: {self.encoder.get_dimension()}")

    def select_most_free_gpu_nvml(self):
        try:
            pynvml.nvmlInit()
        except pynvml.NVMLError:
            print("NVML initialization failed. No GPU available.")
            return -1

        num_gpus = pynvml.nvmlDeviceGetCount()
        if num_gpus == 0:
            print("No GPUs available.")
            return -1

        gpu_memory = []
        for i in range(num_gpus):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            gpu_memory.append(mem_info.free)  # 剩余显存

        best_gpu = max(range(num_gpus), key=lambda x: gpu_memory[x])
        print(f"Selected GPU {best_gpu} with {gpu_memory[best_gpu] / 1024 ** 2:.2f} MB free memory.")

        pynvml.nvmlShutdown()
        return best_gpu

    def embed_text(self, text: str) -> list:
        try:
            return self.encoder.mean_pooling(self.encoder.encode(text))
        except Exception as e:
            print(f"embed_text error: {e}: {text}")
            return [0 for _ in range(self.encoder.get_dimension())]
