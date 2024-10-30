from diffusers import DiffusionPipeline
import torch
from PIL import Image
import torch
from diffusers import DiffusionPipeline


class GenerateImage1:
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

    def generateImage(self, prompt, name_image):
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
        image.save(f"{name_image}.png")


class GenerateImage:
    def __init__(self):
        self.genImageModel = DiffusionPipeline.from_pretrained("emilianJR/CyberRealistic_V3", torch_dtype=torch.float16)
        self.genImageModel.to("cuda")

    def generate_image(self, prompt, name_image):
        neg_prompt = "(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, mutated hands and fingers:1.4), (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, mutation, mutated, ugly, disgusting, amputation"
        generator = torch.Generator(device="cuda").manual_seed(1460)
        out_lpw = self.genImageModel(
            prompt,
            negative_prompt=neg_prompt,
            width=640,
            height=1024,
            max_embeddings_multiples=3,
            num_inference_steps=70,
            generator=generator,
        ).images[0]

        out_lpw.save(f"images/{name_image}.png")
