import streamlit as st
import requests

from dotenv import load_dotenv
from datetime import datetime
import os


load_dotenv()

API_ADDRESS = os.getenv("API_BACKEND_ADRESS", "http://backend:8100")
user_id = st.session_state.get("user_data", {}).get("user_id")

st.set_page_config(
    page_title="User Profile",
    layout="wide"
)

st.title("👤 Your Profile")

if "user_data" not in st.session_state:
    st.warning("You need to log in first.")
    st.switch_page("pages/login.py")
    st.stop()

bookings = []
try:
    resp = requests.get(f"{API_ADDRESS}/book/user-bookings/{user_id}")
    if resp.status_code == 200:
        bookings = resp.json()
    else:
        st.error(f"Cannot load book: {resp.text}")
except Exception as e:
    st.error(f"Error with connection to server: {e}")

def format_date(raw: str) -> str:
    if not raw or raw == "—":
        return "—"
    try:
        # ISO-формат с "T" и микросекундами, возможно с "Z" на конце
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y %H:%M")
    except (ValueError, TypeError):
        return raw

exist_comments = []
try:
    resp = requests.get(f"{API_ADDRESS}/comments/list-comments")
    if resp.status_code == 200:
        exist_comments = resp.json()
    else:
        st.error(f"Cannot load commentary: {resp.text}")
except Exception as e:
    st.error(f"Error with connection to server: {e}")

exist_reviews = []
try:
    resp = requests.get(f"{API_ADDRESS}/comments/list-comments")
    if resp.status_code == 200:
        exist_comments = resp.json()
    else:
        st.error(f"Cannot load review: {resp.text}")
except Exception as e:
    st.error(f"Error with connection to server: {e}")

user = st.session_state.user_data

with st.container(border=True):
    col1, col2 = st.columns([1, 3])

    with col1:
        st.markdown("### Name:")

    with col2:
        st.subheader(user.get("username", "Unknown user"))
        #st.write(f"📧 {user.get('email', '—')}")
        st.write(f"🗓 Registered: {format_date(user.get('date_registration', '—'))}")
st.divider()

st.subheader("📊 Stats")

stat_col1, stat_col2, stat_col3 = st.columns(3)
stat_col1.metric("Reviews left", len(exist_reviews))
stat_col2.metric("Bookings made", len(bookings))
stat_col3.metric("Comments left", len(exist_comments))

st.divider()

st.subheader("📖 Booking history")

if not bookings:
    st.info("You have no bookings yet.")
else:
    counter_bookings = 0
    for booking in bookings:
        with st.container(border=True):
            b_col1, b_col2, b_col3 = st.columns([3, 2, 1])

            with b_col1:
                st.write(f"**{booking.get('place_name', 'Unknown place')}**")

            with b_col2:
                st.write(
                    f"{format_date(booking.get('booked_for', '—'))}")
            with b_col3:
                if (b_to := booking.get('booked_to')) and (b_from := booking.get('booked_from')) and b_to != "—" and b_from != "—" and datetime.fromisoformat(b_from.replace("Z", "+00:00")) <= datetime.now(datetime.fromisoformat(b_to.replace("Z", "+00:00")).tzinfo) <= datetime.fromisoformat(b_to.replace("Z", "+00:00")):
                    st.write(":green[Available.]")

                    cancel_booking = st.button(":red[Cancel booking]", key=f"cancel_button_{counter_bookings}")

                    if cancel_booking:
                        response = requests.delete(
                            f"{API_ADDRESS}/book/delete-booking/{booking['book_id']}",
                            json={"booking_is": booking["book_id"]}
                        )

                elif (b_to := booking.get('booked_to')) and b_to != "—" and datetime.fromisoformat(
                        b_to.replace("Z", "+00:00")) < datetime.now(
                        datetime.fromisoformat(b_to.replace("Z", "+00:00")).tzinfo):

                    st.write(":red[Overdue.]")

                else:
                    st.write(":green[Available.]")

                    cancel_booking = st.button(":red[Cancel booking]", key=f"cancel_button_{counter_bookings}")

                    if cancel_booking:
                        response = requests.delete(
                            f"{API_ADDRESS}/book/delete-booking/{booking['book_id']}",
                            json={"booking_is": booking["book_id"]}
                        )

        counter_bookings += 1



st.divider()

col_back, col_edit, col_logout, col_del = st.columns([1, 1, 1, 1])

with col_back:
    if st.button("⬅ Home"):
        st.switch_page("main.py")

with col_edit:
    edit = st.button("✏ Edit profile")


with col_logout:
    logout = st.button("🚪 Log out")
    # TODO: очистить сессию и токен авторизации
    # if logout:
    #     st.session_state.clear()
    #     st.switch_page("main.py")

with col_del:
    with st.form("delete_form"):
        delete_acc = st.form_submit_button(":red[Delete]")

        if delete_acc:
            confirmation_password = st.text_input("Сonfirm the password", type="password")

            response = requests.delete(
                f"{API_ADDRESS}/login/delete-acc/{user_id}",
                json={
                    "user_id": user_id,
                    "password": str(confirmation_password)
                }
            )

            if response.status_code == 200:
                st.markdown("Account was deleted")
                st.session_state.clear()
                st.switch_page("main.py")