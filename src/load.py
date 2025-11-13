import pandas as pd
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
import json

def load_nrc_lexicon(filepath):
    try:
        df = pd.read_csv(
            filepath,
            sep='\t',
            header=None,
            names=['word', 'emotion', 'association']
        )
        nrc_df = df[df['association'] == 1].pivot(
            index='word',
            columns='emotion',
            values='association'
        ).fillna(0)
        print("NRC Lexicon loaded successfully.")
        return nrc_df
    except FileNotFoundError:
        print(f"Error: NRC lexicon file not found at {filepath}.")
        return None

def get_ted_transcript(ted_talk_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(ted_talk_url, headers=headers)

        if response.status_code != 200:
            print(f"Error: fetching TED Talk: HTTP {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')

        script_tag = soup.find('script', {'type': 'application/ld+json'})

        if not script_tag:
            print("Could not find transcript script tag.")
            return None
        
        json_data = json.loads(script_tag.string)

        transcript = json_data.get('transcript')

        if transcript:
            transcript_cleaned = transcript.replace('\n', ' ').replace('\r', ' ')
            print(f"TED Talk transcript scraped successfully from {ted_talk_url}.")
            return transcript_cleaned
        else:
            print("Found JSON-LD, but 'transcript' key was not found.")
            return None
    
    except Exception as e:
        print(f"Error scraping TED Talk transcript: {e}")
        return None
    
def get_youtube_transcript(youtube_video_id):
    try:
        ytt_api = YouTubeTranscriptApi()
        
        transcript_object = ytt_api.fetch(youtube_video_id)
        
        transcript_list = []
        for snippet in transcript_object.snippets:
            transcript_list.append({
                'text': snippet.text,
                'start': snippet.start,
                'duration': snippet.duration
            })            

        print(f"YouTube transcript retrieved successfully for video ID {youtube_video_id}.")
        return transcript_list
    
    except Exception as e:
        print(f"Error getting YouTube transcript: {e}")
        return None