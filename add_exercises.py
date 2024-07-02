from app import app, db, Exercise

# Definicja nowych ćwiczeń dla barków
shoulder_exercises = [
    {"name": "Shoulder Press", "muscle_group": "Shoulders"},
    {"name": "Lateral Raises", "muscle_group": "Shoulders"},
    {"name": "Front Raises", "muscle_group": "Shoulders"},
    {"name": "Reverse Flyes", "muscle_group": "Shoulders"},
    {"name": "Arnold Press", "muscle_group": "Shoulders"},
]

# Utwórz kontekst aplikacji
with app.app_context():
    # Dodanie ćwiczeń do bazy danych
    for exercise_data in shoulder_exercises:
        exercise = Exercise(name=exercise_data["name"], muscle_group=exercise_data["muscle_group"])
        db.session.add(exercise)

    # Zatwierdzenie zmian w bazie danych
    db.session.commit()

print("Dodano nowe ćwiczenia dla barków do bazy danych.")