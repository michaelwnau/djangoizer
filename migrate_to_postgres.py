import os
import sys
import subprocess
from getpass import getpass

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def create_migration_files():
    subprocess.run(["python", "manage.py", "makemigrations"])

def migrate_database():
    subprocess.run(["python", "manage.py", "migrate"])

def modify_settings(database_settings):
    with open("settings.py", "a") as f:
        f.write("\n")
        f.write("DATABASES = {\n")
        f.write("    'default': {\n")
        for key, value in database_settings.items():
            f.write(f"        '{key}': '{value}',\n")
        f.write("    }\n")
        f.write("}\n")

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_name.settings")
    
    try:
        import django
        django.setup()
    except ImportError:
        print("Django is not installed. Please install Django and try again.")
        sys.exit(1)
    
    try:
        import psycopg2
    except ImportError:
        print("psycopg2-binary is not installed. Installing...")
        install_package("psycopg2-binary")
        import psycopg2

    print("Generating migration files...")
    create_migration_files()

    db_name = input("Enter the new PostgreSQL database name: ")
    user = input("Enter the PostgreSQL user: ")
    password = getpass("Enter the PostgreSQL user's password: ")
    host = input("Enter the PostgreSQL host (default: 'localhost'): ") or "localhost"
    port = input("Enter the PostgreSQL port (default: 5432): ") or 5432

    database_settings = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": db_name,
        "USER": user,
        "PASSWORD": password,
        "HOST": host,
        "PORT": port,
    }

    print("Updating settings.py with new database settings...")
    modify_settings(database_settings)

    print("Migrating the database...")
    migrate_database()

    print("Database migration completed. Please check your new PostgreSQL database to confirm the migration.")

if __name__ == "__main__":
    main()
