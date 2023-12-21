from youtube_transcript_api import YouTubeTranscriptApi
import re
import difflib
import openai
import json
from secret__key import openai_key
openai.api_key = openai_key


def extract_video_id(video_url):
    
    video_id_match = re.search(r"(?:(?:youtu\.be\/|v\/|vi\/|u\/\w\/|embed\/|watch\?v=|&v=|\?v=)([^#\&\?]*))", video_url)
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
        #formatted_transcript = format_transcript( transcript)
        #chunks = split_transcript(formatted_transcript)
        # print(chunks[0][0])
        # print("printing chunks!!!!\n\n")
        # text = ""
        # for i, chunk in enumerate(chunks, start=1):
        #     text += f"\nChunk {i}:\n", chunk
        return transcript
    except Exception as e:
        return f"Error: {str(e)}"



def format_transcript(transcript):
    print("Something")
    formatted_transcript = ""
    timestamped_transcript = []
    for entry in transcript:
        formatted_transcript += entry["text"] + " "
        timestamped_transcript.append((entry["text"], entry["start"]))
    print(formatted_transcript,timestamped_transcript)

    return formatted_transcript, timestamped_transcript



def split_transcript(transcript, chunk_size=4000):
    chunks = [transcript[i:i + chunk_size] for i in range(0, len(transcript), chunk_size)]
    return chunks



def convert_seconds_to_youtube_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))



def search_transcript(transcript, keyword):
    matches = []
    for entry in transcript:
        text, timestamp = entry
        match_ratio = difflib.SequenceMatcher(None, keyword.lower(), text.lower()).ratio()
        if match_ratio > 0.7:  
            matches.append((text, convert_seconds_to_youtube_time(timestamp)))
    return matches



# def de_prompt(chunk):
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": f"give a detailed explaination of each topics in the data not more than 400 words\n{chunk}"},

#         ],
#     )

    
#     detailed_explanation = response.choices[0]['message']['content'].strip()

#     return detailed_explanation

def su_prompt(chunk):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"summarize the data not more than 80 words\n{chunk}"},
        ],
    )

    minimal_explanation = response.choices[0]['message']['content'].strip()

    return minimal_explanation


def generate_summary(chunks):
    summary={}
    main_summary = ""
    
    for i, chapter_content in enumerate(chunks, start=1):
        summary[f"Chapter_{i}"] = su_prompt(chapter_content)
        main_summary += summary[f'Chapter_{i}']
        
   
    result = {"summary":main_summary}

    return main_summary, summary

def make_quiz(data):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Create quiz along with options for about minimum of \n{max(len(data),5)} based on the core content of the {data} in the form of json.first key will be content of the quiz along with options and seconde key wll be answers without any other statements"},
        ],
    )

    quiz_content = response.choices[0]['message']['content'].strip()
    return quiz_content

def save_to_json(result, filename='output.json'):
    
    with open(filename, 'w') as json_file:
        json.dump(result, json_file, indent=2)

def main(url):
    video_url = url
    keyword_to_search = "Structured Query Language"
    # print(f"\nProcessing video: {video_url}")

    try:
        transcript_data = get_video_transcript(video_url)
        #print("inside try")
        if transcript_data:
            #print("das")
            formatted_transcript, timestamped_transcript = format_transcript(transcript_data)
            
            #print(formatted_transcript)
            chunks = split_transcript(formatted_transcript)
            print("printing chunks!!!!\n\n")
            # for i, chunk in enumerate(chunks, start=1):
                # print(f"\nChunk {i}:\n", chunk)
            # search_results = search_transcript(timestamped_transcript, keyword_to_search)
            
            
            # if search_results:
            #     print(f"\nSearch Results for '{keyword_to_search}':")
            #     for result in search_results:
            #         print(f"Text: {result[0]}, Timestamp: {result[1]}\n\n")
            # else:
                # print(f"\nNo results found for '{keyword_to_search}' in the transcript.\n\n")
            
            main_summary , results=generate_summary(chunks)
            # print(results)
            quiz = make_quiz(results)
            # print(quiz)
            # print(type(quiz))
            
            
            # save_to_json(results['summary'])    
            # return {'chunk':chunks[0][0], 'summary':results}
            data = ({'transcript':formatted_transcript, 'summary':main_summary, 'quiz':quiz, 'timestamped_transcript':timestamped_transcript})
            return data
        else:
            print("Transcript is not available for this video.")
    except Exception as e:
        print(f"Errorsfjoudho: {str(e)}")


def get_time_stamp(url, search):
    try:
        video_id = extract_video_id(url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatted_transcript, timestamped_transcript = format_transcript(transcript)
        Outputresult = search_transcript(transcript=timestamped_transcript, keyword=search)
        print(Outputresult)
        return({'status':True})
    except:
        return({'status':False})




if __name__ == "__main__":
    main()
