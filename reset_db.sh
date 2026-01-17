#!/bin/bash
# reset_db.sh - Completely resets the Volunteer Connect backend database and migrations

echo "🚀 Starting full reset..."

# 1️⃣ Delete old database and migrations
echo "Deleting old database and migrations..."
rm -f volunteer.db
rm -rf migrations
find . -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -exec rm -f {} +

# 2️⃣ Ensure dependencies are installed/upgraded
echo "Installing/upgrading dependencies..."
pip install --upgrade Flask-SQLAlchemy Flask-Migrate alembic

# 3️⃣ Initialize new migrations
echo "Initializing new migrations..."
flask db init

# 4️⃣ Create initial migration
echo "Generating initial migration..."
flask db migrate -m "Initial migration"

# 5️⃣ Apply migration (create tables)
echo "Applying migration..."
flask db upgrade

# 6️⃣ Seed the database
echo "Seeding database..."
python seed.py

echo "✅ Reset complete! Database and migrations are fresh."
