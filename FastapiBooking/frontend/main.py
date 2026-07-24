import streamlit as st
from dotenv import load_dotenv

import os
from datetime import datetime

import requests

load_dotenv()

API_ADDRESS = os.getenv("API_BACKEND_ADRESS", "http://backend:8100")
user_id = st.session_state.get("user_data", {}).get("user_id")
user_name = st.session_state.get("user_data", {}).get("username")

st.set_page_config(
    page_title="Traveller Guide",
    layout="wide"
)

def format_date(raw: str) -> str:
    if not raw or raw == "—":
        return "—"
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y %H:%M")
    except (ValueError, TypeError):
        return raw

left, center, right = st.columns([1, 2, 1])

with right:
    profile = st.button("👤", key="user_button_1")

if profile:
    if "user_data" in st.session_state:
        st.switch_page("pages/user_info.py")
    else:
        st.switch_page("pages/login.py")



with center:
    to_book, users_rests, comments = st.tabs(["To book a place", "My rests", "Commentaries"])

    with to_book:

        with st.container(border=True):
            with st.container(border=False):
                st.markdown("Popular places:")

                response = requests.get(f"{API_ADDRESS}/places/popular3places")
                if response.status_code != 200:
                    st.error(f"Error in backend: {response.status_code}")
                    st.stop()

                try:
                    popular_places = response.json()
                except Exception as e:
                    st.error("Backend sent invalid data format (not JSON).")
                    st.code(response.text)
                    st.stop()

                popular_places_counter = 0
                for popular_place in popular_places:

                    if popular_places_counter >= 3:
                        break

                    with st.container(border=True):
                        col_text, col_btn = st.columns([0.85, 0.15])

                        with col_text:
                            st.write(f"{popular_place['name']}")
                            st.write(f"{popular_place['city']}")
                            st.write(f"{popular_place['place_address_url']}")

                        with col_btn:
                            if st.button("Book", key=f"popular_places_counter{popular_places_counter}"):
                                st.session_state["place_name"] = popular_place['name']
                                st.switch_page("pages/book_place.py")

                        popular_places_counter += 1

        with st.container(border=True):
            city = st.selectbox("City:", ["Moscow", "Saint Petersburg", "Smolensk", "Rostov"])
            prefs = st.text_area("Preferences:")
            send = st.button("Show Examples")


            if send and prefs:
                if user_id is None:
                   st.warning("Please, log in your account, to get recommendations")

                else:
                    st.write("Loading answer")
                    response = requests.post(
                        f"{API_ADDRESS}/book/ai",
                        json={
                            "user_id": user_id,
                            "city": city,
                            "prefers": prefs,
                        }
                    )
                    if response.status_code == 200:
                        st.session_state.ai_answer = response.json()

                        st.switch_page("pages/AI_Result.py")
                    else:
                        st.error(response.text)

    #with reviews:
        # return reviews of users
        # TODO
        # print Rating on 5 point scale
        #with st.container(border=True):
            #st.write("Rating:")
            #st.metric(label="Average rating", ")

    with comments:
        with st.container(border=True):
            body = st.text_input("Write commentary:")
            rate = st.selectbox("Relative", ["Positive", "Negative"])
            post_comment = st.button("Post")

            if post_comment:
                if user_id is None:
                    st.warning("Please, log in your account, to get recommendations")

                else:
                    response = requests.post(
                        f"{API_ADDRESS}/comments/create-comment",
                        json={
                            "user_id": user_id,
                            "name": user_name,
                            "body": body,
                            "rate": rate
                        }
                    )


        fetched_comments = (requests.get(f"{API_ADDRESS}/comments/list-comments")).json()

        if not fetched_comments:
            st.write("Be the first.\nThere are no comments yet")
        else:
            counter_comment = 0
            for comment in fetched_comments:
                with st.container(border=True):
                    col_top_name, col_top_del = st.columns([4, 1])

                    with col_top_name:
                        st.markdown(f"**{comment['name']}**")

                    with col_top_del:
                        if user_id == comment["user_id"]:
                            delete = st.button(f":red[Delete]", key=f"delete_{counter_comment}")
                            if delete:
                                response = requests.delete(
                                    f'{API_ADDRESS}/comments/{comment["comment_id"]}',
                                    json={
                                        "comment_id": comment["comment_id"]
                                    }
                                )

                    st.write(comment['body'])

                    col_bot_rate, col_bot_date = st.columns([3, 1])
                    with col_bot_rate:
                        if comment["rate"] == "Positive":
                            st.caption(f"Оценка: :green[{comment['rate']}]")
                        else:
                            st.caption(f"Оценка: :red[{comment['rate']}]")


                    with col_bot_date:
                        formatted_date = format_date(comment['created_at'])
                        st.markdown(
                            f'<p style="text-align: right; font-size: 0.85rem; opacity: 0.8; margin: 0;">'
                            f'{formatted_date}'
                            f'</p>',
                            unsafe_allow_html=True
                        )
                counter_comment += 1


    with users_rests:
        if not user_id:
            st.write("Login to see your bookings")

        response = requests.get(
            f"{API_ADDRESS}/book/user-bookings/{user_id}"
        )

        if response.status_code == 200:
            if not response.json():
                st.write("You do not have any bookings")
            for place in response.json():
                with st.container(border=True):

                    booking_id = place["book_id"]
                    name = place["place_name"]
                    city = place["city"]
                    booked_for = place["booked_for"]
                    time_at = place["created_at"]

                    col_text, col_btn = st.columns([0.8, 0.2])

                    with col_text:
                        st.write(f"### {name}")
                        st.write(f"📍 **City:** {city}")
                        st.write(f"📅 **Booked for:** {format_date(booked_for)}")
                        st.write(f"Created at: {format_date(time_at)}")



