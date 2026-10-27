from flask import Flask, request ,send_from_directory
from db import get_db_connection


def create_app(testing=False):
    app = Flask(__name__)
    app.config["TESTING"] = testing
    @app.route("/app")
    def frontend():
        return send_from_directory("static", "index.html")
   

    @app.route("/")
    def home():
        return {"message": "TaskFlow API is running"}

    @app.route("/api/tasks", methods=["GET"])
    def get_tasks():
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT id, title, description, priority,
                       status, due_date, created_at
                FROM tasks
                ORDER BY id DESC
                """
            )
            tasks = cursor.fetchall()

            for task in tasks:
                if task["due_date"]:
                    task["due_date"] = task["due_date"].isoformat()
                if task["created_at"]:
                    task["created_at"] = task["created_at"].isoformat()

            return tasks
        finally:
            cursor.close()
            connection.close()

    @app.route("/api/tasks", methods=["POST"])
    def create_task():
        data = request.get_json(silent=True) or {}

        title = data.get("title")
        if not isinstance(title, str) or not title.strip():
            return {"error": "Title is required"}, 400

        priority = data.get("priority", "Medium")
        if priority not in ("Low", "Medium", "High"):
            return {"error": "Invalid priority"}, 400

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                INSERT INTO tasks (title, description, priority, status, due_date)
                VALUES (%s, %s, %s, 'To Do', %s)
                """,
                (
                    title.strip(),
                    data.get("description", ""),
                    priority,
                    data.get("due_date") or None,
                ),
            )
            connection.commit()
            task_id = cursor.lastrowid

            cursor.execute(
                """
                SELECT id, title, description, priority,
                       status, due_date, created_at
                FROM tasks WHERE id = %s
                """,
                (task_id,),
            )
            task = cursor.fetchone()

            if task["due_date"]:
                task["due_date"] = task["due_date"].isoformat()
            if task["created_at"]:
                task["created_at"] = task["created_at"].isoformat()

            return task, 201
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()
    @app.route("/api/tasks/<int:task_id>", methods=["PUT"])
    def update_task(task_id):
        data = request.get_json(silent=True) or {}

        allowed_fields = {
            "title", "description", "priority", "status", "due_date"
        }

        if not data or not set(data).issubset(allowed_fields):
            return {"error": "Invalid task data"}, 400

        if "title" in data:
            if not isinstance(data["title"], str) or not data["title"].strip():
                return {"error": "Title cannot be empty"}, 400

        if "priority" in data and data["priority"] not in (
            "Low", "Medium", "High"
        ):
            return {"error": "Invalid priority"}, 400

        if "status" in data and data["status"] not in (
            "To Do", "In Progress", "Done"
        ):
            return {"error": "Invalid status"}, 400

        fields = list(data.keys())
        values = [
            data[field].strip() if field == "title" else data[field]
            for field in fields
        ]

        assignments = ", ".join(f"{field} = %s" for field in fields)
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                f"UPDATE tasks SET {assignments} WHERE id = %s",
                (*values, task_id),
            )

            if cursor.rowcount == 0:
                connection.rollback()
                return {"error": "Task not found"}, 404

            connection.commit()
            return {"message": "Task updated successfully"}
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    @app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
    def delete_task(task_id):
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "DELETE FROM tasks WHERE id = %s", (task_id,)
            )

            if cursor.rowcount == 0:
                connection.rollback()
                return {"error": "Task not found"}, 404

            connection.commit()
            return {"message": "Task deleted successfully"}
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()   
    return app





if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)