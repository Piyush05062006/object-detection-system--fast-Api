import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Object Detection System", layout="wide")
st.title("🎯 Object Detection System")

# ── Sidebar Auth ─────────────────────────────
st.sidebar.title("Account")
auth_option = st.sidebar.selectbox("Choose", ["Login", "Register"])
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if auth_option == "Register":
    if st.sidebar.button("Register"):
        response = requests.post(f"{BASE_URL}/register",
            json={"username": username, "password": password})
        if response.status_code == 200:
            st.sidebar.success("Registered! Please login.")
        else:
            st.sidebar.error(response.json()["detail"])

if auth_option == "Login":
    if st.sidebar.button("Login"):
        response = requests.post(f"{BASE_URL}/login",
            json={"username": username, "password": password})
        if response.status_code == 200:
            st.session_state.token = response.json()["token"]
            st.session_state.username = username
            st.sidebar.success(f"Logged in as {username}")
        else:
            st.sidebar.error("Invalid credentials")

# ── Main Area ─────────────────────────────────
if "token" not in st.session_state:
    st.warning("Please login from the sidebar to use the app")

else:
    st.subheader(f"Welcome {st.session_state.username} 👋")

    tab1, tab2 = st.tabs(["🔍 Detect Objects", "📜 History"])

    # ── Tab 1 — Detection ─────────────────────
    with tab1:
        uploaded_file = st.file_uploader(
            "Upload an image",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", width=400)

            if st.button("Detect Objects"):
                with st.spinner("Detecting..."):
                    response = requests.post(
                        f"{BASE_URL}/detect",
                        headers={"authorization": f"Bearer {st.session_state.token}"},
                        files={"file": (uploaded_file.name, uploaded_file.getvalue())}
                    )

                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Found {data['total_objects']} object(s)!")

                    for det in data["detections"]:
                        st.write(
                            f"🟢 **{det['object']}** — "
                            f"{det['confidence']*100:.1f}% confidence"
                        )
                else:
                    st.error("Detection failed")

    # ── Tab 2 — History ───────────────────────
    with tab2:
        if st.button("Load History"):
            response = requests.get(
                f"{BASE_URL}/history",
                headers={"authorization": f"Bearer {st.session_state.token}"}
            )

            if response.status_code == 200:
                history = response.json()["history"]

                if not history:
                    st.info("No detections yet")
                else:
                    st.success(f"Total detections: {len(history)}")
                    for record in history:
                        with st.expander(f"📁 {record['filename']} — {record['timestamp']}"):
                            st.write(f"**Total objects:** {record['total_objects']}")
                            for det in record["detections"]:
                                st.write(
                                    f"🟢 **{det['object']}** — "
                                    f"{det['confidence']*100:.1f}% confidence"
                                )
            else:
                st.error("Failed to load history")