import json
import os
from datetime import datetime


class TodoList:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []

    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, description):
        """Add a new task"""
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'completed': False,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"✓ Added task: '{description}'")

    def view_tasks(self):
        """Display all tasks"""
        if not self.tasks:
            print("No tasks in your list!")
            return

        print("\n" + "=" * 50)
        print("YOUR TO-DO LIST")
        print("=" * 50)

        for task in self.tasks:
            status = "✓" if task['completed'] else "○"
            print(f"{status} [{task['id']}] {task['description']}")
            if task['completed']:
                print(f"    Completed: {task.get('completed_at', 'Unknown')}")
            else:
                print(f"    Created: {task['created_at']}")
        print("=" * 50)

    def complete_task(self, task_id):
        """Mark a task as completed"""
        for task in self.tasks:
            if task['id'] == task_id:
                if task['completed']:
                    print(f"Task '{task['description']}' is already completed!")
                else:
                    task['completed'] = True
                    task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.save_tasks()
                    print(f"✓ Completed task: '{task['description']}'")
                return
        print(f"Task with ID {task_id} not found!")

    def delete_task(self, task_id):
        """Delete a task"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                description = task['description']
                self.tasks.pop(i)
                self.save_tasks()
                print(f"✗ Deleted task: '{description}'")
                return
        print(f"Task with ID {task_id} not found!")

    def clear_completed(self):
        """Remove all completed tasks"""
        initial_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if not task['completed']]
        removed_count = initial_count - len(self.tasks)
        self.save_tasks()
        print(f"✗ Removed {removed_count} completed task(s)")


def display_menu():
    """Display the main menu"""
    print("\n" + "=" * 30)
    print("TO-DO LIST MENU")
    print("=" * 30)
    print("1. Add task")
    print("2. View tasks")
    print("3. Complete task")
    print("4. Delete task")
    print("5. Clear completed tasks")
    print("6. Exit")
    print("=" * 30)


def main():
    """Main application loop"""
    todo = TodoList()

    print("Welcome to your To-Do List!")

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            description = input("Enter task description: ").strip()
            if description:
                todo.add_task(description)
            else:
                print("Task description cannot be empty!")

        elif choice == '2':
            todo.view_tasks()

        elif choice == '3':
            try:
                task_id = int(input("Enter task ID to complete: "))
                todo.complete_task(task_id)
            except ValueError:
                print("Please enter a valid task ID number!")

        elif choice == '4':
            try:
                task_id = int(input("Enter task ID to delete: "))
                todo.delete_task(task_id)
            except ValueError:
                print("Please enter a valid task ID number!")

        elif choice == '5':
            confirm = input("Are you sure you want to clear all completed tasks? (y/n): ")
            if confirm.lower() == 'y':
                todo.clear_completed()

        elif choice == '6':
            print("Thanks for using the To-Do List! Goodbye!")
            break

        else:
            print("Invalid choice! Please enter a number between 1-6.")


if __name__ == "__main__":
    main()