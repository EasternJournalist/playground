import torch
import clip
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

image = preprocess(Image.open("test_images/20230310144810.png")).unsqueeze(0).to(device)
text = clip.tokenize(["an illustration of a cute girl sitting on a chair", "a chair", "an real photo"]).to(device)

with torch.no_grad():
    image_features = model.encode_image(image)  # (n_images, 512)
    text_features = model.encode_text(text)     # (n_texts, 512)

    logits_per_image, logits_per_text = model(image, text)  # (n_images, n_texts)
    probs = logits_per_image.softmax(dim=-1).cpu().numpy()

print("Label probs:", probs)  # prints: [[0.9927937  0.00421068 0.00299572]]