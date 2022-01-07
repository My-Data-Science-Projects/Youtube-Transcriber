import streamlit as st
from pytube import YouTube
import os
import requests
from api import api_key


# Custom functions

# 2. Retrieving audio file from YouTube video
def get_yt(URL):
    video = YouTube(URL)
    yt = video.streams.get_audio_only()
    yt.download()

    st.warning('Transcription is processing ...')

    # st.info('2. Audio file has been retrieved from YouTube video')
    bar.progress(10)


# 3. Upload YouTube audio file to AssemblyAI
def transcribe_yt():
    global mp4_file
    current_dir = os.getcwd()

    for file in os.listdir(current_dir):
        if file.endswith(".mp4"):
            mp4_file = os.path.join(current_dir, file)
            # print(mp4_file)

    filename = mp4_file
    bar.progress(20)

    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    headers = {'authorization': api_key}
    response = requests.post('https://api.assemblyai.com/v2/upload',
                             headers=headers,
                             data=read_file(filename))
    audio_url = response.json()['upload_url']
    # st.info('3. YouTube audio file has been uploaded to AssemblyAI')
    bar.progress(30)

    # 4. Transcribe uploaded audio file
    endpoint = "https://api.assemblyai.com/v2/transcript"

    json = {
        "audio_url": audio_url
    }

    headers = {
        "authorization": api_key,
        "content-type": "application/json"
    }

    transcript_input_response = requests.post(endpoint, json=json, headers=headers)

    # st.info('4. Transcribing uploaded file')
    bar.progress(40)

    # 5. Extract transcript ID
    transcript_id = transcript_input_response.json()["id"]
    # st.info('5. Extract transcript ID')
    bar.progress(50)

    # 6. Retrieve transcription results
    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {
        "authorization": api_key,
    }
    transcript_output_response = requests.get(endpoint, headers=headers)
    # st.info('6. Retrieve transcription results')
    bar.progress(60)

    # Check if transcription is complete
    from time import sleep

    while transcript_output_response.json()['status'] != 'completed':
        sleep(5)
        transcript_output_response = requests.get(endpoint, headers=headers)

    bar.progress(100)

    # 7. Print transcribed text
    st.header('Result :')
    final = transcript_output_response.json()["text"]
    st.markdown(final)

    # 8. Save transcribed text to file

    if st.download_button(label="Download Data", data=final, file_name='transcript.txt', mime='text/plain'):
        st.markdown(f'<h3 style="color:#28a745; font-size:18px;">'
                    f'Thank You for Downloading !</h3>', unsafe_allow_html=True)


#####

# The App

# 1. Read API from .py file
st.markdown('# 📝 **Transcriber App**')
bar = st.progress(0)

with st.form(key='my_form'):
    URL = st.text_input('Enter URL of YouTube Video:')
    submit_button = st.form_submit_button(label='Submit')

# Run custom functions if URL is entered
if submit_button:
    get_yt(URL)
    transcribe_yt()
