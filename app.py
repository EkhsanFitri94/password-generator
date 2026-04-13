import streamlit as st
import string
import secrets
import math
import json
import httpx
import streamlit.components.v1 as components

AMBIGUOUS_CHARS = "O0Il1|`'\""


def remove_ambiguous_chars(char_pool):
    return "".join(ch for ch in char_pool if ch not in AMBIGUOUS_CHARS)


def calculate_strength(length, pool_size):
    # Entropy approximation in bits.
    entropy = length * math.log2(pool_size)
    score = min(int(entropy), 100)

    if entropy < 40:
        label = "Weak"
    elif entropy < 60:
        label = "Fair"
    elif entropy < 80:
        label = "Strong"
    else:
        label = "Very Strong"

    return score, entropy, label


# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Password Generator", page_icon="🔐")

# --- APP TITLE AND DESCRIPTION ---
st.title("🔐 Secure Password Generator")
st.write("Generate cryptographically secure passwords instantly.")

# --- USER INTERFACE (Sliders and Buttons) ---
# Create a slider between 4 and 128 (defaults to 12)
length = st.slider("Password Length", min_value=4, max_value=128, value=12)

# Create a radio button for difficulty
difficulty = st.radio("Difficulty Level", ("Easy", "Medium", "Hard"), horizontal=True)

# Optional filter for easier human readability
exclude_ambiguous = st.checkbox(
    "Exclude ambiguous characters (O, 0, I, l, 1, etc.)", value=True
)

# Determine the character pool based on the radio button
if difficulty == "Easy":
    pool = string.ascii_letters
    description = "Letters only (A-Z, a-z)"
elif difficulty == "Medium":
    pool = string.ascii_letters + string.digits
    description = "Letters and Numbers (A-Z, a-z, 0-9)"
else:
    pool = string.ascii_letters + string.digits + string.punctuation
    description = "Letters, Numbers, and Symbols (Maximum Security)"

if exclude_ambiguous:
    pool = remove_ambiguous_chars(pool)
    description += " minus ambiguous characters"

st.caption(f"Pool includes: *{description}*")
st.caption(f"Pool size: {len(pool)} characters")

# --- GENERATE BUTTON ---
if st.button("Generate Password", type="primary", use_container_width=True):
    # This is the exact same logic you wrote in your original file!
    password = "".join(secrets.choice(pool) for _ in range(length))
    st.session_state["generated_password"] = password

if "generated_password" in st.session_state:
    password = st.session_state["generated_password"]

    # Display the password in a big, bold code block
    st.code(password, language=None)

    score, entropy, strength_label = calculate_strength(length, len(pool))
    st.progress(score / 100)
    st.write(f"Strength: **{strength_label}** ({entropy:.1f} bits of entropy)")

    escaped_password = json.dumps(password)
    copy_html = f"""
    <button onclick='navigator.clipboard.writeText({escaped_password});'
            style=\"width:100%;padding:0.6rem 0.9rem;border:1px solid #d0d0d0;border-radius:8px;cursor:pointer;\">
      Copy Password
    </button>
    """
    components.html(copy_html, height=52)

    st.toast("Password generated and ready to copy.")

    # --- NEW: SEND TO BACKEND ---
    # The live URL of your FastAPI API
    API_URL = "https://ekhsan-fastapi.onrender.com/passwords"

    try:
        # Send the password to your backend in the background
        response = httpx.post(API_URL, json={"password": password}, timeout=5.0)
        if response.status_code == 201:
            st.success("✅ Synced to database!")
    except httpx.RequestError:
        # If the API is sleeping or the internet is down, don't crash the app
        st.warning("⚠️ Could not reach the backend API.")

st.divider()
st.caption("Built with ❤️ by EkhsanFitri94 using Python & Streamlit")
