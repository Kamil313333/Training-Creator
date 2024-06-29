from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    muscle_group = db.Column(db.String(100), nullable=False)
    equipment_needed = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_exercise', methods=['GET', 'POST'])
def add_exercise():
    if request.method == 'POST':
        name = request.form['name']
        muscle_group = request.form['muscle_group']
        equipment_needed = request.form['equipment_needed']

        exercise = Exercise(name=name, muscle_group=muscle_group, equipment_needed=equipment_needed)
        db.session.add(exercise)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_exercise.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)