import streamlit as st
import json
import os

USERS_FILE = "users.json"

# Load users from file or create empty dict
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

# Save users to file
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# Initialize session state variables
if "users" not in st.session_state:
    st.session_state.users = load_users()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

def sign_up():
    st.subheader("Sign Up")
    new_user = st.text_input("New username", key="new_user")
    new_password = st.text_input("New password", type="password", key="new_pass")
    if st.button("Create account"):
        if not new_user or not new_password:
            st.error("Please enter both username and password.")
        elif new_user in st.session_state.users:
            st.error("Username already exists.")
        else:
            st.session_state.users[new_user] = new_password
            save_users(st.session_state.users)
            st.success("Account created! Please sign in.")
            st.experimental_rerun()

def sign_in():
    st.subheader("Sign In")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Sign In"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

def main_app():
    st.title("Main App")
    st.write(f"Hello, **{st.session_state.username}**! You have access to this app.")
    if st.button("Sign Out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()

def access_denied():
    st.error("You do not have access to this app or it does not exist.")
    st.info("Please sign in to continue.")
    st.write("If you believe this is a bug, contact support.")

def app():
    st.title("Welcome")

    if st.session_state.logged_in:
        main_app()
    else:
        col1, col2 = st.columns(2)
        with col1:
            sign_in()
        with col2:
            sign_up()
        # Optionally, show access denied message here if user tries restricted content
        # access_denied()

if __name__ == "__main__":
    app()
