import container
import fastapi_application

if __name__ == "__main__":
    fastapi_application.application_init()

    db = container.get_database()
    db.generate_tables()
