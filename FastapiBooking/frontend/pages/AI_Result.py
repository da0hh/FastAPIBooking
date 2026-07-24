import streamlit as st
import requests
from dotenv import load_dotenv
import datetime
import os

API_ADDRESS = os.getenv("API_BACKEND_ADRESS", "http://backend:8100")
user_id = st.session_state.get("user_data", {}).get("user_id")

st.set_page_config(
    page_title="AI Suggestions",
    layout="wide"
)

st.title("🤖 AI recommendations")

if user_id is None:
    st.warning("Please log in account to book places")
    if st.button("Log in"):
        st.switch_page("pages/login.py")
    st.stop()

if "ai_answer" not in st.session_state:
    st.warning("No data received.")
    st.stop()


answer = st.session_state.ai_answer

left, center, right = st.columns([1,2,1])


to_home = st.button("⬅ Home")

if to_home:
    st.switch_page(
        "main.py"
    )

counter = 0
for place in answer["places"]:
    with st.container(border=True):
        st.subheader(
            place["name"]
        )
        st.write(
            f"⭐ {place['rating']}"
        )
        st.write(
            place["place_address_url"]
        )

        booked_for = st.date_input("Date book for:", datetime.date(2026, 7, 9), key=f"from_{counter}")

        category = place["category"]
        name = place["name"]
        url = place["place_address_url"]
        city = place["city"]

        if category in ["Landmark", "Museum", "Entertainment"]:
            excursion_button = st.button("Choose excursion", key=f"excursion_{counter}")

            if excursion_button:
                response = requests.post(
                    f"{API_ADDRESS}/book/make-book",
                    json={
                        "user_id": user_id,
                        "city": city,
                        "place_name": name,
                        "booked_for": booked_for.isoformat(),
                    }
                )

                if response.status_code == 200:
                    st.success(f"Excursion «{name}» is booked!")
                else:
                    st.error(f"Error of booking: {response.text}")

        elif category in ["Hotel", "Restaurant"]:
            book_button = st.button("Book", key=f"to_book_{counter}")

            if book_button:
                response = requests.post(
                    f"{API_ADDRESS}/book/make-book",
                    json={
                        "user_id": user_id,
                        "city": city,
                        "place_name": name,
                        "booked_for": booked_for.isoformat()                    }
                )

                if response.status_code == 200:
                    st.success(f"Booked")
                else:
                    st.error(f"Error of booking: {response.text}")
        elif category == "Cinema":
            book_ticket_button = st.button("Book ticket", key=f"book_ticket_{counter}")

            if book_ticket_button:
                response = requests.post(
                    f"{API_ADDRESS}/book/make-book",
                    json={
                        "user_id": user_id,
                        "city": city,
                        "place_name": name,
                        "booked_for": booked_for.isoformat()
                    }
                )

                if response.status_code == 200:
                    st.success(f"Ticket is booked")
                else:
                    st.error(f"Error of booking: {response.text}")

        else:
            choose_button = st.button("Choose", key=f"choose_{counter}")

            if choose_button:
                response = requests.post(
                    f"{API_ADDRESS}/book/make-book",
                    json={
                        "user_id": user_id,
                        "city": city,
                        "place_name": name,
                        "booked_for": booked_for.isoformat()
                    }
                )

                if response.status_code == 200:
                    st.success(f"Planned")
                else:
                    st.error(f"Error of booking: {response.text}")

    counter += 1
st.markdown(
    answer["answer"]
)
