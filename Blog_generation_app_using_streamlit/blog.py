import streamlit as st
from langchain.llms import OpenAI
from langchain import PromptTemplate

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
    
token_lenght = st.sidebar.slider('select number of token', min_value=500, max_value=2000, value=750)
# Set temperature value (adjust as needed)
temperature_value = st.sidebar.slider('Select temperature:', min_value=0.1, max_value=1.0, value=0.5)

about_us_generated = None  # Initialize the variable outside the function
blog_outline_generated = None  # Initialize the variable outside the function
keywords_generated = None 
title_response = None


def generate_title_response(number_of_title, about_us, keywords):
    llm_title = OpenAI(model_name='text-davinci-003', openai_api_key=openai_api_key_title, temperature=temperature_value)
    # Prompt
    template_title = '''Generate {number_of_title} catchy suitable title for a blog for the folllwoing condition.
                        1. "About us" about company is {about_us}.
                        2. company is related with following keyword.{keywords}.
                        '''
    prompt_title = PromptTemplate(input_variables=['number_of_title', 'about_us', 'keywords'], template=template_title)
    prompt_query_title = prompt_title.format(number_of_title=number_of_title, about_us=about_us, keywords=keywords)
    # Run LLM model and print out response
    response_title = llm_title(prompt_query_title)
    return st.sidebar.info(response_title), about_us, keywords   # Return about_us along with the response

def generate_blog_outline( title, about_us):
    llm_blog = OpenAI(model_name='text-davinci-003', openai_api_key=openai_api_key_title, temperature=temperature_value)
    # Prompt
    template_blog = '''As an experienced engaging blog content writer, 
                        generate an concise outline for the blog which has following information.
                        1. Blog title is {title}. 
                        2. company profile is {about_us}'''
    prompt_blog = PromptTemplate(input_variables=['title', 'about_us'], template=template_blog)
    prompt_query_blog = prompt_blog.format(title=title, about_us=about_us)
    # Run LLM model and print out response
    response_blog = llm_blog(prompt_query_blog)
    return st.info(response_blog)

def generate_complete_blog(title, blog_outline, keywords):
    llm_blog = OpenAI(model_name='text-davinci-003', openai_api_key=openai_api_key_title, temperature=temperature_value)
    # Prompt
    template_blog = '''Generate a complete blog post which has following information 
                        1. Title of the blog : "{title}"
                        2. frequently used keyword: "{keywords}".
                        Now, you are required to expand the "{blog_outline}" based on the above information provided to you.
                        please give suitable heading to each section and it must ended smoothly with conclusion'''
    prompt_blog = PromptTemplate(input_variables=['about_us', 'blog_outline', 'keywords'], template=template_blog)
    prompt_query_blog = prompt_blog.format(title=title, blog_outline=blog_outline , keywords=keywords)
    # Run LLM model and print out response
    response_blog = llm_blog(prompt_query_blog, max_tokens=token_lenght)
    return st.info(response_blog)


# Form for generating the blog title
with st.sidebar.form('title_form'):
    selected_value = st.slider('Select a value:', min_value=1, max_value=20, value=10)
    about_us = st.text_area('Enter about us of company:', height=200)
    #about_us = st.text_input('Enter about us of company:', '')
    keywords = st.text_area('Enter keywords separated with comma:', height=100)
    #keywords = st.text_input('Enter keywords separated with comma:', '')
    
    
    submitted_title = st.form_submit_button('Generate Title')

    # if not openai_api_key_title.startswith('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'):
    #     st.sidebar.warning('Please enter your OpenAI API key for title generation!', icon='⚠')
    # else:
    #     st.sidebar.success('API key verified!', icon='✅')

    if submitted_title and openai_api_key_title.startswith('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'):
       title_response, about_us_generated, keywords_generated =  generate_title_response(selected_value, about_us, keywords)

# Second column for generating the complete blog based on the generated title
# st.sidebar.title('Generate Complete Blog')
# openai_api_key_blog = st.sidebar.text_input('OpenAI API Key', type='password')

# Form for generating the outline of blog based on the title and about us
with st.form('blog_outline_form'):
    #topic_text_blog = st.text_input('Enter keyword for the complete blog:', '')
    title_text_blog = st.text_input('Enter the generated blog title:', '')
    submitted_blog = st.form_submit_button('Generate outline of Blog')

    # if not openai_api_key_title.startswith('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'):
    #     st.sidebar.warning('Please enter your OpenAI API key for complete blog generation!', icon='⚠')
    # else:
    #     st.sidebar.success('API key verified!', icon='✅')

    if submitted_blog and openai_api_key_title.startswith('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'):
        #generate_complete_blog_response(topic_text_blog, title_text_blog)
        blog_outline_generated = generate_blog_outline(title_text_blog, about_us_generated)

        




# Form for generating the complete blog based on the title
with st.form('blog_form'):
    #topic_text_blog = st.text_input('Enter keyword for the complete blog:', '')
    #title_text_blog = st.text_input('Enter the generated blog title:', '')
    submitted_blog = st.form_submit_button('Generate Complete Blog')

    # if not openai_api_key_title.startswith('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'):
    #     st.sidebar.warning('Please enter your OpenAI API key for complete blog generation!', icon='⚠')
    # else:
    #     st.sidebar.success('API key verified!', icon='✅')

    if submitted_blog and openai_api_key_title.startswith('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'):
        #generate_complete_blog_response(topic_text_blog, title_text_blog)
        response_complete_blog = generate_complete_blog(title_text_blog, blog_outline_generated, keywords_generated)

        
# Clear button to reset outputs
clear_button = st.button('Clear All Outputs')
if clear_button:
    about_us_generated = None
    blog_outline_generated = None
    keywords_generated = None
    title_text_blog = None
    st.empty()
    st.experimental_rerun()
    
    