# Password Generator

A secure password generator built with Python and Streamlit. It includes a web app for generating strong passwords and a small CLI script for quick terminal use.

## Live Demo

https://ekhsanfitri94-password-generator.streamlit.app/

## Features

- Cryptographically secure password generation with Python's `secrets` module
- Easy, medium, and hard password modes
- Option to remove ambiguous characters such as `O`, `0`, `I`, `l`, and `1`
- Entropy-based password strength estimate
- One-click copy button in the web app
- Optional backend sync for saving generated passwords

## App Modes

### Streamlit app

The main interface is `app.py`. It lets you choose length, difficulty, and backend sync behavior.

### CLI script

`password_generator.py` is a terminal-based version for generating passwords without the web UI.

## Local Setup

1. Clone the repository.

```bash
git clone https://github.com/EkhsanFitri94/password-generator.git
cd password-generator
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Run the Streamlit app.

```bash
streamlit run app.py
```

4. Or run the CLI version.

```bash
python password_generator.py
```

## Environment Variables

- `BACKEND_URL`: optional API base URL used by the Streamlit app to sync generated passwords.

Example:

```bash
BACKEND_URL=https://ekhsan-fastapi.onrender.com
```

## Project Structure

```text
.
├── app.py
├── password_generator.py
├── README.md
├── requirements.txt
└── .devcontainer/
```

## Notes

- The web app requires the backend URL only if you want password sync enabled.
- The CLI version is useful for quick generation without a browser.
