import streamlit as st
from time import sleep

import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_ADDRESS = os.getenv("API_BACKEND_ADRESS", "http://backend:8100")

st.set_page_config(
    page_title="Login",
    layout="centered"
)

st.title("Booking Page")

user_id = st.session_state.get("user_data", {}).get("user_id")
col_back, col_edit, col_logout, col_del = st.columns([1, 1, 1, 1])

if "place_name" in st.session_state:
    chosen_place = st.session_state["place_name"]

    left, center, right = st.columns([1, 2, 1])

    with center:
        response = requests.get(f"{API_ADDRESS}/places/get-place/{chosen_place}")

        if response.status_code == 200:
            booking_place = response.json()

            place_name_str = booking_place["name"]
            place_city_str = booking_place["city"]
            place_rating_str = booking_place["rating"]

            st.write(f'### {place_name_str}')
            st.write(f'📍 City: {place_city_str}')
            st.write(f'⭐ Rate: {place_rating_str}')

            with st.form("book_form"):
                date = st.date_input("Choose date")

                submit = st.form_submit_button("Confirm booking")

                if submit:
                    if user_id is None:
                        st.warning("Please log in account to book places")
                        st.switch_page("pages/login.py")
                    else:
                        response_book = requests.post(
                            f"{API_ADDRESS}/book/make-book",
                            json={
                                "user_id": user_id,
                                "city": place_city_str,
                                "place_name": place_name_str,
                                "booked_for": date.isoformat()
                            }
                        )
                        if response_book.status_code == 200:
                            st.success(f"Successfully booked {place_name_str}!")
                            sleep(2)
                            st.switch_page("main.py")
                        else:
                            st.error(f"Booking failed: {response_book.text}")
        else:
            st.error(f"Failed to load place. Status code: {response.status_code}")
    with col_back:
        if st.button("⬅ Home"):
            st.switch_page("main.py")
else:
    st.warning("No place selected.")
    if st.button("Go to Home"):
        st.switch_page("main.py")