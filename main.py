import openai
import os
from youtube_transcript_api import YouTubeTranscriptApi
import re
import sys
from dotenv import load_dotenv

'''
@private
@param t: "Messy" transcript array of dictionaries
@return res: "Cleaned" transcript
'''
def _clean_transcript(t, outfile=False):
    res = ""

    for i in t:
        if type(i) is dict:
            for k,v in i.items():
                if k == "text":
                    res += v
    
    if True:
        with open("transcript.txt", "w") as file:
            file.write(res)

    return res
'''
@param string idt: If of the yt video to transcribe
@return string: transcript
'''
def get_transcript(idt):
    # Get the transcript from YouTube API
    yt_id = idt
    yt_res = YouTubeTranscriptApi.get_transcript(yt_id)
    ts = _clean_transcript(yt_res)
    return ts

'''
@param string link: yt link to truncate
@return string : youtube ID
'''
def _clean_yt_link(link):
    try:
        youtube_id = re.search(r"(?<=v=)[\w-]+", link)
        return youtube_id.group(0)
    except:
        print("Invalid link provided")
        return ""

'''
@param string: Youtube video link
@return string : response from OpenAI chat
'''
def transcribe(yt_link, arg_key = ""):
    print("Now transcribing " + str(yt_link))
    yt_id = _clean_yt_link(yt_link)
    ts = get_transcript(yt_id)

    # Ask GPT-3 to summarize  the transcript
    openai.api_key = os.getenv('OPENAI_API_KEY')
    content = "Can you summarize this? \n " + ts
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": content}])
    return completion.choices[0].message.content

'''
Example Link: https://www.youtube.com/watch?v=eIho2S0ZahI
'''
if __name__ == "__main__":
    args = sys.argv
    load_dotenv() #Load OpenAI API Key from .env
    yt_link = ""
    res = ""

    if len(args)>1:
        res = transcribe(args[1])
    else:
        yt_link = input("Please enter the link of the YouTube video: ")
        res = transcribe(yt_link)
    print(res)

