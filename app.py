import openai
import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

# Set up OpenAI API key
openai.api_key = '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'

# Function to generate blog content using OpenAI
def generate_blog(prompt):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Function to post the blog to WordPress
def post_to_wordpress(title, content, wp_user, wp_password, wp_site):
    url = f"{wp_site}/wp-json/wp/v2/posts"
    data = {
        "title": title,
        "content": content,
        "status": "publish"  # Change to 'draft' if you want to review the post before publishing
    }
    auth = HTTPBasicAuth(wp_user, wp_password)
    response = requests.post(url, json=data, auth=auth)

    if response.status_code == 201:
        return "Post published successfully!"
    else:
        return f"Failed to publish post: {response.content}"

# Streamlit interface
st.title("Automated Blog Generator and WordPress Poster")

# User inputs for blog generation
st.header("Step 1: Generate a Blog")
prompt = st.text_area("Enter a prompt for the blog", "Write a blog about the latest trends in AI")

# Button to generate blog content
if st.button("Generate Blog"):
    blog_content = generate_blog(prompt)
    st.success("Blog content generated successfully!")
    st.text_area("Generated Blog Content", blog_content, height=300)

    # User inputs for WordPress credentials
    st.header("Step 2: Publish to WordPress")
    wp_site = st.text_input("Enter your WordPress site URL (e.g., https://your-site.com)")
    wp_user = st.text_input("WordPress Username")
    wp_password = st.text_input("WordPress Application Password", type="password")
    blog_title = st.text_input("Enter a title for the blog post", "Latest AI Trends")

    # Button to post blog to WordPress
    if st.button("Publish to WordPress"):
        if wp_site and wp_user and wp_password and blog_title:
            result = post_to_wordpress(blog_title, blog_content, wp_user, wp_password, wp_site)
            st.success(result)
        else:
            st.error("Please provide all the required details to post to WordPress.")
