from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    genre_filter = request.args.get("genre", "All")

    conn = sqlite3.connect("books_music.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Fetch available genres
    cursor.execute("SELECT DISTINCT book_genre FROM books_music")
    genres = [row["book_genre"] for row in cursor.fetchall()]
    genres.insert(0, "All")  # Add "All" option at the top

    # Filter data
    if genre_filter == "All":
        cursor.execute("SELECT * FROM books_music")
    else:
        cursor.execute("SELECT * FROM books_music WHERE book_genre=?", (genre_filter,))
    
    results = cursor.fetchall()
    conn.close()
    return render_template("index.html", rows=results, genres=genres, selected_genre=genre_filter)

if __name__ == '__main__':
    app.run(debug=True)
