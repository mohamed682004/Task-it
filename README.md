# Task Management Application

This is a simple yet effective web-based task management application that allows users to manage their daily tasks. Users can add tasks, categorize them into "Today," "Tomorrow," and "Overdue" columns, and remove tasks as needed. The application uses **Flask** as the backend framework and **SQLite** as the database for storing user tasks.

## Features

- **User Authentication**: Users need to log in to add, remove, and manage tasks.
- **Task Categorization**: Tasks are categorized into three main columns: Today, Tomorrow, and Overdue.
- **Add Tasks**: Users can add tasks with a title and optional description.
- **Delete Tasks**: Users can remove tasks they no longer need.
- **Dynamic Task Count**: Each column dynamically displays the count of tasks it contains.

## Technologies Used

- **Frontend**:
  - HTML
  - CSS
  - JavaScript (for task interaction)
  
- **Backend**:
  - Flask (Python web framework)
  - SQLite (for task data storage)
  
## Getting Started

### Prerequisites

- Python 3.x
- Flask
- SQLite

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/task-management-app.git
   cd task-management-app
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:

   Run the following command to set up the database:

   ```bash
   python init_db.py
   ```

   This will create the necessary tables in the SQLite database.

5. Run the Flask application:

   ```bash
   flask run
   ```

   The application will be available at `http://127.0.0.1:5000`.

## Usage

### Login
To interact with the application, users must log in. After logging in, users can:

- **Add a task**: Click the "+" button in any of the columns (Today, Tomorrow, Overdue) to add a new task. Each task includes a title and optional description.
  
- **Delete a task**: Each task has a "Remove" button. Clicking this button will delete the task from the column.

### Task Columns
Tasks are categorized into three columns:

- **Today**: Tasks to be completed today.
- **Tomorrow**: Tasks to be completed the next day.
- **Overdue**: Tasks that are past their due date.

### Dynamic Updates
- The number of tasks in each column is displayed dynamically.
- After adding or deleting a task, the task count will automatically update.

## Example

Here’s a quick look at the structure of the task grid:

```
+------------------+-------------------+--------------------+
|     Today        |    Tomorrow       |      Overdue       |
+------------------+-------------------+--------------------+
| Task 1           | Task A            | Task X             |
| Task 2           | Task B            | Task Y             |
| Task 3           |                   | Task Z             |
+------------------+-------------------+--------------------+
```

Each task has a title, description, and a "Remove" button to delete it.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository, make improvements, and submit a pull request. Contributions are always welcome!

### Issues and Bugs

If you encounter any issues or bugs, please open an issue on GitHub with a detailed description of the problem. I'll be happy to assist with troubleshooting.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
