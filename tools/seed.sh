#!/usr/bin/env bash

set -e

SCRIPT_PATH=`realpath $0`
DIR_PATH=`dirname $SCRIPT_PATH`
PROJECT_PATH="$DIR_PATH/.."

DB_HOST=${1:-localhost}
DB_USER=${2:-postgres}
DB_PASS=${3:-postgres}
DB_NAME=${4:-postgres}

export PGPASSWORD=$DB_PASS

GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
NC="\033[0m"

shopt -s nullglob

# Execute commands from the project directory
cd $PROJECT_PATH

echo -e "${GREEN}👀 Checking seed migrations for ${BLUE}$DB_NAME${GREEN} on ${BLUE}$DB_HOST${NC}"

# check if the seed_migrations table exists
if
    psql -h $DB_HOST -U $DB_USER -d $DB_NAME -t -c "\dt" | grep 'seed_migrations' > /dev/null
    [ $? -eq 1 ]; then
    echo -e "${YELLOW}⚠️ Seed migration table does not exists. Creating seed migrations table.${NC}"

    # create the seed_migrations table
    echo "CREATE TABLE seed_migrations (id serial PRIMARY KEY, name VARCHAR(255) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);" | psql -h $DB_HOST -U $DB_USER -d $DB_NAME -q -o /dev/null
fi

for file_path in seeds/*.sql; do
    file_name=$(basename $file_path)
    # Check each SQL file to see if it's already in the migrations table
    if psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "SELECT name FROM seed_migrations WHERE name = '$file_name';" | grep -q $file_name; then
        echo -e "${YELLOW}⏩ File $file is already in the seed_migrations table. Skipping.${NC}"
    else
        echo -e "${GREEN}▶️ Running seed_migrations $file_name${NC}"
        psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f $file_path --single-transaction -v ON_ERROR_STOP=1 -q -o /dev/null
        echo "INSERT INTO seed_migrations (name) VALUES ('$file_name');" | psql -h $DB_HOST -U $DB_USER -d $DB_NAME -o /dev/null
    fi
done

for file_path in seeds/*.py; do
    file_name=$(basename $file_path)
    # Check each SQL file to see if it's already in the migrations table
    if psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "SELECT name FROM seed_migrations WHERE name = '$file_name';" | grep -q $file_name; then
        echo -e "${YELLOW}⏩ File $file is already in the seed_migrations table. Skipping.${NC}"
    else
        echo -e "${GREEN}▶️ Running seed_migrations $file_name${NC}"
        python $file_path
        echo "INSERT INTO seed_migrations (name) VALUES ('$file_name');" | psql -h $DB_HOST -U $DB_USER -d $DB_NAME -o /dev/null
    fi
done

shopt -u nullglob
