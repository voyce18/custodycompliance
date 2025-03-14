from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os

# Create Flask app
app = Flask(__name__)
app.secret_key = '8775ea1ba1bb438aef3c6bebcf370446e7e254da9a2aa4f7cbabc3db5344c760'

# Create upload folder if it doesn't exist
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Basic user data (replace with database in production)
users = {
    "admin@myyouthhaven.com": {"password": "Bruton20!", "role": "admin"},
    "attorney@example.com": {"password": "password123", "role": "attorney"},
    "parent@example.com": {"password": "password123", "role": "parent"},
    "court@example.com": {"password": "password123", "role": "court"}
}

# Route for the home page
@app.route('/')
def index():
    return redirect(url_for('custody_monitor'))

@app.route('/custody-monitor')
def custody_monitor():
    """Serve the AI-Based Child Custody Compliance Monitor landing page"""
    return render_template('custody-compliance-monitor.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in users and users[email]["password"] == password:
            session['email'] = email
            session['role'] = users[email]["role"]
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('custody_monitor'))

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))
    
    role = session.get('role')
    return render_template('dashboard.html', role=role)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # In a real app, you would process and save this message
        flash('Your message has been sent. We will get back to you soon!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

# Route that handles file uploads for facial recognition
@app.route('/upload-face', methods=['POST'])
def upload_face():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)
        # In a real app, you would process the image for facial recognition here
        return jsonify({'success': True, 'filename': file.filename})

# API endpoint to check custody compliance
@app.route('/api/check-compliance', methods=['POST'])
def check_compliance():
    data = request.json
    
    # In a real app, you would verify the check-in with your AI system
    # For now, we'll just return a mock success response
    return jsonify({
        'success': True,
        'verified': True,
        'timestamp': '2025-03-13T14:30:00Z',
        'location': 'Verified',
        'compliance_status': 'On Time'
    })

# Route for pricing page
@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

# Route for features page
@app.route('/features')
def features():
    return render_template('features.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)