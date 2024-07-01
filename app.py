from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    muscle_group = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/exercises')
def exercises():
    exercises = Exercise.query.all()
    return render_template('exercises.html', exercises=exercises)

@app.route('/add-exercise', methods=['GET', 'POST'])
def add_exercise():
    if request.method == 'POST':
        name = request.form['name']
        muscle_group = request.form['muscle_group']
        new_exercise = Exercise(name=name, muscle_group=muscle_group)
        db.session.add(new_exercise)
        db.session.commit()
        return redirect(url_for('exercises'))
    return render_template('add_exercise.html')

@app.route('/delete-exercise/<int:id>', methods=['GET', 'POST'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(exercise)
        db.session.commit()
        return redirect(url_for('exercises'))
    return render_template('delete_exercise.html', exercise=exercise)

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        training_type = request.form['training_type']
        return redirect(url_for('plan', training_type=training_type))
    return render_template('home.html')

@app.route('/plan/<training_type>')
def plan(training_type):
    exercises = Exercise.query.all()
    grouped_exercises = {
        'Legs': [e for e in exercises if e.muscle_group == 'Legs'],
        'Shoulders': [e for e in exercises if e.muscle_group == 'Shoulders'],
        'Chest': [e for e in exercises if e.muscle_group == 'Chest'],
        'Back': [e for e in exercises if e.muscle_group == 'Back'],
        'Biceps': [e for e in exercises if e.muscle_group == 'Biceps'],
        'Triceps': [e for e in exercises if e.muscle_group == 'Triceps'],
        'Calves': [e for e in exercises if e.muscle_group == 'Calves']
    }
    plan = generate_plan(training_type, grouped_exercises)
    return render_template('plan.html', training_type=training_type, plan=plan)

def generate_plan(training_type, exercises):
    plan = {}
    if training_type == 'Push Pull Legs':
        plan['Push'] = random.sample(exercises['Chest'], min(3, len(exercises['Chest']))) + \
                       random.sample(exercises['Shoulders'], min(2, len(exercises['Shoulders']))) + \
                       random.sample(exercises['Triceps'], min(1, len(exercises['Triceps'])))
        plan['Pull'] = random.sample(exercises['Back'], min(4, len(exercises['Back']))) + \
                       random.sample(exercises['Biceps'], min(1, len(exercises['Biceps']))) + \
                       random.sample(exercises['Shoulders'], min(1, len(exercises['Shoulders'])))
        plan['Legs'] = random.sample(exercises['Legs'], min(5, len(exercises['Legs']))) + \
                       random.sample(exercises['Calves'], min(1, len(exercises['Calves'])))
    elif training_type == 'Split':
        plan['Legs'] = random.sample(exercises['Legs'], min(4, len(exercises['Legs']))) + \
                       random.sample(exercises['Calves'], min(1, len(exercises['Calves'])))
        plan['Chest'] = random.sample(exercises['Chest'], min(5, len(exercises['Chest'])))
        plan['Back'] = random.sample(exercises['Back'], min(5, len(exercises['Back'])))
        plan['Arms'] = random.sample(exercises['Biceps'], min(2, len(exercises['Biceps']))) + \
                       random.sample(exercises['Triceps'], min(2, len(exercises['Triceps'])))
    elif training_type == 'FBW':
        plan['Day A'] = random.sample(exercises['Legs'], min(1, len(exercises['Legs']))) + \
                        random.sample(exercises['Chest'], min(1, len(exercises['Chest']))) + \
                        random.sample(exercises['Back'], min(1, len(exercises['Back'])))
        plan['Day B'] = random.sample(exercises['Legs'], min(1, len(exercises['Legs']))) + \
                        random.sample(exercises['Chest'], min(1, len(exercises['Chest']))) + \
                        random.sample(exercises['Back'], min(1, len(exercises['Back'])))
    return plan

if __name__ == '__main__':
    app.run(debug=True)