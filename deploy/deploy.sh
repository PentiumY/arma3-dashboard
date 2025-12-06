#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# --------- CONFIGURATION ---------
APP_NAME="arma3-dashboard"
BACKEND_SERVICE="arma3-backend.service"
FRONTEND_SERVICE="arma3-frontend.service"
APP_PATH="/home/arma/$APP_NAME"  # Where the repo will be on the server
PYTHON_VERSION="3.12"
NODE_VERSION="20"
USER="arma"

# --------- FUNCTIONS ---------
install_dependencies() {
    echo "Updating system and installing required packages..."
    sudo apt update
    sudo apt install -y python$PYTHON_VERSION python$PYTHON_VERSION-venv python$PYTHON_VERSION-dev \
                        build-essential curl git nginx
    curl -fsSL https://deb.nodesource.com/setup_$NODE_VERSION.x | sudo -E bash -
    sudo apt install -y nodejs
}

setup_backend() {
    echo "Setting up backend..."
    cd "$APP_PATH/backend"

    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        python$PYTHON_VERSION -m venv venv
    fi

    # Activate and install requirements
    source venv/bin/activate
    pip install --upgrade pip
    if [ -f requirements.txt ]; then
        pip install -r requirements.txt
    fi
    deactivate
}

build_frontend() {
    echo "Building frontend..."
    cd "$APP_PATH/frontend"
    npm install
    npm run build  # assumes your svelte config builds to 'public' or 'build'
}

setup_systemd_service() {
    SERVICE_NAME=$1
    SERVICE_DESC=$2
    SERVICE_CMD=$3

    SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME"

    echo "Creating/updating systemd service: $SERVICE_NAME"

    # Create or replace the systemd service file
    sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=$SERVICE_DESC
After=network.target

[Service]
Type=simple
WorkingDirectory=$APP_PATH
ExecStart=$SERVICE_CMD
Restart=always
RestartSec=5
User=$USER
Environment=PATH=$APP_PATH/backend/venv/bin:/usr/bin:/bin

[Install]
WantedBy=multi-user.target
EOL

    # Reload systemd, enable and restart service
    sudo systemctl daemon-reload
    sudo systemctl enable $SERVICE_NAME
    sudo systemctl restart $SERVICE_NAME
}

# --------- MAIN ---------
echo "Deploying $APP_NAME..."

# 1. Install dependencies
install_dependencies

# 2. Setup backend
setup_backend

# 3. Build frontend
build_frontend

# 4. Setup systemd services
# Backend service
setup_systemd_service "$BACKEND_SERVICE" "Arma3 Dashboard Backend" "$APP_PATH/backend/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000"

# Frontend service (simple static server)
setup_systemd_service "$FRONTEND_SERVICE" "Arma3 Dashboard Frontend" "npx serve -s $APP_PATH/frontend/build -l 3000"

echo "Deployment complete. Services are running."
