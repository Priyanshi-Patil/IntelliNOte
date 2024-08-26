import streamlit as st
import mysql.connector

# Create a MySQL database connection
cnx = mysql.connector.connect(
    user='your_username',
    password='your_password',
    host='your_host',
    database='your_database'
)
cursor = cnx.cursor()

# Define a login function
def login(username, password):
    query = "SELECT 1 FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    if cursor.fetchone():
        return True
    return False

# Create a Streamlit login page
st.title("Login Page")

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    if login(username, password):
        st.write("Login successful!")
    else:
        st.write("Invalid username or password.")