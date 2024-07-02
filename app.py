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

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        training_type = request.form['training_type']
        if training_type == 'Push Pull Legs':
            plan = generate_push_pull_legs_plan()
        elif training_type == 'Split':
            plan = generate_split_plan()
        elif training_type == 'FBW':
            plan = generate_fbw_plan()
        else:
            return "Unknown training type"

        return render_template('plan.html', training_type=training_type, plan=plan)

    return render_template('home.html')

@app.route('/exercises')
def exercises():
    all_exercises = Exercise.query.all()
    return render_template('exercises.html', exercises=all_exercises)

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

@app.route('/delete_exercise/<int:id>', methods=['POST'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if exercise:
        db.session.delete(exercise)
        db.session.commit()
    return redirect(url_for('exercises'))

def generate_push_pull_legs_plan():
    chest_exercises = Exercise.query.filter_by(muscle_group='Chest').all()
    shoulders_exercises = Exercise.query.filter_by(muscle_group='Shoulders').all()
    triceps_exercises = Exercise.query.filter_by(muscle_group='Triceps').all()
    back_exercises = Exercise.query.filter_by(muscle_group='Back').all()
    biceps_exercises = Exercise.query.filter_by(muscle_group='Biceps').all()
    legs_exercises = Exercise.query.filter_by(muscle_group='Legs').all()
    calves_exercises = Exercise.query.filter_by(muscle_group='Calves').all()

    plan = {}
    plan['Push'] = random.sample(chest_exercises, min(3, len(chest_exercises))) + \
                   random.sample(shoulders_exercises, min(2, len(shoulders_exercises))) + \
                   random.sample(triceps_exercises, min(1, len(triceps_exercises)))
    plan['Pull'] = random.sample(back_exercises, min(4, len(back_exercises))) + \
                   random.sample(biceps_exercises, min(1, len(biceps_exercises))) + \
                   random.sample(shoulders_exercises, min(1, len(shoulders_exercises)))
    plan['Legs'] = random.sample(legs_exercises, min(5, len(legs_exercises))) + \
                   random.sample(calves_exercises, min(1, len(calves_exercises)))
    
    return plan

def generate_split_plan():
    chest_exercises = Exercise.query.filter_by(muscle_group='Chest').all()
    back_exercises = Exercise.query.filter_by(muscle_group='Back').all()
    biceps_exercises = Exercise.query.filter_by(muscle_group='Biceps').all()
    legs_exercises = Exercise.query.filter_by(muscle_group='Legs').all()
    calves_exercises = Exercise.query.filter_by(muscle_group='Calves').all()

    plan = {}
    plan['Legs'] = random.sample(legs_exercises, min(4, len(legs_exercises))) + \
                   random.sample(calves_exercises, min(1, len(calves_exercises)))
    plan['Chest'] = random.sample(chest_exercises, min(5, len(chest_exercises)))
    plan['Back'] = random.sample(back_exercises, min(5, len(back_exercises)))
    plan['Arms'] = random.sample(biceps_exercises, min(2, len(biceps_exercises)))

    return plan

def generate_fbw_plan():
    chest_exercises = Exercise.query.filter_by(muscle_group='Chest').all()
    back_exercises = Exercise.query.filter_by(muscle_group='Back').all()
    legs_exercises = Exercise.query.filter_by(muscle_group='Legs').all()

    plan = {}
    plan['Day A'] = random.sample(chest_exercises, min(1, len(chest_exercises))) + \
                    random.sample(back_exercises, min(1, len(back_exercises))) + \
                    random.sample(legs_exercises, min(1, len(legs_exercises)))
    plan['Day B'] = random.sample(chest_exercises, min(1, len(chest_exercises))) + \
                    random.sample(back_exercises, min(1, len(back_exercises))) + \
                    random.sample(legs_exercises, min(1, len(legs_exercises)))
    
    return plan

if __name__ == "__main__":
    app.run(debug=True)