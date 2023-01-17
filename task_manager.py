# =====importing libraries===========
import datetime
import os


def reg_user():
    # loops if reentered username and/or password does not match
    ok = False
    while not ok:
        ru_login_check = open("user.txt", "r+")
        ru_new_username = input("Please enter a new username: \n")
        ok = True
        for ru_line in ru_login_check:
            ru_name = ru_line.strip()
            ru_name = ru_name.split(",")
            ru_user_check = ru_name[0].strip(",")
            if ru_new_username == ru_user_check:
                print("User name has been taken. Please enter a new username.\n")
                ok = False

    while True:
        ru_new_password = input("Please enter a new password: \n")
        ru_new_pass_check = input("Please reenter the new password: \n")
        if ru_new_password == ru_new_pass_check:
            ru_login_check.write(f"\n{ru_new_username}, {ru_new_password}")
            break
        else:
            print("Password do not match. Please renter the information.\n")
    ru_login_check.close()
    return print("New username and password has been logged.\n")


def disp_stat():
    # displaying the two reports from generate reports files
    gen_reports()
    ds_task_overview = open("task_overview.txt", "r")
    ds_user_overview = open("user_overview.txt", "r")
    print(f"————————————————————\n"
          f"Task Overview")
    for ds_line in ds_task_overview:
        ds_line = ds_line.strip()
        ds_line = ds_line.split(":")
        print(f"{ds_line[0]}:\t{ds_line[1]}")
    print(f"————————————————————\n"
          f"————————————————————\n"
          f"User Overview")
    for ds_line in ds_user_overview:
        ds_line = ds_line.strip()
        ds_line = ds_line.split(":")
        print(f"{ds_line[0]}:\t{ds_line[1]}")
    print(f"————————————————————\n")
    ds_task_overview.close()
    ds_user_overview.close()


def gen_reports():
    # creating two reports with various stats
    gr_task = open("tasks.txt", "r")
    user_view = {}
    total_task = 0
    total_complete = 0
    total_incomplete = 0
    task_overdue = 0
    today_date = datetime.date.today()

    for gr_line in gr_task:
        total_task += 1
        gr_data = gr_line.strip()
        gr_data = gr_data.split(",")

        # turning due date into a readable form for python and comparing to today's date
        if gr_data[5] == " No":
            gr_due_date = gr_data[4].strip()
            gr_due_date = datetime.datetime.strptime(gr_due_date, "%d %b %Y").date()
            if today_date > gr_due_date:
                task_overdue += 1

        # making sure user is not duplicated in the nested dictionary
        if gr_data[0] not in user_view:
            user_view[gr_data[0]] = {}

        # counting number of tasks for each user
        if "number of task" in user_view[gr_data[0]]:
            user_view[gr_data[0]]["number of task"] += 1
        else:
            user_view[gr_data[0]]["number of task"] = 1

        # counting total tasks
        if gr_data[5] == " Yes":
            total_complete += 1
        else:
            total_incomplete += 1

        # counting number of completed tasks for each user
        if gr_data[5] == " Yes" and "completed task" in user_view[gr_data[0]]:
            user_view[gr_data[0]]["completed task"] += 1
        elif gr_data[5] == " Yes" and "completed task" not in user_view[gr_data[0]]:
            user_view[gr_data[0]]["completed task"] = 1
        elif gr_data[5] == " No" and "completed task" not in user_view[gr_data[0]]:
            user_view[gr_data[0]]["completed task"] = 0

        # counting number of tasks overdue for each user
        if gr_data[5] == " No" and today_date > gr_due_date and "overdue task" in user_view[gr_data[0]]:
            user_view[gr_data[0]]["overdue task"] += 1
        elif gr_data[5] == " No" and today_date > gr_due_date and "overdue task" not in user_view[gr_data[0]]:
            user_view[gr_data[0]]["overdue task"] = 1
        elif gr_data[5] == " Yes" and "overdue task" not in user_view[gr_data[0]]:
            user_view[gr_data[0]]["overdue task"] = 0

    gr_task_overview = open("task_overview.txt", "w+")
    # creating task file and displaying various stats
    gr_task_overview.write(f"Total number of tasks generated: {total_task}\n"
                           f"Total number of completed tasks: {total_complete}\n"
                           f"Total number of uncompleted tasks: {total_incomplete}\n"
                           f"Percentage of incomplete tasks: {round(((total_incomplete / total_task) * 100), 2)}\n"
                           f"Total number of tasks overdue: {task_overdue}\n"
                           f"Percentage of tasks overdue: {round(((task_overdue / total_task) * 100), 2)}\n")
    gr_task_overview.close()

    gr_user_overview = open("user_overview.txt", "w+")
    # creating file and displaying various stats for each user
    for user_name, user_info in user_view.items():
        gr_user_overview.write(f"User: {user_name}\n")
        for key in user_info:
            gr_user_overview.write(f"Total {key} : {user_info[key]}\n")
        gr_user_overview.write(f"Percentage of total task assigned: "
                               f"{round(((user_view[user_name]['number of task'] / total_task) * 100), 2)}\n"
                               f"Percentage of task assigned that has been completed: "
                               f"{round(((user_view[user_name]['completed task'] / user_view[user_name]['number of task']) * 100), 2)}\n"
                               f"Percentage of task assigned that must still be completed: "
                               f"{round((100 - ((user_view[user_name]['completed task'] / user_view[user_name]['number of task']) * 100)), 2)}\n"
                               f"Percentage of task assigned that are overdue: "
                               f"{round(((user_view[user_name]['overdue task'] / user_view[user_name]['number of task']) * 100), 2)}\n")

    gr_user_overview.close()
    gr_task.close()
    return print("Reports have been generated\n")


def add_task():
    # ask user to input all info for new task and add it to the file
    at_new_user = input("Please enter the username of the person the task is assigned to: \n")
    at_new_title = input("Please enter the title of the task: \n")
    at_new_description = input("Please enter a description of the task: \n")
    at_due_date = input("Please enter the due date of the task: \n")
    at_new_task = open("tasks.txt", "a")
    at_date = datetime.datetime.now().strftime("%d %b %Y")
    at_new_task.write(f"{at_new_user}, {at_new_title}, {at_new_description}, {at_date}, {at_due_date}, No\n")
    at_new_task.close()
    return print("Task has been added.\n")


def view_all():
    # strips each line of spaces and comma and rearranged for a more user-friendly output
    va_task = open("tasks.txt", "r")
    for va_line in va_task:
        va_data = va_line.strip()
        va_data = va_data.split(",")
        print(f"————————————————————\n"
              f"Task:\t\t\t{va_data[1]}\n"
              f"Assigned to:\t {va_data[0]}\n"
              f"Date assigned:\t{va_data[3]}\n"
              f"Due date:\t\t{va_data[4]}\n"
              f"Task Complete?\t{va_data[5]}\n"
              f"Task description:\n\t{va_data[2]}\n"
              f"————————————————————")
    va_task.close()


def view_mine():
    # same as previous block code but only for user that is logged in
    vm_task = open("tasks.txt", "r")
    vm_task_count = 1
    for vm_line in vm_task:
        vm_data = vm_line.strip()
        vm_data = vm_data.split(",")
        if vm_data[0] == user:
            print(f"————————————————————\n"
                  f"{vm_task_count}\n"
                  f"Task:\t\t\t{vm_data[1]}\n"
                  f"Assigned to:\t {vm_data[0]}\n"
                  f"Date assigned:\t{vm_data[3]}\n"
                  f"Due date:\t\t{vm_data[4]}\n"
                  f"Task Complete?\t{vm_data[5]}\n"
                  f"Task description:\n\t{vm_data[2]}\n"
                  f"————————————————————")
            vm_task_count += 1
    vm_task.close()


def task_comp():
    # editing a user selected task to mark as complete and saving it in the task file
    tc_task = open("tasks.txt", "r")
    tc_task_temp = open("tasks_temp.txt", "w")
    tc_line_count = 0
    for tc_line in tc_task:
        tc_line_count += 1
        if user_task.get(task_num) == tc_line_count:
            tc_data = tc_line.strip("No\n")
            tc_data = tc_data + "Yes\n"
            tc_task_temp.write(tc_data)
        else:
            tc_task_temp.write(tc_line)
    tc_task.close()
    tc_task_temp.close()
    os.remove("tasks_backup.txt")
    os.rename("tasks.txt", "tasks_backup.txt")
    os.rename("tasks_temp.txt", "tasks.txt")
    print("Task changed to complete.\n")


def task_edit():
    # editing user selected task to change assigned name or due date and saving it in the task file
    te_task = open("tasks.txt", "r")
    te_task_temp = open("tasks_temp.txt", "w")
    te_line_count = 0
    for te_line in te_task:
        te_line_count += 1

        # changing assigned name
        if user_task.get(task_num) == te_line_count and vm_edit == "u":
            te_data = te_line.strip()
            te_data = te_data.split(",")
            te_edit = input("Please enter the username of the person the task should be assigned to:\n")
            te_data[0] = te_edit
            te_data = ",".join(te_data)
            te_task_temp.write(te_data + "\n")
        # changing due date
        elif user_task.get(task_num) == te_line_count and vm_edit == "d":
            te_data = te_line.strip()
            te_data = te_data.split(",")
            te_edit = input("Please enter the due date the task should be assigned to:\n")
            te_data[0] = te_edit
            te_data = ",".join(te_data)
            te_task_temp.write(te_data + "\n")
        else:
            te_task_temp.write(te_line)
    te_task.close()
    te_task_temp.close()
    os.remove("tasks_backup.txt")
    os.rename("tasks.txt", "tasks_backup.txt")
    os.rename("tasks_temp.txt", "tasks.txt")
    print("Task has been edited.\n")


# ====Login Section====
login = True
menu = False

# stripping all spaces and commas in each line to compare username and password matches
while login:
    login_check = open("user.txt", "r")
    user = input("Please enter your username: \n")
    password = input("Please enter your password: \n")

    for line in login_check:
        name = line.strip()
        name = name.split(",")
        user_check = name[0].strip(",")
        password_check = name[1].strip()
        if user == user_check and password == password_check:
            login = False
            menu = True

    if login:
        print("You have entered an incorrect username or password. Please try again.\n")
    login_check.close()

# only admin gets the additional menu
while menu:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    if user == "admin":
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my tasks
gr - Generate reports 
ds - Display statistics
e - Exit
: ''').lower()
    else:
        menu = input('''Select one of the following Options below:
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: ''').lower()

    if menu == 'r' and user == "admin":
        reg_user()

    elif menu == 'ds' and user == "admin":
        disp_stat()

    elif menu == 'gr' and user == "admin":
        gen_reports()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()
        # menu for user to select their specific non completed task
        task_num = int(input("\nPlease enter a task number or enter -1 to quit.\n:"))
        task = open("tasks.txt", "r")
        task_count = 1
        line_count = 0
        complete = ""
        user_task = {}
        for line in task:
            data = line.strip()
            data = data.split(",")
            line_count += 1
            if data[0] == user:
                user_task[task_count] = line_count
                task_count += 1
                complete = data[5]
        task.close()

        if complete == ' Yes':
            print("Task is already marked complete.\n")

        # menu for user to edit their selected task
        else:

            if task_num in user_task.keys():

                while True:
                    vm_menu = input('''
Select one of the following Options below:
m - Mark task as complete
t - Edit the task
e - Exit
: ''').lower()

                    if vm_menu == 'm':
                        task_comp()

                    # menu to chose what to edit
                    elif vm_menu == 't':
                        vm_edit = input('''
Select Option to edit:
u - Edit username of the person the task is assigned to
d - Edit due date of the task
: ''').lower()
                        task_edit()

                    elif vm_menu == 'e':
                        print('Goodbye!!!')
                        break

                    else:
                        print("You have made an incorrect entry, Please Try again\n")

            elif task_num == -1:
                print("Goodbye!!!")
                break

            else:
                print("The task number you entered does not exist, Please Try again\n")

    elif menu == 'e':
        print('Goodbye!!!')
        break

    else:
        print("You have made a wrong choice, Please Try again\n")
