from flask import Flask, render_template, request, redirect
import sqlite3
import hashlib

app = Flask(__name__)

def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS web_url(original_url TEXT NOT NULL, short_url TEXT NOT NULL);')
    print("Table created successfully")
    conn.close()

init_sqlite_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_short_url', methods=['POST'])
def create_short_url():
    if request.method == 'POST':
        original_url = request.form['url']
        hash_object = hashlib.md5(original_url.encode())
        short_url = hash_object.hexdigest()[:10]
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO web_url(original_url, short_url) VALUES(?, ?)', (original_url, short_url))
            conn.commit()
        return render_template('url_display.html', url=short_url)

@app.route('/<short_url>')
def redirect_url(short_url):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute('SELECT original_url FROM web_url WHERE short_url=?', (short_url,))
        try:
            url = result.fetchone()[0]
            return redirect(url)
        except TypeError:
            return "URL not found"

if __name__ == '__main__':
    app.run(port=8080, debug=True)
