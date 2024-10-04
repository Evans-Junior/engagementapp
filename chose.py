import streamlit as st
import threading
import time
import random
from collections import defaultdict

# Initialize session state for user name and selected room
if 'username' not in st.session_state:
    st.session_state.username = ''

if 'selected_room' not in st.session_state:
    st.session_state.selected_room = ''

# Define available rooms (classes)
ROOMS = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'Computer Science']

# Global dictionary to store queues for each room
# Using defaultdict for automatic list creation
queues = defaultdict(list)
queue_lock = threading.Lock()

# Function to add user to queue
def join_queue(room, username):
    with queue_lock:
        if username not in queues[room]:
            queues[room].append(username)

# Function to remove user from queue (optional, e.g., after contribution)
def leave_queue(room, username):
    with queue_lock:
        if username in queues[room]:
            queues[room].remove(username)

# Function to generate random color in HEX
def get_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# Streamlit App Layout
st.title("📚 Complex Queuing System for Classes")

st.sidebar.header("User Settings")

# User enters their name
username = st.sidebar.text_input("Enter your name", st.session_state.username)
st.session_state.username = username.strip()

# User selects a room
selected_room = st.sidebar.selectbox("Select a Room", ROOMS, index=0)
st.session_state.selected_room = selected_room

# Button to join the queue
if st.sidebar.button("Join Queue"):
    if st.session_state.username:
        join_queue(st.session_state.selected_room, st.session_state.username)
        st.sidebar.success(f"Joined the queue for {st.session_state.selected_room}!")
    else:
        st.sidebar.error("Please enter your name to join the queue.")

st.markdown("## Current Queue")

# Placeholder for the queue display
queue_placeholder = st.empty()

# Function to display the queue with randomized colors, within the main Streamlit thread
def display_queue():
    with queue_lock:
        current_queue = queues[selected_room].copy()
    if current_queue:
        # Create HTML for horizontal display with random colors
        html_content = "<div style='display: flex; flex-wrap: wrap;'>"
        for user in current_queue:
            color = get_random_color()
            html_content += f"""
            <div style="
                background-color: {color};
                color: white;
                padding: 10px 20px;
                margin: 5px;
                border-radius: 20px;
                animation: fadein 2s;
                ">
                {user}
            </div>
            """
        html_content += "</div>"
    else:
        html_content = "<p>No one is in the queue.</p>"
    
    # Add some CSS for animation
    html_content += """
    <style>
    @keyframes fadein {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
    """
    queue_placeholder.markdown(html_content, unsafe_allow_html=True)

# Update queue display every 2 seconds
while True:
    display_queue()
    time.sleep(2)

# Optional: Allow users to leave the queue
st.sidebar.markdown("---")
if st.sidebar.button("Leave Queue"):
    if st.session_state.username:
        leave_queue(st.session_state.selected_room, st.session_state.username)
        st.sidebar.success(f"Left the queue for {st.session_state.selected_room}.")
    else:
        st.sidebar.error("You are not in any queue.")

# Optional: Display all queues for debugging
# st.write("All Queues:", queues)
