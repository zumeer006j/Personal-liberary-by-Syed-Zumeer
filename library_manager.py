import streamlit as st
import pandas as pd
import json
import os
import datetime
import time
import random
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

st.set_page_config(
    page_title="Personal Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem !important;
        color: #1E3A8A;
        font-weight: 700;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

if 'library' not in st.session_state:
    st.session_state.library = []
if 'book_added' not in st.session_state:
    st.session_state.book_added = False
if 'book_removed' not in st.session_state:
    st.session_state.book_removed = False
if 'current_view' not in st.session_state:
    st.session_state.current_view = "library"

def load_library():
    try:
        if os.path.exists('library.json'):
            with open('library.json', 'r') as file:
                st.session_state.library = json.load(file)
    except Exception as e:
        st.error(f"Error loading library: {e}")

def save_library():
    try:
        with open('library.json', 'w') as file:
            json.dump(st.session_state.library, file)
    except Exception as e:
        st.error(f"Error saving library: {e}")

def add_book(title, author, publication_year, genre, read_status):
    book = {
        'title': title,
        'author': author,
        'publication_year': publication_year,
        'genre': genre,
        'read_status': read_status,
        'added_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.library.append(book)
    save_library()
    st.session_state.book_added = True
    time.sleep(0.5)

def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        del st.session_state.library[index]
        save_library()
        st.session_state.book_removed = True

def get_library_stats():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book['read_status'])
    percent_read = (read_books / total_books * 100) if total_books > 0 else 0
    return {
        'total_books': total_books,
        'read_books': read_books,
        'percent_read': percent_read,
    }

st.sidebar.markdown("<h1>Navigation</h1>", unsafe_allow_html=True)
nav_options = st.sidebar.radio(
    "Choose an option:",
    ["View Library", "Add Book", "Library Statistics"]
)

if nav_options == "View Library":
    st.session_state.current_view = "library"
elif nav_options == "Add Book":
    st.session_state.current_view = "add"
elif nav_options == "Library Statistics":
    st.session_state.current_view = "stats"

st.markdown("<h1 class='main-header'>Personal Library Manager</h1>", unsafe_allow_html=True)

if st.session_state.current_view == "add":
    st.markdown("<h2>Add a New Book</h2>", unsafe_allow_html=True)
    with st.form(key='add_book_form'):
        title = st.text_input("Book Title", max_chars=100)
        author = st.text_input("Author", max_chars=100)
        publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.datetime.now().year, step=1, value=2023)
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "Technology", "Romance", "Poetry", "Self-help", "Art", "Religion", "History"])
        read_status = st.radio("Read Status", ["Read", "Unread"], horizontal=True) == "Read"
        submit_button = st.form_submit_button(label="Add Book")
        if submit_button and title and author:
            add_book(title, author, publication_year, genre, read_status)

    if st.session_state.book_added:
        st.success("Book added successfully!")
        st.session_state.book_added = False

elif st.session_state.current_view == "library":
    st.markdown("<h2>Your Library</h2>", unsafe_allow_html=True)
    if not st.session_state.library:
        st.warning("Your library is empty. Add some books to get started.")
    else:
        for i, book in enumerate(st.session_state.library):
            st.markdown(f"""
                **Title:** {book['title']}  
                **Author:** {book['author']}  
                **Year:** {book['publication_year']}  
                **Genre:** {book['genre']}  
                **Status:** {'Read' if book['read_status'] else 'Unread'}
            """)
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove {book['title']}", key=f"remove_{i}"):
                    remove_book(i)
                    st.experimental_rerun()

elif st.session_state.current_view == "stats":
    st.markdown("<h2>Library Statistics</h2>", unsafe_allow_html=True)
    if not st.session_state.library:
        st.warning("Your library is empty. Add some books to view stats.")
    else:
        stats = get_library_stats()
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Books", stats['total_books'])
        col2.metric("Books Read", stats['read_books'])
        col3.metric("% Read", f"{stats['percent_read']:.2f}%")

st.markdown("---")
st.markdown("© 2025 Personal Library Manager")

