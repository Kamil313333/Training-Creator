from app import db

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