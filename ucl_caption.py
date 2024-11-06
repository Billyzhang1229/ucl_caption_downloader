import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

# Step 1: Define a list of URLs
urls = [
    'https://echo360.org.uk/lesson/G_e26b2bdc..........',  # Add the URL of the Echo360 lesson here
]

# Define the cookie header
cookie = "ECHO_JWT=eyJ0eXAiOiJKV1QiLCJhbGciOi.........."

# Set single_line to True to save captions as a single line, False to save with separate lines
single_line = False  # Set this to False to keep captions on separate lines

for url in urls:
    # Fetch the HTML content for each URL
    response = requests.get(url, headers={'Cookie': cookie})
    soup = BeautifulSoup(response.content, 'html.parser')
    scripts = soup.find_all('script')

    vtt_link = ''
    title = ''
    date_str = ''
    for script in scripts:
        if script.string and 'Echo["classroomApp"]' in script.string:
            # Extract the JSON string within Echo["classroomApp"](...)
            match = re.search(r'Echo\["classroomApp"\]\("({.*?})"\);', script.string, re.DOTALL)
            if match:
                json_str = match.group(1)
                json_str = bytes(json_str, 'utf-8').decode('unicode_escape')
                data = json.loads(json_str)
                
                # Get the VTT link, title, and timing
                vtt_link = data.get('captions', {}).get('file', '')
                lesson_info = data.get('lesson', {})
                title = lesson_info.get('name', 'Untitled')
                timing = lesson_info.get('timing', {})
                start_date = timing.get('start', '')
                if start_date:
                    date_obj = datetime.strptime(start_date.split('T')[0], '%Y-%m-%d')
                    date_str = date_obj.strftime('%a %b %d')
                break

    if vtt_link:
        filename = f"{title} - {date_str}.vtt"
        vtt_response = requests.get(vtt_link, headers={'Cookie': cookie})
        vtt_content = vtt_response.content.decode('utf-8')

        # Remove timestamps and speaker labels
        caption_lines = []
        pattern = re.compile(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\s*\n(.*?)(?=\n\n|\Z)', re.DOTALL)
        matches = pattern.findall(vtt_content)
        for match in matches:
            text = re.sub(r'<v\s+[^>]+>', '', match)
            caption_lines.append(text.strip())

        # Join all captions into a single line or keep separate lines based on the single_line setting
        if single_line:
            cleaned_content = ' '.join(caption_lines)
        else:
            cleaned_content = '\n'.join(caption_lines)
        
        # Save the cleaned content to the file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        print(f'Downloaded {filename} as {'a single line' if single_line else 'separate lines'}')
    else:
        print(f'No .vtt file link found for URL: {url}')
