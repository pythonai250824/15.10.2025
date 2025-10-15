import streamlit as st
import psycopg2
import time
import json

# ---------- Database Setup ----------

def get_db_config():
    # with = like using finally + close
    with open('db_config.json') as f:
        return json.load(f)

def get_connection():
    config = get_db_config()
    return psycopg2.connect(**config)

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_name VARCHAR(50) UNIQUE NOT NULL,
            pwd VARCHAR(50) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, user_name FROM users ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def add_user(user_name, pwd):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (user_name, pwd) VALUES (%s, %s) ON CONFLICT (user_name) DO NOTHING;", (user_name, pwd))
    conn.commit()
    cur.close()
    conn.close()

def delete_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

# ---------- Streamlit UI ----------
st.title("User DB Table Management")

create_table()

# Refresh button
if st.button("🔄 Refresh User List"):
    st.rerun()

# --- Show users ---
st.subheader("👥 Current Users:")
users = get_users()
if users:
    for uid, uname in users:
        st.write(f"**{uid}.** {uname}")

# --- Add new user ---
st.subheader("➕ Add New User")
new_user = st.text_input("Username:")
new_pwd = st.text_input("Password:", type="password")

if st.button("Create User"):
    if new_user and new_pwd:
        add_user(new_user, new_pwd)
        st.success(f"User '{new_user}' created successfully!")
        time.sleep(1)
        st.rerun()
    else:
        st.warning("Please fill in both fields.")

#--------------- BONUS

# --- Delete user ---
st.subheader("🗑️ Delete User")
users = get_users()
if users:
    user_dict = {f"{uname} (ID: {uid})": uid for uid, uname in users}
    selected_user = st.selectbox("Select user to delete:", list(user_dict.keys()))
    if st.button("Delete Selected User"):
        delete_user(user_dict[selected_user])
        st.success(f"User '{selected_user}' deleted successfully!")
        time.sleep(1)
        st.rerun()
else:
    st.info("No users to delete.")