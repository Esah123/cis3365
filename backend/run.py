import os
from app import create_app, db
from flask import current_app
from flask import Flask, render_template, send_from_directory

# Print the current working directory
print("Current Working Directory:", os.getcwd())

app = create_app()

with app.app_context():
    for rule in app.url_map.iter_rules():
        methods = ', '.join(sorted(rule.methods - set(['HEAD', 'OPTIONS'])))
        print(f"{rule.endpoint}: {methods}")

@app.route('/test-css')
def test_css():
    # Construct an absolute path to the stylesheet
    stylesheet_path = os.path.abspath(os.path.join(app.static_folder, 'styles.css'))
    print(f"Serving stylesheet from: {stylesheet_path}")  # Debugging print statement
    directory = os.path.dirname(stylesheet_path)
    filename = os.path.basename(stylesheet_path)
    return send_from_directory(directory, filename)

@app.route('/')
def home():
    frontend_dir = os.path.abspath('../frontend')
    return send_from_directory(frontend_dir, 'index.html')

if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5000, debug=True)