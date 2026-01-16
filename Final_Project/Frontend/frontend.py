import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# ---------- Gradient Background ----------
def add_bg_gradient():
    st.markdown(
        """
        <style>
        /* Main app background */
        .stApp {
            background: linear-gradient(135deg, #1e3c72, #2a5298, #6dd5ed);
            background-attachment: fixed;
        }

        /* Headings */
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
        }

        label, p {
            color: #f5f5f5 !important;
        }

        /* Text area */
        textarea {
            background-color: #ffffff !important;
            color: #000000 !important;
            border-radius: 10px;
            font-size: 16px;
        }

        /* Button */
        div.stButton > button {
            background: linear-gradient(90deg, #ff512f, #dd2476);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.6em 1em;
            font-weight: bold;
            font-size: 16px;
        }

        /* Recommendation / info boxes */
        .stAlert {
            background-color: #ffffff !important;
            color: #000000 !important;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
            font-size: 15px;
        }

        /* Warning & error text */
        .stAlert p {
            color: #000000 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------- UI ----------
def frontend_ui():
    add_bg_gradient()

    st.markdown("<h1>Welcome to our AI based</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Smart Ticket Resolution System</h2>", unsafe_allow_html=True)

    st.subheader("Entry your ticket")
    ticket_text = st.text_area(
        "Description",
        placeholder="Type the user issue here..."
    )

    analyze_btn = st.button("Analyze Ticket", use_container_width=True)

    if analyze_btn:
        if not ticket_text:
            st.warning("Please enter a ticket description.")
        else:
            with st.spinner("🤖 AI processing in progress..."):
                try:
                    final_content = ticket_text

                    rec_response = requests.post(
                        f"{API_URL}/recommend",
                        json={"content": final_content}
                    )

                    recommendations = rec_response.json().get("recommendations", [])

                    st.divider()
                    st.markdown("**These are the solutions related to your issue:**")

                    if recommendations:
                        for idx, rec in enumerate(recommendations, 1):
                            st.info(f"{idx}. {rec}")
                    else:
                        st.warning("No matches found.")

                except requests.exceptions.ConnectionError:
                    st.error("❌ Could not connect to the Backend API.")

# ---------- Run ----------
if __name__ == "__main__":
    frontend_ui()


