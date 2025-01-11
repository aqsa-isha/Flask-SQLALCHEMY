from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set up the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object with the app
db = SQLAlchemy(app)

# Model (database table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

# Route: Home Page
@app.route('/')
def index():
    users = User.query.all()  # Retrieve all users from the database
    return render_template('index.html', users=users)

# Route: Add User
@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    new_user = User(name=name, email=email)  # Create a new user object
    db.session.add(new_user)  # Add the new user to the session
    db.session.commit()  # Commit the changes to the database
    return redirect('/')  # Redirect back to the home page

# Create the database and tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
