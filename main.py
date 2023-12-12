import requests
import certifi
from bs4 import BeautifulSoup
import youtube_dl
import os
from pathlib import Path

def scrape_video_url(sign):
	url = f"https://www.signasl.org/sign/{sign}"
	
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
		response = requests.get(url, headers=headers, verify=certifi.where())
		response.raise_for_status()

		soup = BeautifulSoup(response.text, 'html.parser')
		# print(soup)
		# Finding the first video tag and then the nested source tag
		video_tag = soup.find('video')
		if not video_tag:
				print(f"No video tag found for {sign}")
				return None

		source_tag = video_tag.find('source')
		if not source_tag or not source_tag.get('src'):
			print(f"No source tag found for {sign}")
			return None

		video_url = source_tag['src']
		return video_url

	except Exception as e:
		print(f"Error scraping video URL for {sign}: {e}")
		return None

def download_video(video_url, download_folder, sign):
    ydl_opts = {
        'outtmpl': os.path.join(download_folder, f'{sign}.%(ext)s'),
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([video_url])
            print(f"Downloaded video for {sign}")
        except Exception as e:
            print(f"Error downloading video for {sign}: {e}")


def main(signs, download_folder):
	for sign in signs:
		video_url = scrape_video_url(sign)
		if video_url:
			download_video(video_url, download_folder, sign)
			
if __name__ == "__main__":
	prompt_message = "Enter the signs you want videos of, separated by commas:\n\n"\
                     "e.g. today, eat, sleep, never\n> "
	input_string = input(prompt_message)
	signs = [sign.strip() for sign in input_string.split(',')]


	script_dir = Path(__file__).parent
	download_folder = script_dir / 'videos'
	os.makedirs(download_folder, exist_ok=True)

	main(signs, download_folder)
	

## note... when there are multiple videos, let's just download all of them. if there is one it will be labeled _0, and then we increment from there
