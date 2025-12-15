from flask import Flask, jsonify, request
import os
import mysql.connector

#flask app instance update joo
app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'db'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )


@app.get('/api/health')
def health():
    return jsonify(message={'status': 'ok'})
#ju
@app.get('/api/time')
def time():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT NOW()")
        row = cur.fetchone()
        return jsonify(message={'time': str(row[0])})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

@app.get('/api')
def index():
    """Simple endpoint that greets from DB."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 'Hello from MySQL via Testi!'")
        row = cur.fetchone()
        return jsonify(message=row[0])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

@app.route('/api/init-db')
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diary_entries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE NOT NULL,
                title VARCHAR(255) NOT NULL,
                content LONGTEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            INSERT INTO users (name, email) VALUES
            ('John Doe', 'john@example.com'),
            ('Jane Smith', 'jane@example.com')
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Database initialized"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

