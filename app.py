from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Model Exercise
class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    muscle_group = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Exercise {self.name}>'

# Tworzenie przykładowych ćwiczeń w bazie danych
def create_sample_exercises():
    exercises = [
        Exercise(name='Push-ups', muscle_group='Chest'),
        Exercise(name='Pull-ups', muscle_group='Back'),
        Exercise(name='Squats', muscle_group='Legs'),
        Exercise(name='Plank', muscle_group='Core')
    ]
    db.session.bulk_save_objects(exercises)
    db.session.commit()

# Widok listy ćwiczeń z podziałem na grupy mięśniowe
@app.route('/')
def exercises():
    exercises = Exercise.query.all()
    return render_template('exercises.html', exercises=exercises)

# Widok dodawania nowego ćwiczenia
@app.route('/add_exercise', methods=['GET', 'POST'])
def add_exercise():
    if request.method == 'POST':
        name = request.form['name']
        muscle_group = request.form['muscle_group']

        new_exercise = Exercise(name=name, muscle_group=muscle_group)
        db.session.add(new_exercise)
        db.session.commit()

        return redirect(url_for('exercises'))

    return render_template('add_exercise.html')

# Widok usuwania ćwiczenia
@app.route('/delete_exercise/<int:id>', methods=['POST'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return redirect(url_for('exercises'))

# Inicjalizacja bazy danych
with app.app_context():
    db.create_all()
    create_sample_exercises()

# Uruchomienie aplikacji
if __name__ == '__main__':
    app.run(debug=True)