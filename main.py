from flask import jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re
import openai
import json
from secret__key import openai_key
from sentence_transformers import SentenceTransformer, util

openai.api_key = openai_key


def extract_video_id(video_url):
    video_id_match = re.search(
        r"(?:(?:youtu\.be\/|v\/|vi\/|u\/\w\/|embed\/|watch\?v=|&v=|\?v=)([^#\&\?]*))",
        video_url,
    )
    if video_id_match:
        return video_id_match.group(1)
    else:
        video_id_match = re.search(r"youtu\.be/([^#\&\?]+)", video_url)
        if video_id_match:
            return video_id_match.group(1)
        else:
            raise ValueError("Invalid YouTube video URL")


def get_video_transcript(video_url):
    video_id = extract_video_id(video_url)

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        return f"Error: {str(e)}"


def format_transcript(transcript):
    formatted_transcript = ""
    timestamped_transcript = []
    for entry in transcript:
        formatted_transcript += entry["text"] + " "
        timestamped_transcript.append((entry["text"].lower(), entry["start"]))
    # print(formatted_transcript,timestamped_transcript)

    return formatted_transcript, timestamped_transcript


def split_transcript(transcript, chunk_size=4000):
    chunks = [
        transcript[i : i + chunk_size] for i in range(0, len(transcript), chunk_size)
    ]
    return chunks


def convert_seconds_to_youtube_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))


def search_transcript(transcript, keyword):
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

    # Encode the keyword to get its vector representation
    keyword_embedding = model.encode(keyword, convert_to_tensor=True)

    matches = []
    for entry in transcript:
        text, timestamp = entry
        text_embedding = model.encode(text, convert_to_tensor=True)

        # Calculate cosine similarity between the keyword and the text
        similarity = util.pytorch_cos_sim(keyword_embedding, text_embedding).item()

        # Adjust the threshold based on your preference
        if similarity > 0.7:
            matches.append((text, convert_seconds_to_youtube_time(timestamp)))
    return matches


def su_prompt(chunk):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"summarize the data not more than 80 words\n{chunk}",
            },
        ],
    )
    minimal_explanation = response.choices[0]["message"]["content"].strip()
    return minimal_explanation


import time


def generate_summary(chunks):
    summary = {}
    main_summary = ""
    for i, chapter_content in enumerate(chunks, start=1):
        summary[f"Chapter_{i}"] = su_prompt(chapter_content)
        main_summary += summary[f"Chapter_{i}"]
        time.sleep(20)
    result = {"summary": main_summary}

    return main_summary, summary


def make_quiz(data):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"Create quiz along with options for about minimum of \n{max(len(data),5)} based on the core content of the {data} in the form of json.Follow this format correctly quiz1:question,options:multiple options,answer:answer inside a parent quiz json format without any other statements.",
            },
        ],
    )
    quiz_content = response.choices[0]["message"]["content"].strip()
    return quiz_content


def save_to_json(result, filename="output.json"):
    with open(filename, "w") as json_file:
        json.dump(result, json_file, indent=2)


def main(url):
    video_url = url
    keyword_to_search = "Structured Query Language"

    try:
        transcript_data = get_video_transcript(video_url)
        if transcript_data:
            formatted_transcript, timestamped_transcript = format_transcript(
                transcript_data
            )
            chunks = split_transcript(formatted_transcript)
            main_summary, results = generate_summary(chunks)
            quiz = make_quiz(results)
            data = {
                "transcript": formatted_transcript,
                "summary": main_summary,
                "quiz": json.loads(quiz),
            }
            return data
        else:
            return "Transcript is not available for this video."
    except Exception as e:
        return f"Errors: {str(e)}"


from new import search_transcript_semantic


def get_time_stamp(url, search):
    try:
        video_id = extract_video_id(url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatted_transcript, timestamped_transcript = format_transcript(transcript)
        Outputresult = search_transcript_semantic(
            transcript=timestamped_transcript, keyword=search
        )
        return Outputresult
    except:
        return "Nothing to respond"


if __name__ == "__main__":
    main()
