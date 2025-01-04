import json
import os


MENU_OPTIONS = {  
    1: "Add a Task",
    2: "View Tasks",
    3: "Mark Task as Complete",
    4: "Delete a Task",
    5: "Exit",
}

task_list = []
FILE_NAME = "tasks.json" # File to store tasks

def load_tasks():
    """Loads tasks from a JSON file if it exists."""
    global task_list
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            task_list = json.load(file)
        print("Tasks have been loaded from the file.")
    else:
        print("No saved tasks found. Starting with an empty task list.")


def save_tasks():
    """Saves the current task list to a JSON file."""
    with open(FILE_NAME, "w") as file:
        json.dump(task_list, file, indent=4)


def print_menu():
    """Prints the main menu options."""
    print("\nMAIN MENU")
    for key, value in MENU_OPTIONS.items():
        print(f"{key} -- {value}")


def add_task():
    """Prompts the user to add a new task and appends it to the task list."""
    while True:
        task_description = input("Write a task to add to your list, then hit enter: ").strip()
        if task_description:
            task = {"Description": task_description, "Completed": False}
            task_list.append(task)
            save_tasks()
            print(f'\nThe task "{task["Description"]}" has been added to your list.')
            break
        else:
            print("Task description cannot be empty. Please try again.")


def view_tasks():
    """Displays all tasks in the task list with their completion status."""
    if not task_list:
        print("\nThe task list is empty.")
        return
    print("\nYour Tasks:")
    for index, task in enumerate(task_list, start=1):
        status = "Yes" if task["Completed"] else "No"
        print(f'{index}. {task["Description"]}, Completed: {status}')


def select_task(prompt):
    """Prompts the user to select a valid task number."""
    while True:
        try:
            task_number = int(input(prompt))
            if 1 <= task_number <= len(task_list):
                return task_number - 1
            else:
                print("Invalid number. Please enter a number within the list range.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def mark_task_complete():
    """Prompts the user to mark a task as complete."""
    if not task_list:
        print("\nNo tasks to mark as complete.")
        return
    view_tasks()
    task_number = select_task("Enter the number of the task you would like to mark as complete: ")
    task_list[task_number]["Completed"] = True
    save_tasks()
    print(f'\nThe task "{task_list[task_number]["Description"]}" has been marked as complete.')


def delete_task():
    """Prompts the user to delete a task."""
    if not task_list:
        print("\nNo tasks to delete.")
        return
    view_tasks()
    task_number = select_task("Enter the number of the task you would like to delete: ")
    deleted_task = task_list.pop(task_number)
    save_tasks()
    print(f'\nThe task "{deleted_task["Description"]}" has been deleted.')


def main():
    """Runs the main menu loop."""
    load_tasks()
    while True:
        print_menu()
        try:
            option = int(input("\nEnter your choice (number): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if option == 1:
            add_task()
        elif option == 2:
            view_tasks()
        elif option == 3:
            mark_task_complete()
        elif option == 4:
            delete_task()
        elif option == 5:
            print("\nExiting To-Do List application. Goodbye!")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
