from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(100))
    experience_level = db.Column(db.String(100))
    available_time = db.Column(db.Integer)
    equipment = db.Column(db.String(100))

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    muscle_group = db.Column(db.String(100))
    equipment_needed = db.Column(db.String(100))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_preferences', methods=['POST'])
def submit_preferences():
    goal = request.form['goal']
    experience_level = request.form['experience_level']
    available_time = request.form['available_time']
    equipment = request.form['equipment']
    
    user_preferences = UserPreferences(goal=goal, experience_level=experience_level, available_time=available_time, equipment=equipment)
    db.session.add(user_preferences)
    db.session.commit()
    
    return redirect(url_for('plan', user_id=user_preferences.id))

@app.route('/plan/<int:user_id>')
def plan(user_id):
    user_preferences = UserPreferences.query.get(user_id)
    exercises = Exercise.query.filter((Exercise.equipment_needed == user_preferences.equipment) | (Exercise.equipment_needed == None)).all()
    
    return render_template('plan.html', exercises=exercises)

if __name__ == '__main__':
    app.run(debug=True)