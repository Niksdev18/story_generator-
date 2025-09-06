import openai
import json

def generate_story_segments(prompt, genre, tone, audience, api_key):
    openai.api_key = api_key
    try:
        outline_prompt = f"""
        Create a structured plot outline for the story prompt below.

        Story Prompt: "{prompt}"

        Genre: {genre}
        Tone: {tone}
        Audience: {audience}

        Return 5 plot points in JSON format as: {{"segments": ["...", "...", ...]}}
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": outline_prompt}],
            max_tokens=500
        )
        outline_text = response.choices[0].message['content']
        outline_json = json.loads(outline_text)
        segments_outline = outline_json.get("segments", [])

        story_segments = []
        previous_text = ""
        for idx, segment in enumerate(segments_outline):
            detail_prompt = f"""
            Continue the story based on the previous part while keeping characters and plot consistent.

            Previous text: "{previous_text}"

            Plot point: "{segment}"

            Write a detailed narrative for this part.
            """
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": detail_prompt}],
                max_tokens=300
            )
            text = response.choices[0].message['content']
            story_segments.append(text)
            previous_text = text

        return story_segments

    except openai.error.OpenAIError as e:
        print("OpenAI API Error:", e)
        return ["Error generating story."]
    except json.JSONDecodeError as e:
        print("JSON Parsing Error:", e)
        return ["Error parsing story outline."]
    except Exception as e:
        print("Unexpected Error:", e)
        return ["An unexpected error occurred."]
