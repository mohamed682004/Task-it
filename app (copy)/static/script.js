document.addEventListener("DOMContentLoaded", () => {
  ///////////////////////////////////////////////////////////////////////////
  // Date Initialization
  const today = new Date();
  const day = today.getDate();
  const month = today.toLocaleString("default", { month: "long" });
  const year = today.getFullYear();
  const daysOfWeek = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
  ];
  const dayOfWeek = daysOfWeek[today.getDay()];
  const formattedDate = `${month} ${day}, ${year}`;

  // Update date and day in the DOM
  document.getElementById("current-day").textContent = dayOfWeek;
  document.getElementById("current-date").textContent = formattedDate;

  ///////////////////////////////////////////////////////////////////////////
  // Utility Functions

  // Updates task counters for each column
  function updateCounters() {
    document.getElementById(
      "today-counter"
    ).textContent = `(${countTasksForColumn("Today")})`;
    document.getElementById(
      "tomorrow-counter"
    ).textContent = `(${countTasksForColumn("Tomorrow")})`;
    document.getElementById(
      "overdue-counter"
    ).textContent = `(${countTasksForColumn("Over-due")})`;
  }

  // Counts tasks for a given column based on its title
  function countTasksForColumn(columnTitle) {
    const taskContainer = document.querySelector(
      `#${columnTitle.toLowerCase()}-tasks`
    );
    return taskContainer ? taskContainer.querySelectorAll(".task-card").length : 0;
  }

  ///////////////////////////////////////////////////////////////////////////
  // Modal and Task Logic

  const modal = document.getElementById("task-modal");
  const taskForm = document.getElementById("task-form");
  const addTaskButtons = document.querySelectorAll(".add-task-button");
  const cancelTaskButton = document.getElementById("cancel-task");
  const titleInput = document.getElementById("task-title");
  const descriptionInput = document.getElementById("task-description");

  // Open the modal for adding a task
  addTaskButtons.forEach((button) => {
    button.addEventListener("click", () => {
      modal.style.display = "block";
      const columnTitle = button.dataset.column;
      modal.dataset.column = columnTitle;
      document.getElementById("task-column").value = columnTitle; // Set the hidden input value
    });
  });

  // Close the modal and reset the form
  cancelTaskButton.addEventListener("click", () => {
    modal.style.display = "none";
    taskForm.reset();
  });

  // Event delegation for delete buttons (to handle both existing and dynamically added tasks)
  document.querySelector(".grid").addEventListener("click", (event) => {
    const deleteButton = event.target.closest(".delete-task-button");
    if (deleteButton) {
      const taskCard = deleteButton.closest(".task-card");
      const taskId = deleteButton.dataset.taskId;

      // Send a request to delete the task from the backend
      fetch(`/delete_task`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          task_id: taskId,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            taskCard.remove();
            updateCounters();
          } else {
            alert("Failed to delete task.");
          }
        })
        .catch(() => alert("Error occurred while deleting the task."));
    }
  });

  // Save the task
  taskForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const taskTitle = titleInput.value.trim();
    const taskDescription = descriptionInput.value.trim();
    const columnDay = modal.dataset.column;
    const taskContainer = document.getElementById(
      `${columnDay.toLowerCase()}-tasks`
    );

    if (!taskTitle) {
      alert("Task title cannot be empty.");
      return;
    }

    // Check for duplicate task names
    const existingTasks = taskContainer.querySelectorAll(".task-title");
    const duplicate = Array.from(existingTasks).some(
      (task) => task.textContent.toLowerCase() === taskTitle.toLowerCase()
    );

    if (duplicate) {
      alert("Task name already exists. Please choose a different name.");
      return;
    }

    // Close modal and reset the form
    modal.style.display = "none";
    taskForm.reset();

    // Update counters
    updateCounters();
  });

  // Close the modal when clicking outside of it
  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      modal.style.display = "none";
      taskForm.reset();
    }
  });

  ///////////////////////////////////////////////////////////////////////////
  // Initial Counter Update
  updateCounters();
});