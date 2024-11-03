import json
import sqlite3

# Load data from JSON file
with open('db.json') as f:  # Replace with the actual path
    data = json.load(f)

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Function to create tables based on model data
def create_tables(data):
    tables = {}
    for entry in data:
        model_name = entry['model'].replace(".", "_")
        fields = entry['fields']
        
        if model_name not in tables:
            # Dynamically create SQL table structure
            columns = ["id INTEGER PRIMARY KEY"]
            for field, value in fields.items():
                if isinstance(value, int):
                    col_type = "INTEGER"
                elif isinstance(value, float):
                    col_type = "REAL"
                elif isinstance(value, str):
                    col_type = "TEXT"
                elif isinstance(value, bool):
                    col_type = "BOOLEAN"
                else:
                    col_type = "TEXT"
                
                columns.append(f"{field} {col_type}")
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {model_name} ({', '.join(columns)});"
            cursor.execute(create_table_sql)
            tables[model_name] = fields.keys()

# Function to insert data
def insert_data(data):
    for entry in data:
        model_name = entry['model'].replace(".", "_")
        fields = entry['fields']
        placeholders = ', '.join(['?'] * len(fields))
        columns = ', '.join(fields.keys())
        values = tuple(fields.values())
        
        insert_sql = f"INSERT INTO {model_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(insert_sql, values)

# Create tables and insert data
create_tables(data)
insert_data(data)

# Commit and close connection
conn.commit()
conn.close()
print("Data successfully inserted into the SQLite database.")