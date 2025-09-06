import openai

STYLE_GUIDES = {
    "Realistic": "A highly detailed, realistic depiction with sharp textures.",
    "Cartoon": "A colorful, cartoonish style with bold outlines.",
    "Watercolor": "A soft watercolor painting with flowing brush strokes.",
    "Anime": "A Japanese anime style with expressive characters and vibrant backgrounds."
}

NEGATIVE_PROMPT = "blurry, low quality, extra limbs, deformed"

def create_story_images(segments, art_style, api_key):
    openai.api_key = api_key
    images = []
    style_description = STYLE_GUIDES.get(art_style, "")

    try:
        for segment in segments:
            prompt = f"{style_description} {segment}"
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512",
                response_format="b64_json"
            )
            image_data = response['data'][0]['b64_json']
            images.append(f"data:image/png;base64,{image_data}")

        return images
    except openai.error.OpenAIError as e:
        print("OpenAI API Error:", e)
        return ["Error generating image."]
    except Exception as e:
        print("Unexpected Error:", e)
        return ["An unexpected error occurred."]
