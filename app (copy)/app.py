from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os ,sys

import sqlite3
import hashlib


class DatabaseManager:
    def __init__(self, db_name='taskit.db'):
        """
        Initialize the database connection and create tables if they don't exist
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.create_tables()

    def _connect(self):
        """
        Establish a connection to the SQLite database
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def _close(self):
        """
        Close the database connection
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def create_tables(self):
        """
        Create necessary tables if they don't exist
        """
        self._connect()
        
        # Create users table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        
        # Create tasks table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            title TEXT NOT NULL,
            description TEXT,
            column_name TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        ''')
        
        self.conn.commit()
        self._close()

    def generate_user_id(self, username, email):
        """
        Generate a unique user ID using username and email
        """
        # Create a hash using username and email
        user_id = hashlib.sha256(f"{username}:{email}".encode()).hexdigest()
        return user_id

    def register_user(self, username, email, password):
        """
        Register a new user
        """
        self._connect()
        
        # Generate user ID
        user_id = self.generate_user_id(username, email)
        
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            # Check if user already exists
            self.cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            if self.cursor.fetchone():
                self._close()
                return False, "User already exists"
            
            # Insert new user
            self.cursor.execute('''
            INSERT INTO users (user_id, username, email, password) 
            VALUES (?, ?, ?, ?)
            ''', (user_id, username, email, hashed_password))
            
            self.conn.commit()
            self._close()
            return True, user_id
        except sqlite3.Error as e:
            self._close()
            return False, str(e)

    def login_user(self, email, password):
        """
        Authenticate user login
        """
        self._connect()
        
        # Hash the provided password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            # Check credentials
            self.cursor.execute('''
            SELECT user_id, username FROM users 
            WHERE email = ? AND password = ?
            ''', (email, hashed_password))
            
            user = self.cursor.fetchone()
            self._close()
            
            return (True, user[0], user[1]) if user else (False, None, None)
        except sqlite3.Error as e:
            self._close()
            return False, None, str(e)

    def add_task(self, user_id, title, description, column_name):
        """
        Add a new task for a user
        """
        self._connect()
        
        try:
            # Insert new task
            self.cursor.execute('''
            INSERT INTO tasks (user_id, title, description, column_name) 
            VALUES (?, ?, ?, ?)
            ''', (user_id, title, description, column_name))
            
            task_id = self.cursor.lastrowid
            self.conn.commit()
            self._close()
            return True, task_id
        except sqlite3.Error as e:
            self._close()
            return False, str(e)

    def get_tasks(self, user_id, column_name=None):
        """
        Retrieve tasks for a user, optionally filtered by column
        """
        self._connect()
        
        try:
            if column_name:
                self.cursor.execute('''
                SELECT task_id, title, description, column_name 
                FROM tasks 
                WHERE user_id = ? AND column_name = ?
                ''', (user_id, column_name))
            else:
                self.cursor.execute('''
                SELECT task_id, title, description, column_name 
                FROM tasks 
                WHERE user_id = ?
                ''', (user_id,))
            
            tasks = self.cursor.fetchall()
            self._close()
            return tasks
        except sqlite3.Error as e:
            self._close()
            return []

    def delete_task(self, task_id, user_id):
        """
        Delete a specific task for a user
        """
        self._connect()
        
        try:
            # Delete task, ensuring it belongs to the user
            self.cursor.execute('''
            DELETE FROM tasks 
            WHERE task_id = ? AND user_id = ?
            ''', (task_id, user_id))
            
            self.conn.commit()
            deleted_count = self.cursor.rowcount
            self._close()
            return deleted_count > 0
        except sqlite3.Error as e:
            self._close()
            return False

    def update_task(self, task_id, user_id, new_title=None, new_description=None, new_column=None):
        """
        Update a specific task for a user
        """
        self._connect()
        
        try:
            # Prepare update query based on provided parameters
            update_fields = []
            params = []
            
            if new_title:
                update_fields.append("title = ?")
                params.append(new_title)
            
            if new_description:
                update_fields.append("description = ?")
                params.append(new_description)
            
            if new_column:
                update_fields.append("column_name = ?")
                params.append(new_column)
            
            # Add user_id to params
            params.append(user_id)
            params.append(task_id)
            
            if update_fields:
                query = f'''
                UPDATE tasks 
                SET {", ".join(update_fields)}
                WHERE user_id = ? AND task_id = ?
                '''
                
                self.cursor.execute(query, params)
                self.conn.commit()
                updated_count = self.cursor.rowcount
                self._close()
                return updated_count > 0
            
            self._close()
            return False
        except sqlite3.Error as e:
            self._close()
            return False


app = Flask(__name__)
# Set a secret key for session management
app.secret_key = os.urandom(24)

# Initialize database manager
db_manager = DatabaseManager()

@app.route('/')
def home():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Fetch tasks for the logged-in user
    tasks_today = db_manager.get_tasks(session['user_id'], 'Today')
    tasks_tomorrow = db_manager.get_tasks(session['user_id'], 'Tomorrow')
    tasks_overdue = db_manager.get_tasks(session['user_id'], 'Over-due')
    
    return render_template('yeh.html', 
                           username=session['username'], 
                           tasks_today=tasks_today,
                           tasks_tomorrow=tasks_tomorrow,
                           tasks_overdue=tasks_overdue)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return render_template('login.html', error='Email and password are required')

        success, user_id, username = db_manager.login_user(email, password)

        if success:
            session['user_id'] = user_id
            session['username'] = username

            # Fetch tasks for the logged-in user
            tasks_today = db_manager.get_tasks(user_id, 'Today')
            tasks_tomorrow = db_manager.get_tasks(user_id, 'Tomorrow')
            tasks_overdue = db_manager.get_tasks(user_id, 'Over-due')

            return render_template('yeh.html',
                                   username=username,
                                   tasks_today=tasks_today,
                                   tasks_tomorrow=tasks_tomorrow,
                                   tasks_overdue=tasks_overdue)
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')





@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        success, result = db_manager.register_user(username, email, password)
        
        if success:
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error=result)
    
    return render_template('register.html')




@app.route('/add_task', methods=['POST'])
def add_task():
    # Check if user is logged in
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})

    title = request.form.get('title')
    description = request.form.get('description', '')
    column_name = request.form.get('column')

    print(f"Adding task - User: {session['user_id']}, Title: {title}, Column: {column_name}")

    try:
        success, task_id = db_manager.add_task(
            session['user_id'],
            title,
            description,
            column_name
        )
        print(f"Task Add Result: {success}, Task ID: {task_id}")

        # Redirect to the home route after successful task addition
        if success:
            return redirect(url_for('home'))
        else:
            return jsonify({'success': False, 'message': 'Failed to add task'})
    except Exception as e:
        print(f"Error adding task: {e}")
        return jsonify({'success': False, 'message': 'Failed to add task due to an error'})


@app.route('/delete_task', methods=['POST'])
def delete_task():
    # Check if user is logged in
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    task_id = request.form.get('task_id')
    
    success = db_manager.delete_task(task_id, session['user_id'])
    
    return jsonify({
        'success': success,
        'message': 'Task deleted successfully' if success else 'Failed to delete task'
    })


if __name__ == '__main__':
    app.run(debug=True)