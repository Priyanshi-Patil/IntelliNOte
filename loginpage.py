import streamlit as st

# Create a title and a form to accept username and password
st.title("Login Form")

# Set the background color to olive using CSS
st.write("<style>body { background-color: #808000; }</style>", unsafe_allow_html=True)

with st.form("login_form"):
    st.write("Please enter your username and password:")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

# Display a message if the form is submitted
if submitted:
    st.write(f"Welcome, {username}!")