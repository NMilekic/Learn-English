from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vocabulary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# CONFIGURE TABLES

class Words(db.Model):
    __tablename__ = 'english'
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(100), unique=True)
    serbian = db.Column(db.String(100))

# db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/learn', methods=['GET', 'POST'])
def learn():
    all_words = db.session.query(Words).all()
    #Dodati ako je prazna baza, probaj kroz Flask Message
    word = choice(all_words)
    if request.method == 'POST':
        answer = [request.form['answer_english'], request.form['answer_serbian']]
        guess_word_id = request.args.get('id')
        word = Words.query.get(guess_word_id)
        if word.english == answer[0] and word.serbian == answer[1]:
            db.session.delete(word)
            db.session.commit()
        return render_template('check_answer.html', word=word, answer=answer)
    return render_template("learn.html", word=word)

@app.route('/listofwords', methods=['GET', 'POST'])
def listofwords():
    if request.method == 'POST':
        english_word = request.form['english'].lower()
        serbian_word = request.form['serbian'].lower()
        #Potrebno je napraviti try-except za slucaj da se unese rec koja postoji u bazi
        new_word = Words(english=english_word, serbian=serbian_word)
        db.session.add(new_word)
        db.session.commit()

    all_words = db.session.query(Words).all()
    return render_template("listofwords.html", words=all_words)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
