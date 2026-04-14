import streamlit as st
import string
import secrets
import math
import json
import os
from urllib.parse import urlsplit, urlunsplit

import httpx
import streamlit.components.v1 as components

AMBIGUOUS_CHARS = "O0Il1|`'\""


def build_password_endpoint(backend_url):
    parsed_url = urlsplit(backend_url)
    path = parsed_url.path.rstrip("/")

    if path.endswith("/passwords"):
        endpoint_path = path
    elif path in ("", "/"):
        endpoint_path = "/passwords"
    else:
        endpoint_path = f"{path}/passwords"

    return urlunsplit(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            endpoint_path,
            parsed_url.query,
            parsed_url.fragment,
        )
    )


def sync_password_to_backend(password):
    backend_url = os.getenv("BACKEND_URL", "").strip()

    if not backend_url:
        return {"state": "disabled", "message": "BACKEND_URL is not set."}

    try:
        endpoint_url = build_password_endpoint(backend_url)
        response = httpx.post(
            endpoint_url,
            json={"password": password},
            timeout=5.0,
        )
    except httpx.TimeoutException:
        return {
            "state": "error",
            "message": "Request timed out while contacting backend.",
        }
    except httpx.RequestError as exc:
        return {
            "state": "error",
            "message": (
                "Network error while contacting backend "
                f"({exc.__class__.__name__})."
            ),
        }

    if response.status_code in (200, 201):
        return {"state": "ok", "message": "Password synced to backend."}

    return {
        "state": "error",
        "message": f"Backend returned HTTP {response.status_code}.",
    }


def check_backend_connection():
    backend_url = os.getenv("BACKEND_URL", "").strip()

    if not backend_url:
        return {"state": "disabled", "message": "BACKEND_URL is not set."}

    endpoint_url = build_password_endpoint(backend_url)

    try:
        response = httpx.get(endpoint_url, timeout=5.0)
    except httpx.TimeoutException:
        return {
            "state": "error",
            "message": "Connection test timed out while contacting backend.",
        }
    except httpx.RequestError as exc:
        return {
            "state": "error",
            "message": (
                "Connection test failed "
                f"({exc.__class__.__name__})."
            ),
        }

    if response.status_code in (200, 201, 405):
        return {
            "state": "ok",
            "message": (
                f"Backend reachable at {endpoint_url} "
                f"(HTTP {response.status_code})."
            ),
        }

    if response.status_code == 404:
        return {
            "state": "warning",
            "message": (
                "Backend reachable, but endpoint not found: "
                f"{endpoint_url}"
            ),
        }

    return {
        "state": "error",
        "message": (
            "Backend responded with unexpected status "
            f"HTTP {response.status_code}."
        ),
    }


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
difficulty = st.radio(
    "Difficulty Level",
    ("Easy", "Medium", "Hard"),
    horizontal=True,
)

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

if st.button("Test Backend Connection", use_container_width=True):
    connection_result = check_backend_connection()

    if connection_result["state"] == "ok":
        st.success(f"✅ {connection_result['message']}")
    elif connection_result["state"] == "warning":
        st.warning(f"⚠️ {connection_result['message']}")
    elif connection_result["state"] == "error":
        st.error(f"❌ {connection_result['message']}")
    else:
        st.info(f"ℹ️ {connection_result['message']}")

# --- GENERATE BUTTON ---
if st.button("Generate Password", type="primary", use_container_width=True):
    # This is the exact same logic you wrote in your original file!
    password = "".join(secrets.choice(pool) for _ in range(length))
    st.session_state["generated_password"] = password

    st.toast("Password generated and ready to copy.")

    sync_result = sync_password_to_backend(password)
    if sync_result["state"] == "ok":
        st.success("✅ Synced to database!")
    elif sync_result["state"] == "error":
        st.warning(f"⚠️ {sync_result['message']}")

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
            style=\"width:100%;padding:0.6rem 0.9rem;border:1px solid #d0d0d0;
            border-radius:8px;cursor:pointer;\">
      Copy Password
    </button>
    """
    components.html(copy_html, height=52)

st.divider()
st.caption("Built with ❤️ by EkhsanFitri94 using Python & Streamlit")

