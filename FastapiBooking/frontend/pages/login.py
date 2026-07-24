import streamlit as st

from dotenv import load_dotenv
import os

import requests

load_dotenv()

API_ADDRESS = os.getenv("API_BACKEND_ADRESS", "http://backend:8100")

st.set_page_config(
    page_title="Login",
    layout="centered"
)

st.title("🔐 Login or Sign up")

login_tab, signup_tab = st.tabs(["Log in", "Sign up"])

with login_tab:
    with st.form("login_form"):
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        submit_login = st.form_submit_button("Log in")

    if submit_login:
        if not username or not password:
            st.error("Please fill in both fields.")
        else:
            response = requests.post(
                f"{API_ADDRESS}/login/enter-in-acc",
                json={
                    "username": username,
                    "password": password,
                }
            )

            if response.status_code == 200:
                st.session_state.user_data = response.json()
                st.success("Logged in successfully!")
                st.switch_page("main.py")
            elif response.status_code == 403:
                st.error("Invalid username or password.")
            elif response.status_code == 404:
                st.error("User with this username does not exist.")
            else:
                st.error(response.text)

with signup_tab:
    with st.form("signup_form"):
        new_username = st.text_input("Username", key="signup_username")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm password", type="password", key="signup_confirm")
        submit_signup = st.form_submit_button("Sign up")

    if submit_signup:
        if not new_username or not new_password:
            st.error("Please fill in both fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            response = requests.post(
                f"{API_ADDRESS}/login/sign-up",
                json={
                    "username": new_username,
                    "password": new_password,
                }
            )

            if response.status_code == 200:
                st.session_state.user_data = response.json()
                st.success("Account created successfully!")
                st.switch_page("main.py")
            elif response.status_code == 409:
                st.error("User with this username already exists.")
            else:
                st.error(response.text)

st.divider()

if st.button("⬅ Home"):
    st.switch_page("main.py")