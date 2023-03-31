from diffusers import StableDiffusionPipeline
import torch

model_path = "./sd-pokemon-model-lora"
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16)
pipe.safety_checker = lambda images, clip_input: (images, False)
pipe.unet.load_attn_procs(model_path)
pipe.to("cuda")

prompt = "a yello pokemon; 3D model; low poly; stylized; cartoon; 3D;"
image = pipe(prompt, num_inference_steps=30, guidance_scale=7.5).images[0]
image.save("pokemon.png")