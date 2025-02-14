from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database configuration
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'postgres')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')

def connect_to_db():
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
    return conn

# Create table if not exists
def create_table():
    conn = connect_to_db()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                content TEXT
            )
        """)
        conn.commit()
        cur.close()
        conn.close()

create_table()

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'message': 'Title and content are required'}), 400

    conn = connect_to_db()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING id", (title, content))
            post_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'message': 'Post created successfully', 'id': post_id}), 201
        except psycopg2.Error as e:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({'message': f'Error creating post: {e}'}), 500
    else:
        return jsonify({'message': 'Database connection failed'}), 500

@app.route('/posts', methods=['GET'])
def get_posts():
    conn = connect_to_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT id, title, content FROM posts")
        posts = []
        for row in cur.fetchall():
            posts.append({'id': row[0], 'title': row[1], 'content': row[2]})
        cur.close()
        conn.close()
        return jsonify(posts), 200
    else:
        return jsonify({'message': 'Database connection failed'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
