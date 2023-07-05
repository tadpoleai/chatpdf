import os
import sys
import requests

import streamlit as st
from pydantic import BaseModel


class Response(BaseModel):
    result: str
    error: str
    stdout: str


# get file dir and add it to sys.path
cwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(cwd)

st.set_page_config(
    page_title='Q&A Bot on PDFs',
    page_icon='⚡',
    layout='wide',
    initial_sidebar_state='auto',
)

st.sidebar.markdown('## OpenAI Token')
openai_token = st.sidebar.text_input(
    'Enter your OpenAI token:', value='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', type='password'
)

host = st.text_input(
    'Enter the lc-serve host to connect to',
    value='https://pdfqna-b1b9f43e7a.wolf.jina.ai',
)

urls = st.text_area(
    'Type your urls (separated by comma)',
    value='https://github.com/tadpoleai/SAPdocs/blob/main/SAPFICO01.pdf',
    placeholder='https://github.com/tadpoleai/SAPdocs/blob/main/SAPFICO01.pdf',
)

question = st.text_input(
    'Type your question',
    value='凭证编制过账的步骤是什么?',
    placeholder='凭证编制过账的步骤是什么?',
)

submit = st.button('Submit')


def play():
    if submit:
        if not openai_token:
            st.error('Please enter your OpenAI token')
            return

        if not host:
            st.error('Please enter the lc-serve host')
            return

        if not question:
            st.error('Please enter your question')
            return

        if not urls:
            st.error('Please enter your urls')
            return

        headers = {'Content-Type': 'application/json'}
        data = {
            'urls': urls.split(','),
            'question': question,
            'envs': {'OPENAI_API_KEY': openai_token},
        }
        with st.spinner(text="Asking chain..."):
            response = requests.post(host + '/ask', headers=headers, json=data)
            st.info('get response')
            
            try:
                st.info(response.text)
                
                #response = Response.model_validate(response.text)
                #response.result=response.text['result']
                #st.markdown(f'Answer: **{response.result.strip()}**')
                #with st.expander('Show stdout'):
                    #st.write(response.json())
            except Exception as e:
                st.error(e)
                return


if __name__ == '__main__':
    play()
