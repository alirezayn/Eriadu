import requests

header = {
    "Authorization": "Bearer sk-7c5371ca2a70048898931c4c448017ad"
}

data = {
 'text': 'جاوا اسکریپت یک زبان چند منظوره هست',
    'server': 'farsi',
    'sound': '3'
}

response = requests.post('https://api.talkbot.ir/v1/media/text-to-speech/REQ', data=data, headers=header)

if response.status_code == 200:
    response_json = response.json()
    download_url = response_json["response"]["download"]

    # ارسال درخواست GET برای دانلود فایل صوتی
    audio_response = requests.get(download_url)

    if audio_response.status_code == 200:
        # ذخیره فایل صوتی با نام مورد نظر
        with open("js_crossplatform.mp3", "wb") as audio_file:
            audio_file.write(audio_response.content)
        print("File downloaded and saved as js_crossplatform.mp3")
    else:
        print(f"Failed to download audio file: {audio_response.status_code}")
else:
    print(f"Error: {response.status_code} - {response.text}")
