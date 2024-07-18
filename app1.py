from flask import Flask, render_template, request, redirect, url_for



app1 = Flask(__name__)

@app1.route('/')

def index():
    return render_template('index1.html')


# @app1.route('/')
# def index():
#     return redirect(url_for('signup.html'))

# @app1.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         # Here, you would typically handle the signup logic, such as saving the user data to a database
#         return redirect(url_for('thank_you'))
#     return render_template('signup.html')

# @app1.route('/thank_you')
# def thank_you():
#     return "Thank you for signing up!"

if __name__ == '__main__':
    app1.run(debug=True)