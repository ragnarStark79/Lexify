from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_bcrypt import Bcrypt # Import Bcrypt
from functools import wraps # For login_required decorator
from enhancer import get_text_enhancer
from database import get_db_handler
import config
import time

app = Flask(__name__, static_url_path='/static')
app.secret_key = config.SECRET_KEY # Set secret key for sessions
bcrypt = Bcrypt(app) # Initialize Bcrypt

enhancer = get_text_enhancer()
db = get_db_handler()

# Decorator to require login for certain routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('enhancer_page')) # Redirect logged-in users to enhancer
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db.find_user_by_email(email)
        
        # Check if user exists AND has a password field before checking hash
        if user and 'password' in user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id']) # Store user ID in session
            session['user_name'] = user['name'] # Store user name in session
            flash(f"Welcome back, {user['name']}!", 'success') # Use name in flash
            return redirect(url_for('enhancer_page'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
            
    # If GET request or login failed, show login page
    if 'user_id' in session:
         return redirect(url_for('enhancer_page')) # Don't show login if already logged in
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name'] # Get name from form
        email = request.form['email']
        password = request.form['password']
        
        existing_user = db.find_user_by_email(email)
        if existing_user:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('login'))
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_id = db.add_user(name, email, hashed_password) # Pass name to add_user
        
        if user_id:
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error creating account. Please try again.', 'danger')
            
    # If GET request or signup failed, show signup page
    if 'user_id' in session:
         return redirect(url_for('enhancer_page')) # Don't show signup if already logged in
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None) # Remove user_name from session
    session.pop('user_email', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index')) # Redirect to index page

@app.route('/enhancer')
@login_required # Protect this route
def enhancer_page():
    return render_template('enhancer.html')

@app.route('/enhance', methods=['POST'])
@login_required # Also protect the API endpoint
def enhance_text():
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    input_text = data['text']
    user_id = session.get('user_id') # Get user_id from session
    
    try:
        enhanced_text, duration = enhancer.enhance_text(input_text)
        
        db.log_interaction(
            original_text=input_text,
            enhanced_text=enhanced_text,
            model_name=enhancer.model_name,
            user_feedback=None,
            user_id=user_id # Pass user_id to log
        )
        
        return jsonify({'enhanced_text': enhanced_text, 'duration': duration})
    except Exception as e:
        return jsonify({'error': str(e), 'duration': None}), 500

@app.route('/feedback', methods=['POST'])
def record_feedback():
    data = request.get_json()
    
    if not data or 'feedback' not in data or 'interactionId' not in data:
        return jsonify({'error': 'Invalid feedback data'}), 400
    
    # Here you would update the MongoDB record with the feedback
    # This is a placeholder for actual feedback implementation
    
    return jsonify({'success': True})

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session['user_id']
    user = db.find_user_by_id(user_id)

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('logout'))

    if request.method == 'POST':
        new_name = request.form['name']
        new_email = request.form['email']

        # Basic validation
        if not new_name or not new_email:
            flash('Name and email cannot be empty.', 'warning')
        elif new_name == user['name'] and new_email == user['email']:
            flash('No changes detected.', 'info')
        else:
            success = db.update_user_profile(user_id, new_name, new_email)
            if success:
                session['user_name'] = new_name # Update session name if changed
                flash('Profile updated successfully!', 'success')
                # Re-fetch user data after update to display the latest info
                user = db.find_user_by_id(user_id) 
            else:
                # Check if the email was the issue (update_user_profile returns False if email exists)
                if db.find_user_by_email(new_email) and new_email != user['email']:
                     flash('Email already in use by another account.', 'danger')
                else:
                    flash('Error updating profile. Please try again.', 'danger')

    # Pass user data (including registration date) to the template
    return render_template('profile.html', user=user)

def run_webapp(debug=False, port=5000):
    app.run(debug=debug, port=port)

if __name__ == '__main__':
    run_webapp(debug=True)
