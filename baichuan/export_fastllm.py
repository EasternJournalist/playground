import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
from fastllm_pytools import torch2flm

MODEL_PATH = "baichuan-inc/Baichuan2-7B-Chat"
DTYPE = "int4"

if __name__ == "__main__":
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, device_map="auto", torch_dtype=torch.float16, trust_remote_code=True)
    model.to("cpu")
    try:
        model.generation_config = GenerationConfig.from_pretrained(MODEL_PATH)
    except:
        pass
    dtype = sys.argv[2] if len(sys.argv) >= 3 else "int4"
    exportPath = sys.argv[1] if len(sys.argv) >= 2 else f"baichuan2-7b-{DTYPE}.flm"
    torch2flm.tofile(exportPath, model, tokenizer, dtype=DTYPE)
