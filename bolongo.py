"""
Bolongo: A chatbot to help with common questions about growing trees in Old School RuneScape,
using natural language processing to provide accurate answers in a gnome-inspired tone.

Note: This Streamlit app was generated with AI assistance, but the rest of the project was written by hand unless otherwise specified
"""

import streamlit as st
import base64
from PIL import Image
from source.orchestrator import Bolongo

# Initialize
if 'bolongo' not in st.session_state:
    st.session_state.bolongo = Bolongo()

# Make icon square
def make_square_icon(image_path):
    img = Image.open(image_path)
    max_dim = max(img.size)
    square_img = Image.new('RGBA', (max_dim, max_dim), (0, 0, 0, 0))
    offset = ((max_dim - img.size[0]) // 2, (max_dim - img.size[1]) // 2)
    square_img.paste(img, offset)
    return square_img

# Set page config
page_icon = make_square_icon("assets/bolongo_chathead.png")
st.set_page_config(page_title="Bolongo", page_icon=page_icon)

# Encode background image
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# Encode font
def get_base64_font(font_path):
    try:
        with open(font_path, "rb") as font_file:
            return base64.b64encode(font_file.read()).decode()
    except:
        return None

# Custom CSS for background and styling
bg_image = get_base64_image("assets/grand_tree.png")
bg_style = f'background-image: url("data:image/png;base64,{bg_image}");'
runescape_bold_font = get_base64_font("assets/RuneScape-Bold-12.ttf")
runescape_plain_font = get_base64_font("assets/RuneScape-Plain-12.ttf")

st.markdown(f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
    @font-face {{
        font-family: 'RuneScape';
        src: url('data:font/truetype;charset=utf-8;base64,{runescape_plain_font}') format('truetype');
        font-weight: normal;
        font-style: normal;
    }}
    @font-face {{
        font-family: 'RuneScape';
        src: url('data:font/truetype;charset=utf-8;base64,{runescape_bold_font}') format('truetype');
        font-weight: bold;
        font-style: normal;
    }}
    .stApp {{
        {bg_style}
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* Dark overlay for background */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.75);
        z-index: 0;
        pointer-events: none;
    }}
    /* Bring content above overlay */
    .stApp > header,
    .stApp > div {{
        position: relative;
        z-index: 1;
    }}
    /* Apply RuneScape font globally */
    * {{
        font-family: 'RuneScape', monospace !important;
        color: #FFFF00 !important;
        font-weight: normal !important;
    }}
    /* Override yellow for text input container elements */
    .stTextInput *:not(input),
    [data-testid="stTextInput"] *:not(input) {{
        color: #666666 !important;
    }}
    /* Bold text uses RuneScape Bold */
    strong, b, .bold-text {{
        font-weight: bold !important;
    }}
    /* Only h1 (Bolongo title) should be bold */
    h1 {{
        font-weight: bold !important;
    }}
    /* h2 and h3 should be normal weight and white */
    h2, h3 {{
        font-weight: normal !important;
        color: white !important;
    }}
    /* White chat input box */
    .stTextInput > div > div > input {{
        background-color: white !important;
        color: #1a1a1a !important;
        font-weight: 500;
        caret-color: #1a1a1a !important;
    }}
    .stTextInput > div > div > input::placeholder {{
        color: #999999 !important;
    }}
    .stTextInput > div > div > input::selection {{
        background-color: #CCCCCC !important;
        color: #1a1a1a !important;
    }}
    /* Fix helper text to be dark and visible */
    .stTextInput small,
    .stTextInput [data-baseweb="helper-text"],
    .stTextInput div[data-baseweb="base-input"] small,
    [data-testid="stTextInput"] small,
    [data-testid="InputInstructions"],
    .stTextInput div[class*="InputInstructions"],
    div[data-baseweb="base-input"] + div,
    .stTextInput p,
    [data-testid="stTextInput"] p,
    [data-testid="stTextInput"] div[class*="caption"] {{
        color: #666666 !important;
    }}
    /* White answer box */
    .stAlert {{
        background-color: white !important;
        color: black !important;
        max-width: 800px;
        margin: 0 auto;
    }}
    /* Center the input area */
    .stTextInput {{
        max-width: 800px;
        margin: 0 auto;
    }}
    /* Left align topics section */
    .topics-section {{
        text-align: left !important;
    }}
    .topics-section p, .topics-section ul {{
        text-align: left !important;
    }}
    /* Make examples white */
    .topics-section ul, .topics-section li, .topics-section li strong {{
        color: white !important;
    }}
    /* Center footer */
    .footer-section {{
        text-align: center !important;
    }}
    .social-icon {{
        color: white !important;
        text-decoration: none !important;
        margin: 0 10px;
        font-size: 20px;
        transition: opacity 0.2s;
    }}
    .social-icon:hover {{
        opacity: 0.7;
        text-decoration: none !important;
    }}
    /* Font Awesome icons need their original font and white color */
    .fab, .fa-brands, .fa, .fas {{
        font-family: 'Font Awesome 6 Brands', 'Font Awesome 6 Free' !important;
        color: white !important;
    }}
    /* Make topics header bold and bigger */
    .topics-header {{
        font-weight: bold !important;
        font-size: 18px !important;
    }}
    /* Response box text should be black */
    .response-box, .response-box * {{
        color: #1a1a1a !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Bolongo")
    st.subheader("The best gardener in Gielinor")
with col2:
    st.image("assets/bolongo_standing.png", width=112)

# Example topics
st.markdown("""
<div class="topics-section">
<p class="topics-header" style="font-weight: bold; margin-bottom: 5px; text-align: left; color: #FFFF00;">Ask me anything about trees!</p>
<ul style="font-size: 16px; margin-top: 0; text-align: left; padding-left: 0; list-style-type: none;">
<li><strong>Patch locations</strong> — "Give me a list of all regular tree patches."</li>
<li><strong>Transportation methods</strong> — "How do I get to the Catherby patch?"</li>
<li><strong>Quest requirements</strong> — "What are the requirements for the Nemus Retreat patch?"</li>
<li><strong>Farming level requirements</strong> — "What Farming level do I need to plant Maple trees?"</li>
<li><strong>Tree recommendations</strong> — "Which trees should I grow at level 27?"</li>
<li><strong>Growth time</strong> — "How long do Willow trees take to grow?"</li>
<li><strong>Protection payments</strong> — "What do I give to the gardener to protect Yew trees?"</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Question
user_question = st.text_input(label="Question", 
                               placeholder="Enter your question here...",
                               label_visibility="collapsed")

# Answer
if user_question:
    with st.spinner("Hmm..."):
        answer = st.session_state.bolongo.ask(user_question)
    
    st.markdown('<p style="font-weight: bold !important; margin-bottom: 5px; color: black;"><strong>Bolongo:</strong></p>', unsafe_allow_html=True)
    # Create a white container for the answer
    st.markdown(f"""
    <div class="response-box" style="background-color: white; padding: 15px; border-radius: 8px; max-width: 800px; margin: 0 auto; white-space: pre-wrap; font-family: 'RuneScape', monospace;">{answer}</div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('''
<div class="footer-section" style="color: #FFFF00;">
    Created by <strong style="color: #FFFF00;">Charlie</strong>
    <br>
    <a href="https://github.com/chmcbs" target="_blank" class="social-icon" title="GitHub"><i class="fab fa-github"></i></a>
    <a href="https://x.com/chmcbx" target="_blank" class="social-icon" title="X" style="font-family: Arial, sans-serif; font-weight: bold; color: white;">𝕏</a>
</div>
''', unsafe_allow_html=True)