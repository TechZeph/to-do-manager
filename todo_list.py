import json
import os
from datetime import datetime


class TaskManager:
    def __init__(self, file_name="tasks.json"):
        self.file_name = file_name
        self.task_list = []
        self.load_tasks()

    def load_tasks(self):
        """Loads tasks from a JSON file if it exists."""
        try:
            if os.path.exists(self.file_name):
                with open(self.file_name, "r") as file:
                    self.task_list = json.load(file)
                print("Tasks have been loaded from the file.")
            else:
                print("No saved tasks found. Starting with an empty task list.")
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading tasks: {e}")
            self.task_list = []

    def save_tasks(self):
        """Saves the current task list to a JSON file."""
        try:
            with open(self.file_name, "w") as file:
                json.dump(self.task_list, file, indent=4)
        except IOError as e:
            print(f"Error saving tasks: {e}")

    def is_task_list_empty(self):
        """Checks if the task list is empty and prints a message if it is."""
        if not self.task_list:
            print("\nThe task list is empty.")
            return True
        return False

    def print_menu(self):
        """Prints the main menu options."""
        menu_options = {
            1: "Add a Task",
            2: "View/Edit Tasks",
            3: "Mark Task(s) as Complete",
            4: "Delete a Task",
            5: "Search Tasks",
            6: "View Statistics",
            7: "Exit",
        }
        print("\nMAIN MENU")
        for key, value in menu_options.items():
            print(f"{key} -- {value}")

    def get_priority(self):
        """Prompts the user to select a priority level."""
        valid_priorities = ["High", "Medium", "Low"]
        while True:
            priority = input("Enter task priority (High, Medium, Low): ").capitalize().strip()
            if priority in valid_priorities:
                return priority
            else:
                print("Invalid input. Please enter 'High', 'Medium', or 'Low'.")

    def get_due_date(self):
        """Prompts the user to enter a due date for the task."""
        while True:
            due_date_str = input("Enter due date (YYYY-MM-DD) or press Enter to skip: ").strip()
            if not due_date_str:
                return None
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
                return due_date_str
            except ValueError:
                print("Invalid date format. Please enter in YYYY-MM-DD format.")

    def add_task(self):
        """Prompts the user to add a new task and appends it to the task list."""
        while True:
            task_description = input("Write a task to add to your list, then hit enter: ").strip()
            if task_description:
                priority = self.get_priority()
                due_date = self.get_due_date()
                category = input("Enter task category (e.g., Work, Personal): ").strip()
                task = {
                    "Description": task_description,
                    "Completed": False,
                    "Priority": priority,
                    "DueDate": due_date,
                    "Category": category
                }
                self.task_list.append(task)
                self.save_tasks()
                print(f'\nThe task "{task["Description"]}" has been added to your list.')
                break
            else:
                print("Task description cannot be empty. Please try again.")

    def view_or_edit_tasks(self, pause=False, edit_mode=False):
        """Displays all tasks in the task list with option for editing tasks."""
        if self.is_task_list_empty():
            return

        print("\nYour Tasks:")
        for index, task in enumerate(self.task_list, start=1):
            status = "Yes" if task["Completed"] else "No"
            priority = task.get("Priority", "None")
            due_date = task.get("DueDate", "None")
            category = task.get("Category", "None")
            print(f'{index}. {task["Description"]}, Completed: {status}, Priority: {priority}, Due Date: {due_date}, Category: {category}')

        if edit_mode:
            while True:
                try:
                    task_number = int(input("\nEnter the number of the task to edit, or 0 to return: "))
                    if task_number == 0:
                        break
                    elif 1 <= task_number <= len(self.task_list):
                        task_index = task_number - 1
                        self.edit_task(task_index)
                        break
                    else:
                        print("Invalid number. Please enter a valid task number.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

        if pause and not edit_mode:  # Only pauses if pause parameter is set to true
            input("\nPress Enter to return to the previous menu...")

    def edit_task(self, task_index):
        """Displays edit options for a selected task."""
        task = self.task_list[task_index]
        while True:
            print(f'\nEditing Task: {task["Description"]}')
            print("1 -- Edit Description")
            print("2 -- Edit Priority")
            print("3 -- Edit Due Date")
            print("4 -- Edit Category")
            print("5 -- Mark as Complete")
            print("6 -- Return to Main Menu")

            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    new_description = input("Enter the new description: ").strip()
                    if new_description:
                        task["Description"] = new_description
                        print("Task description updated.")
                    else:
                        print("Description cannot be empty.")
                elif choice == 2:
                    task["Priority"] = self.get_priority()
                    print("Task priority updated.")
                elif choice == 3:
                    task["DueDate"] = self.get_due_date()
                    print("Task due date updated.")
                elif choice == 4:
                    task["Category"] = input("Enter the new category: ").strip()
                    print("Task category updated.")
                elif choice == 5:
                    task["Completed"] = not task["Completed"]
                    print(f'Task marked as {"complete" if task["Completed"] else "incomplete"}.')
                elif choice == 6:
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 6.")

                self.save_tasks()
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def select_task(self, prompt):
        """Prompts the user to select a valid task number or cancel by entering 0."""
        while True:
            try:
                task_number = int(input(prompt))
                if task_number == 0:
                    return None  # User cancels the operation
                elif 1 <= task_number <= len(self.task_list):
                    return task_number - 1
                else:
                    print("Invalid number. Please enter a number within the list range.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def mark_tasks_complete(self):
        """Prompts the user to mark multiple tasks as complete."""
        if self.is_task_list_empty():
            return
        self.view_or_edit_tasks()
        task_numbers = input("Enter the numbers of the tasks to mark as complete, separated by commas (0 to cancel): ")
        if task_numbers.strip() == "0":
            print("Operation canceled.")
            return
        try:
            task_indices = [int(num.strip()) - 1 for num in task_numbers.split(",")]
            for index in task_indices:
                if 0 <= index < len(self.task_list):
                    self.task_list[index]["Completed"] = True
            self.save_tasks()
            print("\nSelected tasks have been marked as complete.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter valid task numbers.")

    def delete_task(self):
        """Prompts the user to delete a task with confirmation."""
        if self.is_task_list_empty():
            return
        self.view_or_edit_tasks()
        task_number = self.select_task("Enter the number of the task you would like to delete (0 to cancel): ")
        if task_number is not None:
            confirmation = input(f'Are you sure you want to delete the task "{self.task_list[task_number]["Description"]}"? (yes/no): ').strip().lower()
            if confirmation == "yes":
                deleted_task = self.task_list.pop(task_number)
                self.save_tasks()
                print(f'\nThe task "{deleted_task["Description"]}" has been deleted.')
                print(f"Remaining tasks: {len(self.task_list)}")
            else:
                print("Deletion canceled.")
        else:
            print("Deletion canceled.")

    def search_tasks(self):
        """Allows the user to search tasks by keyword or priority."""
        if self.is_task_list_empty():
            return
        search_option = input("Search by (1) Keyword or (2) Priority: ").strip()
        if search_option == "1":
            keyword = input("Enter a keyword to search for: ").strip().lower()
            results = [task for task in self.task_list if keyword in task["Description"].lower()]
        elif search_option == "2":
            priority = self.get_priority()
            results = [task for task in self.task_list if task["Priority"] == priority]
        else:
            print("Invalid option.")
            return

        if results:
            print("\nSearch Results:")
            for index, task in enumerate(results, start=1):
                status = "Yes" if task["Completed"] else "No"
                due_date = task.get("DueDate", "None")
                category = task.get("Category", "None")
                print(f'{index}. {task["Description"]}, Completed: {status}, Priority: {task["Priority"]}, Due Date: {due_date}, Category: {category}')
        else:
            print("No tasks found matching the search criteria.")

    def view_statistics(self):
        """Displays task statistics and progress."""
        if self.is_task_list_empty():
            return

        total_tasks = len(self.task_list)
        completed_tasks = sum(1 for task in self.task_list if task["Completed"])
        high_priority = sum(1 for task in self.task_list if task["Priority"] == "High")
        medium_priority = sum(1 for task in self.task_list if task["Priority"] == "Medium")
        low_priority = sum(1 for task in self.task_list if task["Priority"] == "Low")
        progress = (completed_tasks / total_tasks) * 100

        print("\nTask Statistics:")
        print(f"Total Tasks: {total_tasks}")
        print(f"Completed Tasks: {completed_tasks}")
        print(f"High Priority Tasks: {high_priority}")
        print(f"Medium Priority Tasks: {medium_priority}")
        print(f"Low Priority Tasks: {low_priority}")
        print(f"Progress: {progress:.2f}% completed")

    def run(self):
        """Runs the main menu loop."""
        while True:
            self.print_menu()
            try:
                option = int(input("\nEnter your choice (number): "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if option == 1:
                self.add_task()
            elif option == 2:
                self.view_or_edit_tasks(pause=True, edit_mode=True)
            elif option == 3:
                self.mark_tasks_complete()
            elif option == 4:
                self.delete_task()
            elif option == 5:
                self.search_tasks()
            elif option == 6:
                self.view_statistics()
            elif option == 7:
                print("\nExiting To-Do List application. Goodbye!")
                break
            else:
                print("Invalid option. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.run()
