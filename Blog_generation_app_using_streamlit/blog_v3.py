import streamlit as st
from langchain.llms import OpenAI
from langchain import PromptTemplate
import subprocess
subprocess.call(['pip', 'install', '-r', 'requirements.txt'])




# Set Streamlit page configuration
st.set_page_config(page_title="🦜🔗 Blog Outline Generator App", layout="wide")


# Title and OpenAI API key input in the sidebar
st.title('🦜🔗 Blog Outline Generator App')

# First column for generating the blog title
st.sidebar.title('Generate Blog Title')
openai_api_key_title = st.sidebar.text_input('OpenAI API Key', type='password')

if not openai_api_key_title.startswith('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'):
    st.sidebar.warning('Please enter your OpenAI API key for title generation!', icon='⚠')
else:
    st.sidebar.success('API key verified!', icon='✅')
    
token_length = st.sidebar.slider('select number of token', min_value=500, max_value=2000, value=750)
# Set temperature value (adjust as needed)
temperature_value = st.sidebar.slider('Select temperature:', min_value=0.1, max_value=1.0, value=0.5)

# Initialize session state variables
if 'outputs' not in st.session_state:
    st.session_state.outputs = []
    
about_us_generated = None
blog_outline_generated = None
keywords_generated = None 
title_response = None
title_text_blog = None

# Container to store and display outputs
output_container = st.container()

def generate_title_response(number_of_title, about_us, keywords):
    llm_title = OpenAI(model_name='text-davinci-003', openai_api_key=openai_api_key_title, temperature=temperature_value)
    # Prompt
    template_title = '''Generate {number_of_title} catchy suitable title for a blog for the following condition.
                        1. "About us" about company is {about_us}.
                        2. company is related with following keyword.{keywords}.
                        '''
    prompt_title = PromptTemplate(input_variables=['number_of_title', 'about_us', 'keywords'], template=template_title)
    prompt_query_title = prompt_title.format(number_of_title=number_of_title, about_us=about_us, keywords=keywords)
    # Run LLM model and append response to outputs list
    response_title = llm_title(prompt_query_title)
    st.session_state.outputs.append(response_title)
    return st.sidebar.info(response_title), about_us, keywords   # Return about_us along with the response

def generate_blog_outline(title, about_us):
    llm_blog = OpenAI(model_name='text-davinci-003', openai_api_key=openai_api_key_title, temperature=temperature_value)
    # Prompt
    template_blog = '''As an experienced engaging blog content writer, 
                        generate a concise outline for the blog which has following information.
                        1. Blog title is {title}. 
                        2. company profile is {about_us}'''
    prompt_blog = PromptTemplate(input_variables=['title', 'about_us'], template=template_blog)
    prompt_query_blog = prompt_blog.format(title=title, about_us=about_us)
    # Run LLM model and append response to outputs list
    response_blog = llm_blog(prompt_query_blog)
    st.session_state.outputs.append(response_blog)
    return st.info(response_blog)

def generate_complete_blog(title, blog_outline, keywords):
    llm_blog = OpenAI(model_name='text-davinci-003', openai_api_key=openai_api_key_title, temperature=temperature_value)
    # Prompt
    template_blog = '''Generate a complete blog post which has following information 
                        1. Title of the blog : "{title}"
                        2. frequently used keyword: "{keywords}".
                        Now, you are required to expand the "{blog_outline}" based on the above information provided to you.
                        please give suitable heading to each section and it must end smoothly with a conclusion'''
    prompt_blog = PromptTemplate(input_variables=['about_us', 'blog_outline', 'keywords'], template=template_blog)
    prompt_query_blog = prompt_blog.format(title=title, blog_outline=blog_outline , keywords=keywords)
    # Run LLM model and append response to outputs list
    response_blog = llm_blog(prompt_query_blog, max_tokens=token_length)
    st.session_state.outputs.append(response_blog)
    return st.info(response_blog)

# Form for generating the blog title
with st.sidebar.form('title_form'):
    selected_value = st.slider('Select a value:', min_value=1, max_value=20, value=10)
    about_us = st.text_area('Enter about us of the company:', height=200)
    keywords = st.text_area('Enter keywords separated with commas:', height=100)
    
    submitted_title = st.form_submit_button('Generate Title')

    if submitted_title and openai_api_key_title.startswith('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'):
        title_response, about_us_generated, keywords_generated = generate_title_response(selected_value, about_us, keywords)

# Second column for generating the complete blog based on the generated title
with st.form('blog_form'):
    title_text_blog = st.text_input('Enter the generated blog title:', '')
    
    col1, col2, col3 = st.columns(3)

    submitted_outline = col1.form_submit_button('Outline of Blog')
    submitted_complete = col2.form_submit_button('Complete Blog')
    submitted_summary = col3.form_submit_button('Summary')

    if submitted_outline and openai_api_key_title.startswith('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'):
        blog_outline_generated = generate_blog_outline(title_text_blog, about_us_generated)

    if submitted_complete and openai_api_key_title.startswith('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'):
        response_complete_blog = generate_complete_blog(title_text_blog, blog_outline_generated, keywords_generated)

    # Container to store and display outputs
    output_container = st.container()
    if submitted_summary:
        with output_container:
            for output in st.session_state.outputs:
                st.info(output)

# Clear button to reset outputs
col1, col2, col3 = st.columns(3)
clear_button = col2.button('Clear All Outputs')
if clear_button:
    about_us_generated = None
    blog_outline_generated = None
    keywords_generated = None
    title_text_blog = None
    st.session_state.outputs = []  # Clear the stored outputs
    st.empty()
    st.experimental_rerun()
