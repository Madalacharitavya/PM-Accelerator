## PM Acceleratr

**Weather App** 

### Features

- Add new weather entries
- Edit or delete existing records
- View weather history
- Clean and minimal web interface using HTML/CSS

### Project Structure

```
PM Acceleratr/
├── app.py              # Main Flask application
├── weather.db          # SQLite database
├── static/
│   └── style.css       # Stylesheet
├── templates/
│   ├── index.html      # Home page
│   ├── edit.html       # Edit form
│   └── history.html    # History view
└── venv/               # Virtual environment (optional)
```

### Requirements

- Python 3.8+
- Flask

### Installation

1. Clone the repository or extract the project zip:
   ```bash
   git clone https://github.com/yourusername/PM-Acceleratr.git
   cd PM-Acceleratr
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install Flask
   ```

4. Run the app:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

### License

MIT License

