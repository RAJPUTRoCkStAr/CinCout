

# from flask import Flask, render_template, request, redirect, url_for

# app = Flask(__name__)

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         # Here, you would typically handle form submission,
#         # e.g., save to a database or perform validation.
#         # For now, we'll just redirect to the success page.
#         return redirect(url_for('success'))  # Redirect to the success page.
#     return render_template('signup.html')

# @app.route('/')
# def home():
#     return redirect(url_for('signup'))

# @app.route('/success')
# def success():
#     return render_template('main.html')  # Renders main.html after successful signup.

# if __name__ == '__main__':
#     app.run(debug=True)
# from flask import Flask, render_template, request, redirect, url_for, session
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Replace with a real secret key

# # Simulated database for demonstration purposes
# users_db = {}

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         hashed_password = generate_password_hash(password, method='sha256')

#         if username in users_db:
#             return "User already exists! Please log in."

#         users_db[username] = {'email': email, 'password': hashed_password}
#         return redirect(url_for('login'))
#     return render_template('signup.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         user = users_db.get(username)
#         if user and check_password_hash(user['password'], password):
#             session['username'] = username
#             return redirect(url_for('home'))
#         return "Invalid credentials! Please try again."

#     return render_template('main.html')

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('login'))

# @app.route('/')
# def home():
#     if 'username' in session:
#         return render_template('sign.html')
#     return redirect(url_for('login'))

# @app.route('/success')
# def success():
#     if 'username' in session:
#         return render_template('main.html')
#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# Simulated database for demonstration purposes
users_db = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'signup' in request.form:
            return redirect(url_for('signup'))
        elif 'login' in request.form:
            return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        if username in users_db:
            return "User already exists! Please log in."

        users_db[username] = {'email': email, 'password': hashed_password}
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_db.get(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('main'))
        return "Invalid credentials! Please try again."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/main')
def main():
    if 'username' in session:
        return render_template('main.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
