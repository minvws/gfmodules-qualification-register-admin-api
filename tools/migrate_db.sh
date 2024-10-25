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

# Execute commands from the project directory
cd $PROJECT_PATH

echo -e "${GREEN}👀 Checking migrations for ${BLUE}$DB_NAME${GREEN} on ${BLUE}$DB_HOST${NC}"

# check if the migration table exists
if
    psql -h $DB_HOST -U $DB_USER -d $DB_NAME -t -c "\dt" | grep 'migrations' > /dev/null
    [ $? -eq 1 ]; then
    echo -e "${YELLOW}⚠️ Migration table does not exists. Creating migrations table.${NC}"

    # create the migration table
    echo "CREATE TABLE migrations (id serial PRIMARY KEY, name VARCHAR(255) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);" | psql -h $DB_HOST -U $DB_USER -d $DB_NAME -q -o /dev/null
fi

for file_path in sql/*.sql; do
    file_name=$(basename $file_path)

    # Check each SQL file to see if it's already in the migrations table
    if psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "SELECT name FROM migrations WHERE name = '$file_name';" | grep -q $file_name; then
        echo -e "${YELLOW}⏩ File $file_name is already in the migrations table. Skipping.${NC}"
    else
        echo -e "${GREEN}▶️ Running migration $file_name${NC}"
        psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f $file_path --single-transaction -v ON_ERROR_STOP=1 -q -o /dev/null
        echo "INSERT INTO migrations (name) VALUES ('$file_name');" | psql -h $DB_HOST -U $DB_USER -d $DB_NAME -o /dev/null
    fi
done

