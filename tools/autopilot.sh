#!/usr/bin/env bash

set -euo pipefail

echo "📖 This script will help you running SKELETON for the first time. It will try to setup everything"
echo "with default values so you can run it directly."

if [ ! -f ~/.auth.toml ] ; then
  echo "⚠️  Poetry needs a auth.toml file to install private dependencies inside a docker container."
  echo "Please create the auth.toml file in the home directory with the following content:"
  echo ""
  echo "[http-basic.git-minvws-gfmodules-python-shared]"
  echo "username = github-username"
  echo "password = github-personal-access-token"
  echo ""
  exit;
fi

cp ~/.auth.toml auth.toml

# Check if we already are configured
if [ -e .autopilot ] ; then
    echo "⚠️ It seems that you already ran this script. If you want to run it again, please remove the .autopilot file."
    exit;
fi

# Create postgres database within docker
echo "➡️ Firing up postgres database in a docker container"
if
    docker compose version
    [ $? -eq 1 ] ; then
    echo "⚠️ Docker compose is not a valid command. Perhaps you are running on a old docker version (needs v2 or higher)."
    exit;
fi
docker compose up qualification_db -d

# Generate TLS certificates (they are not used in the default configuration)
echo "➡️ Generating TLS certificates"
if [ -e secrets/ssl/server.key ] && [ -e secrets/ssl/server.cert ]; then
    echo "⚠️ TLS certificates already exist. Skipping."
else
    ./tools/generate_certs.sh
fi

# Create the configuration file
echo "➡️ Creating the configuration file"
if [ -e app.conf ]; then
    echo "⚠️ Configuration file already exists. Skipping."
else
    cp app.conf.autopilot app.conf
fi

# Build the application docker container
echo "➡️ Building the application docker container"
make container-build GIT_USER="${GIT_USER}" GIT_PAT="${GIT_PAT}"

# Run the container
echo "➡️ Running the application docker container"
docker compose up app -d

# Create the .autopilot file
touch .autopilot

echo "🏁 Autopilot completed. You should be able to go to your web browser and access the application at http://localhost:8506/docs."
