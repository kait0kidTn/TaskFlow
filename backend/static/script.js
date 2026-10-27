const API = "/api/tasks";

const form = document.getElementById("task-form");
const taskId = document.getElementById("task-id");
const titleInput = document.getElementById("title");
const descriptionInput = document.getElementById("description");
const priorityInput = document.getElementById("priority");
const dueDateInput = document.getElementById("due-date");
const taskList = document.getElementById("task-list");
const message = document.getElementById("message");
const saveButton = document.getElementById("save-button");
const cancelButton = document.getElementById("cancel-button");
const filterInput = document.getElementById("filter");

let tasks = [];

document.getElementById("today").textContent = new Date().toLocaleDateString(
  undefined,
  {
    weekday: "short",
    month: "short",
    day: "numeric",
    year: "numeric",
  },
);

async function request(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || `Request failed (${response.status})`);
  }
  return data;
}

function showMessage(text, isError = false) {
  message.textContent = text;
  message.style.color = isError ? "#fda4af" : "#c4b5fd";
}

async function loadTasks() {
  taskList.innerHTML = '<p class="muted">Loading tasks...</p>';

  try {
    tasks = await request(API);
    renderTasks();
  } catch (error) {
    taskList.textContent =
      "Could not load tasks. Check that Flask and MySQL are running.";
    showMessage(error.message, true);
  }
}

function renderTasks() {
  document.getElementById("total-count").textContent = tasks.length;
  document.getElementById("progress-count").textContent = tasks.filter(
    (task) => task.status === "In Progress",
  ).length;
  document.getElementById("done-count").textContent = tasks.filter(
    (task) => task.status === "Done",
  ).length;

  const selected = filterInput.value;
  const visibleTasks = tasks.filter(
    (task) => selected === "All" || task.status === selected,
  );

  taskList.replaceChildren();

  if (visibleTasks.length === 0) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "No tasks here yet. Add one above!";
    taskList.appendChild(empty);
    return;
  }

  visibleTasks.forEach((task) => {
    const card = document.createElement("article");
    card.className = "task-card";

    const main = document.createElement("div");
    main.className = "task-main";

    const heading = document.createElement("div");
    heading.className = "task-title";
    heading.textContent = task.title;
    main.appendChild(heading);

    if (task.description) {
      const description = document.createElement("p");
      description.className = "task-description";
      description.textContent = task.description;
      main.appendChild(description);
    }

    const meta = document.createElement("div");
    meta.className = "task-meta";

    const priority = document.createElement("span");
    priority.className = "tag priority-" + task.priority.toLowerCase();
    priority.textContent = task.priority + " priority";
    meta.appendChild(priority);

    const status = document.createElement("span");
    status.className = "tag";
    status.textContent = task.status;
    meta.appendChild(status);

    if (task.due_date) {
      const due = document.createElement("span");
      due.className = "tag";
      due.textContent = "Due: " + task.due_date;
      meta.appendChild(due);
    }

    main.appendChild(meta);

    const actions = document.createElement("div");
    actions.className = "task-actions";

    const statusButton = document.createElement("button");
    statusButton.className = "secondary";
    statusButton.textContent =
      task.status === "Done" ? "Reopen" : "Next status";
    statusButton.addEventListener("click", () => advanceTask(task));

    const editButton = document.createElement("button");
    editButton.className = "secondary";
    editButton.textContent = "Edit";
    editButton.addEventListener("click", () => startEdit(task));

    const deleteButton = document.createElement("button");
    deleteButton.className = "danger";
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", () => deleteTask(task));

    actions.append(statusButton, editButton, deleteButton);
    card.append(main, actions);
    taskList.appendChild(card);
  });
}

function startEdit(task) {
  taskId.value = task.id;
  titleInput.value = task.title;
  descriptionInput.value = task.description || "";
  priorityInput.value = task.priority;
  dueDateInput.value = task.due_date || "";

  document.getElementById("form-title").textContent = "Edit task";
  saveButton.textContent = "Save changes";
  cancelButton.classList.remove("hidden");
  titleInput.focus();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function resetForm() {
  form.reset();
  taskId.value = "";
  priorityInput.value = "Medium";
  document.getElementById("form-title").textContent = "Create a task";
  saveButton.textContent = "Add task";
  cancelButton.classList.add("hidden");
}

cancelButton.addEventListener("click", () => {
  resetForm();
  showMessage("");
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const id = taskId.value;
  const payload = {
    title: titleInput.value.trim(),
    description: descriptionInput.value.trim(),
    priority: priorityInput.value,
    due_date: dueDateInput.value || null,
  };

  if (!payload.title) {
    showMessage("Please enter a task title.", true);
    return;
  }

  saveButton.disabled = true;

  try {
    if (id) {
      await request(`${API}/${id}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
      showMessage("Task updated successfully.");
    } else {
      await request(API, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      showMessage("Task created successfully.");
    }

    resetForm();
    await loadTasks();
  } catch (error) {
    showMessage(error.message, true);
  } finally {
    saveButton.disabled = false;
  }
});

async function advanceTask(task) {
  const nextStatus = {
    "To Do": "In Progress",
    "In Progress": "Done",
    Done: "To Do",
  };

  try {
    await request(`${API}/${task.id}`, {
      method: "PUT",
      body: JSON.stringify({ status: nextStatus[task.status] }),
    });
    showMessage("Task status updated.");
    await loadTasks();
  } catch (error) {
    showMessage(error.message, true);
  }
}

async function deleteTask(task) {
  if (!confirm(`Delete "${task.title}"?`)) return;

  try {
    await request(`${API}/${task.id}`, { method: "DELETE" });
    showMessage("Task deleted.");
    await loadTasks();
  } catch (error) {
    showMessage(error.message, true);
  }
}

filterInput.addEventListener("change", renderTasks);

loadTasks();
