import json
import os


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
            2: "View Tasks",
            3: "Mark Task as Complete",
            4: "Delete a Task",
            5: "Exit",
        }
        print("\nMAIN MENU")
        for key, value in menu_options.items():
            print(f"{key} -- {value}")

    def get_priority(self): #Error when calling this function, need to look into it.
        """Prompts the user to select a priority level."""
        valid_priorities = ["High", "Medium", "Low"]
        while True:
            priority = input("Enter task priority (High, Medium, Low): ").capitalize().strip()
            if priority in valid_priorities:
                return priority
            else:
                print("Invalid input. Please enter 'High', 'Medium', or 'Low'.")

    def add_task(self):
        """Prompts the user to add a new task and appends it to the task list."""
        while True:
            task_description = input("Write a task to add to your list, then hit enter: ").strip()
            if task_description:
                priority = self.get_priority() #get_priority function not working
                task = {"Description": task_description, "Completed": False, "Priority": priority}, 
                self.task_list.append(task)
                self.save_tasks()
                print(f'\nThe task "{task["Description"]}" has been added to your list.')
                break
            else:
                print("Task description cannot be empty. Please try again.")

    def view_or_edit_task(self, pause=False, edit_mode=False):
        """Displays all tasks in the task list with option for editing tasks."""
        if self.is_task_list_empty():
            return
        print("\nYour Tasks:")
        for index, task in enumerate(self.task_list, start=1):
            status = "Yes" if task["Completed"] else "No"
            priority = task.get("Priority", "None")
            print(f'{index}. {task["Description"]}, Completed: {status}, Priority: {priority}')
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
        if pause: #Only pauses if parameter is set to true
            input("\nPress Enter to return to the previous menu...")


def edit_task(self, task_index):
    """Displays edit options for a selected task."""
    task = self.task_list[task_index]
    while True:
        print(f'\nEditing Task: {task["Description"]}')
        print("1 -- Edit Description")
        print("2 -- Edit Priority")
        print("3 -- Mark as Complete")
        print("4 -- Return to Main Menu")

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
                task["Completed"] = not task["Completed"]
                print(f'Task marked as {"complete" if task["Completed"] else "incomplete"}.')
            elif choice == 4:
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
            
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

    def mark_task_complete(self):
        """Prompts the user to mark a task as complete."""
        if self.is_task_list_empty():
            return
        self.view_tasks()
        task_number = self.select_task("Enter the number of the task you would like to mark as complete (0 to cancel): ")
        if task_number is not None:
            self.task_list[task_number]["Completed"] = True
            self.save_tasks()
            print(f'\nThe task "{self.task_list[task_number]["Description"]}" has been marked as complete.')
        else:
            print("Operation canceled.")

    def delete_task(self):
        """Prompts the user to delete a task."""
        if self.is_task_list_empty():
            return
        self.view_tasks()
        task_number = self.select_task("Enter the number of the task you would like to delete (0 to cancel): ")
        if task_number is not None:
            deleted_task = self.task_list.pop(task_number)
            self.save_tasks()
            print(f'\nThe task "{deleted_task["Description"]}" has been deleted.')
            print(f"Remaining tasks: {len(self.task_list)}")
        else:
            print("Deletion canceled.")

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
                self.view_tasks(pause=True)
            elif option == 3:
                self.mark_task_complete()
            elif option == 4:
                self.delete_task()
            elif option == 5:
                print("\nExiting To-Do List application. Goodbye!")
                break
            else:
                print("Invalid option. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.run()
