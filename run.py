from app import create_app, db
from flask_migrate import upgrade

app = create_app()

with app.app_context():
    try:
        upgrade()
    except Exception as e:
        print(f"Migration notice: {e}")
        db.create_all()

if __name__ == "__main__":
    app.run()