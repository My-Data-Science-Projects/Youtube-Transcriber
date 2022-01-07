import pandas as pd
import streamlit as st
from streamlit_player import st_player
from pytube import extract
from youtube_transcript_api import YouTubeTranscriptApi as yta

def main():
    st.title('Transcribe YouTube Videos')

    form = st.form(key="my_form", clear_on_submit=True)
    link = form.text_input(label="Enter YouTube Link")

    df = pd.read_csv("lang.csv")
    lst = list(df.English)

    option = form.selectbox('Select Language', lst)
    lang = df.loc[df['English'] == option, 'alpha2'].iloc[0]

    submit_button = form.form_submit_button(label="Submit")

    try:
        if submit_button and link != '':
            st_player(link)

            vid_id = extract.video_id(link)

            # transcript_list = yta.list_transcripts(vid_id)

            data = yta.get_transcript(vid_id, languages=[lang])

            transcript = ''

            for value in data:
                for key, val in value.items():
                    if key == 'text':
                        transcript += " " + val.replace('\n', '')
                        transcript = transcript.lstrip()

            # lines = transcript.splitlines()
            # final = " ".join(lines)

            st.subheader('Transcription Result : ')

            st.markdown(transcript)

            if st.download_button(label="Download Data", data=transcript, file_name='transcript.txt', mime='text/plain'):
                st.markdown(f'<h3 style="color:#28a745; font-size:18px;">'
                            f'Thank You for Downloading !</h3>', unsafe_allow_html=True)
    except:
        st.error("Transcription Not Available in This Video")
        st.stop()


if __name__ == "__main__":
    main()
