import sqlite3
import pandas as pd
import streamlit as st

def view_database():
    database_path = 'Data/database.db'
    
    st.title("Database Viewer")

    # Authentication
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if username == st.secrets["USERNAME"] and password == st.secrets["PASSWORD"]:
                st.session_state['authenticated'] = True
                st.success("Logged in successfully!")
            else:
                st.error("Invalid credentials")
    else:
        st.subheader("Database Tables")
        
        # Get table names
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()

        tables = [table[0] for table in tables]

        if tables:
            st.write("Select a table to view:")
            table_selection = st.selectbox("Table", tables)
            
            if table_selection:
                conn = sqlite3.connect(database_path)
                df = pd.read_sql_query(f'SELECT * FROM {table_selection}', conn)
                conn.close()
                st.write(f"Data from table: {table_selection}")
                st.dataframe(df,use_container_width=True)
        else:
            st.write("No tables found in the database.")
