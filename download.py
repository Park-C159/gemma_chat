import shutil
import kagglehub

download_path = "./models/gemma-2-2b-it"
cache_path = kagglehub.model_download("google/gemma-2/pyTorch/gemma-2-2b-it")

shutil.move(cache_path, download_path)
print("Path to model files:", download_path)
