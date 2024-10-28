from diffusers import DiffusionPipeline
import torch
from PIL import Image


class GenerateImage:
    def __init__(self):
        self.genImageModel = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
        )
        self.genImageModel.to("cuda")
        # base.unet = torch.compile(base.unet, mode="reduce-overhead", fullgraph=True)
        self.refiner = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-refiner-1.0",
            text_encoder_2=self.genImageModel.text_encoder_2,
            vae=self.genImageModel.vae,

            torch_dtype=torch.float16,
            use_safetensors=True,
            variant="fp16",
        )
        self.refiner.to("cuda")
        self.n_steps = 30
        self.high_noise_frac = 0.8


    def generateImage(self, prompt, nameImage):
        image = self.genImageModel(
            prompt=prompt,
            num_inference_steps=self.n_steps,
            denoising_end=self.high_noise_frac,
            output_type="latent",
        ).images
        image = self.refiner(
            prompt=prompt,
            num_inference_steps=self.n_steps,
            denoising_start=self.high_noise_frac,
            image=image,
        ).images[0]
        image.save(f"{nameImage}.png")

a=GenerateImage()
a.generateImage("luffy with husky,full body,on a beach,8k,no hand","haha")
import torch
from diffusers import DiffusionPipeline

pipe_sd = DiffusionPipeline.from_pretrained("emilianJR/CyberRealistic_V3", torch_dtype=torch.float16)
pipe_sd.to("cuda")
# load long prompt weighting pipeline
# pipe_lpw = DiffusionPipeline.from_pipe(
#     pipe_sd,
#     custom_pipeline="lpw_stable_diffusion",
# ).to("cuda")

prompt = "cat, hiding in the leaves, ((rain)), zazie rainyday, beautiful eyes, macro shot, colorful details, natural lighting, amazing composition, subsurface scattering, amazing textures, filmic, soft light, ultra-detailed eyes, intricate details, detailed texture, light source contrast, dramatic shadows, cinematic light, depth of field, film grain, noise, dark background, hyperrealistic dslr film still, dim volumetric cinematic lighting"
neg_prompt = "(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, mutated hands and fingers:1.4), (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, mutation, mutated, ugly, disgusting, amputation"
generator = torch.Generator(device="cpu").manual_seed(220)
out_lpw = pipe_sd(
    prompt,
    negative_prompt=neg_prompt,
    width=512,
    height=512,
    max_embeddings_multiples=3,
    num_inference_steps=80,
    generator=generator,
    ).images[0]



out_lpw.save("01223wcybfer_realadasdistic_lpw_cat_hiding_in_leaves.png")
