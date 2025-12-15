from flask import Flask, jsonify
import os
import mysql.connector

#flask app instance update joo
app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'db')
DB_USER = os.getenv('DB_USER', 'appuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'changeme')
DB_NAME = os.getenv('DB_NAME', 'appdb')

@app.get('/api/health')
def health():
    return jsonify(message={'status': 'ok'})
#ju
@app.get('/api/time')
def time():
    # Placeholder for actual time fetching logic
    #get server time from db
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    cur = conn.cursor()
    cur.execute("SELECT NOW()")
    row = cur.fetchone()
    cur.close(); conn.close()
    return jsonify(message={'time': row[0]})

@app.get('/api')
def index():
    """Simple endpoint that greets from DB."""
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    cur = conn.cursor()
    cur.execute("SELECT 'Hello from MySQL via Testi!'")
    row = cur.fetchone()
    cur.close(); conn.close()
    return jsonify(message=row[0])
@app.route('/api/diary/add', methods=['POST'])
def add_diary_entry():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['date', 'title', 'content']):
            return jsonify({"error": "Missing required fields"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO diary_entries (date, title, content)
            VALUES (%s, %s, %s)
        """, (data['date'], data['title'], data['content']))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Diary entry added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/diary/entries')
def get_diary_entries():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT date, title, content FROM diary_entries
            ORDER BY date DESC, created_at DESC
        """)
        entries = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Format dates for display
        for entry in entries:
            if isinstance(entry['date'], bytes):
                entry['date'] = entry['date'].decode('utf-8')
            else:
                entry['date'] = str(entry['date'])
        
        return jsonify(entries)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Dev-only fallback
    app.run(host='0.0.0.0', port=8000, debug=True)

