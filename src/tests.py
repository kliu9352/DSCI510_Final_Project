import json
from load import get_youtube_transcript, get_ted_transcript

def run_api_test():
    video_id = "iG9CE55wbtY"    # Video: "Sir Ken Robinson: Do schools kill creativity?"

    print(f"Testing YouTube Transcript API for video ID: {video_id}")

    transcript_list = get_youtube_transcript(video_id)

    if transcript_list:
        print(f"\n[TEST SUCCESS] Retrieved {len(transcript_list)} transcript snippets.")

        print("\nSample Transcript Snippets:")
        for i, snippet in enumerate(transcript_list[:3]):
            print(json.dumps(snippet, indent=2))

    else:
        print("\n[TEST FAILURE] Could not retrieve transcript snippets.")

def run_scraping_test():
    url = "https://www.ted.com/talks/juulia_jylhava_the_3_best_predictors_of_how_well_you_ll_age"

    print(f"Testing TED Talk Transcript Scraping for URL: {url}")

    transcript_text = get_ted_transcript(url)

    if transcript_text:
        print(f"\n[TEST SUCCESS] Retrieved {len(transcript_text)} characters of transcript.")

        print("\nSample Transcript Text:")
        print(transcript_text[:200] + "...")
    else:
        print("\n[TEST FAILURE] Could not retrieve transcript text.")

if __name__ == "__main__":
    run_api_test()
    print("\n" + "="*50 + "\n")
    run_scraping_test()