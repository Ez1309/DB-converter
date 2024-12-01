import pandas as pd
import os
import sqlite3
import glob

def create_db(filename, db_name):
    """
    Create a SQLite database from a CSV or XLSX file.
    """
    connection = sqlite3.connect(f"./files/databases/{db_name}.db")
    file_path = f"./files/plans/{filename}"
    
    try:
        if filename.endswith(".xlsx"):
            frames = pd.read_excel(file_path, sheet_name=None)
            for sheet, df in frames.items():
                df.to_sql(sheet, con=connection, if_exists='replace', index=False)
                
        elif filename.endswith(".csv"):
            df = pd.read_csv(file_path)
            table_name = filename.replace(" ", "_").split(".")[0]
            df.to_sql(table_name, con=connection, if_exists='replace', index=False)
            
    except ValueError as UnsupportedFileExtension:
        print(f"Error: {UnsupportedFileExtension}\nThe uploaded file is not a CSV or XLSX file.")
    
    finally:
        connection.close()
        os.remove(file_path)

def create_table(filename):
    """
    Create a dictionary or list from a CSV or XLSX file for rendering in HTML templates.
    """
    file_path = f"./files/plans/{filename}"
    
    if filename.endswith(".csv"):
        df = pd.read_csv(file_path)
        data = df.to_dict("records")
        
    elif filename.endswith(".xlsx"):
        data = pd.read_excel(file_path, sheet_name=None)
        for sheet in data:
            data[sheet] = data[sheet].to_dict("records")
 
    os.remove(file_path)
    return data

def clean_files(session_id):
    """
    Remove all database files associated with a session ID.
    """
    if session_id is not None:
        files = glob.glob(f"./files/databases/{session_id}*.db")
        for file in files:
            os.remove(file)
