# 4x upscale with Real-ESRGAN (x4plus). Writes <name>-hd.jpg next to the source. Run by the upscale workflow.
import sys, numpy as np, torch, spandrel
from PIL import Image
src, weights = sys.argv[1], sys.argv[2]
model = spandrel.ModelLoader().load_from_file(weights).eval()
img = np.asarray(Image.open(src).convert("RGB")).astype(np.float32) / 255.0
t = torch.from_numpy(img).permute(2, 0, 1)[None]
with torch.no_grad():
    out = model(t)[0].clamp(0, 1).permute(1, 2, 0).numpy()
Image.fromarray((out * 255).round().astype(np.uint8)).save(src.rsplit(".", 1)[0] + "-hd.jpg", quality=90, optimize=True, progressive=True)
