from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class UserSession(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    question = db.Column(db.String(200))
    answer = db.Column(db.String(200))

db.create_all()

@app.route('/')
def index():
    session_id = str(uuid.uuid4())
    session['session_id'] = session_id
    new_session = UserSession(id=session_id, question="What is 2+2?", answer="")
    db.session.add(new_session)
    db.session.commit()
    return render_template('index.html', session_id=session_id)

@app.route('/question/<session_id>')
def question(session_id):
    user_session = UserSession.query.get(session_id)
    if user_session:
        return render_template('question.html', question=user_session.question, session_id=session_id)
    else:
        return "Invalid session ID", 404

@app.route('/submit_answer/<session_id>', methods=['POST'])
def submit_answer(session_id):
    user_session = UserSession.query.get(session_id)
    if user_session:
        user_session.answer = request.form['answer']
        db.session.commit()
        return "Answer submitted!"
    else:
        return "Invalid session ID", 404

if __name__ == '__main__':
    app.run(debug=True)
