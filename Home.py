import streamlit as st
from hashing import generate_hash, is_valid_hash
from app_model.db import conn
from app_model.users import add_user, get_user
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

st.title("Welcome to main page🏠")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.button("Log In", key="main_login_button"):
    st.session_state['logged_in'] = True

tab_login, tab_register = st.tabs(["Login Status", "Register"])

with tab_login:
    login_username = st.text_input("Username", key="login_username_input")
    login_password = st.text_input("Password", type="password", key="login_password_input")
    if st.button("Log in", key="login_button"):
        st.session_state['logged_in'] = True

with tab_register:
    register_username = st.text_input("New username")
    register_password = st.text_input("New Password", type="password")
    hash_password = generate_hash(register_password)
    if st.button("Register", key="register_button"):
        st.session_state['logged_in'] = False
        add_user(conn, register_username, hash_password) 
        st.success("Registration successful! You can now log in.")

st.session_state
