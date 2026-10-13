import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Role-based Creative Chatbot", page_icon="🎭", layout="wide")

ROLES = {
    "🎥 Video Director": {
        "system": (
            "You are an experienced video director. Answer with concrete advice on "
            "shot composition, camera movement, lighting, editing rhythm, and "
            "storytelling. Suggest specific shots or scene ideas."
        ),
        "hint": "Think like a director: plan the shots, framing, and mood of a film scene.",
        "placeholder": "e.g., How can I express sadness in movement?",
    },
    "💃 Dance Instructor": {
        "system": (
            "You are a professional dance instructor and choreographer. Answer with "
            "practical guidance on movement, rhythm, body expression, and "
            "choreography. Describe movements step by step."
        ),
        "hint": "Think like a choreographer: express emotion through the body.",
        "placeholder": "e.g., How can I express sadness in movement?",
    },
    "👗 Fashion Stylist": {
        "system": (
            "You are a creative fashion stylist. Answer with ideas about outfits, "
            "color palettes, textures, silhouettes, and styling that fit the "
            "mood or concept described."
        ),
        "hint": "Think like a stylist: let clothing and color tell the story.",
        "placeholder": "e.g., What outfit conveys quiet confidence?",
    },
    "🎭 Acting Coach": {
        "system": (
            "You are an acting coach. Answer with practical techniques for emotion, "
            "voice, gesture, character building, and scene work. Offer short "
            "exercises the actor can try."
        ),
        "hint": "Think like a coach: build a believable character and emotion.",
        "placeholder": "e.g., How do I play a character hiding grief?",
    },
    "🎨 Art Curator": {
        "system": (
            "You are an art curator. Answer with insights on themes, visual "
            "language, art history, and exhibition concepts. Connect ideas to "
            "relevant artists or movements."
        ),
        "hint": "Think like a curator: connect ideas to art and context.",
        "placeholder": "e.g., How would you curate an exhibition about memory?",
    },
    "📷 Camera Settings Helper": {
        "system": (
            "You are an expert photography instructor who helps people choose camera "
            "settings. The user will describe the shot they want: the subject, the "
            "lighting conditions, and the look or mood they're after. Respond with:\n"
            "1. Recommended settings: aperture (f-stop), shutter speed, ISO, and, when "
            "relevant, white balance, focus mode, and metering mode.\n"
            "2. Why each setting works for this shot, in one or two short sentences "
            "(depth of field, motion blur or freezing motion, noise, exposure).\n"
            "3. A quick tip for adjusting if the light is brighter or darker than "
            "described.\n"
            "If key information is missing (for example, whether the subject is "
            "moving, or whether the user is using a tripod), state your assumption "
            "and give the settings anyway. Keep the answer practical and easy to "
            "follow for someone setting up a manual camera."
        ),
        "hint": "Describe the shot, the light, and the look you want. You'll get aperture, shutter speed, and ISO.",
        "placeholder": "e.g., Portrait at sunset with a blurry background, soft golden light, no tripod.",
    },
}

with st.sidebar:
    st.subheader("🔑 API & Role Settings")
    api_key = st.text_input("Enter your OpenAI API Key:", type="password", placeholder="sk-xxxxxxxxxxxxxxxxx")
    role_name = st.selectbox("Choose a role:", list(ROLES.keys()))
    st.info(ROLES[role_name]["hint"])
    model = st.selectbox("Model:", ["gpt-4o-mini", "gpt-4o"], index=0)

st.title("🎭 Role-based Creative Chatbot")
st.write("Select a creative role and ask your question!")

question = st.text_area(
    "💬 Enter your question or idea:",
    placeholder=ROLES[role_name]["placeholder"],
)

if st.button("Generate Response"):
    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar.")
    elif not question.strip():
        st.warning("Please enter a question or idea.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            with st.spinner("Thinking..."):
                resp = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": ROLES[role_name]["system"]},
                        {"role": "user", "content": question},
                    ],
                    temperature=0.3 if "Camera" in role_name else 0.8,
                )
            st.markdown(f"### {role_name}")
            st.write(resp.choices[0].message.content)
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.caption("Built for 'Art & Advanced Big Data' • Prof. Jahwan Koo (SKKU)")
