function start() {
    echo "Pulling latest version from Git..."
    git pull
    if [[ "$OSTYPE" == "msys"* ]]; then
        echo "Updating python requirements..."
        python -m pip install -e .
        echo "Opening game..."
        python main.py
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Updating python requirements..."
        python3 -m pip install -e .
        echo "Opening game..."
        python3 main.py
    fi
}

if [[ "$1" == "--debug" ]]; then
    start
else
    garbage_variable_to_hide_output=$(start)
fi
