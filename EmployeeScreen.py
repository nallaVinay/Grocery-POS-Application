import mysql.connector
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
import re


class EmployeeScreen(Screen):
    def show_all_employees(self):
        # Establish a connection to your MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vinay@143",
            port='3306',
            database='grocerystore'
        )
        cursor = conn.cursor()

        # Fetch specific columns (first_name, last_name, emp_id, phone) from the database
        cursor.execute("SELECT first_name, last_name, emp_id, emp_password FROM employee")
        employees_data = cursor.fetchall()

        # Close the database connection
        cursor.close()
        conn.close()

        # Create a BoxLayout to organize the labels and the scroll view
        content_layout = BoxLayout(orientation='vertical', padding=10, spacing=40,
                                   background_color=(0.004, 0.055, 0.102, 1.0))

        # Create a GridLayout for the labels
        labels_layout = GridLayout(cols=4, size_hint_y=None, height='40dp', padding=10, spacing=40)

        # Set fixed widths for columns
        column_widths = [150, 150, 150, 150]

        # Add column labels
        labels_layout.add_widget(Label(text='First Name', size_hint_x=None, width=column_widths[0]))
        labels_layout.add_widget(Label(text='Last Name', size_hint_x=None, width=column_widths[1]))
        labels_layout.add_widget(Label(text='Employee ID', size_hint_x=None, width=column_widths[2]))
        labels_layout.add_widget(Label(text='password', size_hint_x=None, width=column_widths[3]))

        # Add labels layout to content layout
        content_layout.add_widget(labels_layout)

        # Create a ScrollView with GridLayout inside to allow scrolling
        layout = GridLayout(cols=4, size_hint_y=None, padding=10, spacing=40)
        layout.bind(minimum_height=layout.setter('height'))

        # Add employee data
        for employee in employees_data:
            first_name_label = Label(text=employee[0], size_hint_x=None, width=column_widths[0], height='40dp',
                                     )
            last_name_label = Label(text=employee[1], size_hint_x=None, width=column_widths[1], height='40dp',
                                    )
            emp_id_label = Label(text=str(employee[2]), size_hint_x=None, width=column_widths[2], height='40dp',
                                 )
            phone_label = Label(text=employee[3], size_hint_x=None, width=column_widths[3], height='40dp',
                                )

            layout.add_widget(first_name_label)
            layout.add_widget(last_name_label)
            layout.add_widget(emp_id_label)
            layout.add_widget(phone_label)

        # Create a ScrollView with GridLayout inside to allow scrolling
        scroll_view = ScrollView()
        scroll_view.add_widget(layout)

        # Add scroll view to content layout
        content_layout.add_widget(scroll_view)

        # Create a close button
        close_button = Button(text='Close', size_hint=(None, None), size=(100, 50),
                              background_color=(0.133, 0.855, 0.431, 1.0))
        close_button.bind(on_press=self.dismiss_popup)

        # Add close button to content layout
        content_layout.add_widget(close_button)

        # Create a Popup with the content layout
        self.popup = Popup(title='All Employees', content=content_layout, size_hint=(None, None), size=(800, 600),
                           background_color=(0.004, 0.055, 0.102, 1.0), auto_dismiss=False)
        self.popup.open()

    def dismiss_popup(self, instance):
        if hasattr(self, 'popup') and self.popup:
            self.popup.dismiss()

    def add_employee(self):
        # Create a GridLayout to organize input fields
        layout = GridLayout(cols=2, spacing=10, padding=10, background_color=(0.004, 0.055, 0.102, 1.0))

        # Add labels and input fields for each attribute
        layout.add_widget(Label(text='First Name:', ))
        self.first_name_input = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),
                                          cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.first_name_input)

        layout.add_widget(Label(text='Last Name:', ))
        self.last_name_input = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),
                                         cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.last_name_input)

        layout.add_widget(Label(text='Age:', ))
        self.age = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),
                             cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.age)

        layout.add_widget(Label(text='Phone:', ))
        self.phone_input = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),
                                     cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.phone_input)

        layout.add_widget(Label(text='Email:', ))
        self.email_input = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),
                                     cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.email_input)

        layout.add_widget(Label(text='Street Address:', ))
        self.street_address_input = TextInput(multiline=True, background_color=(0.004, 0.055, 0.102, 1.0),
                                              cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.street_address_input)

        layout.add_widget(Label(text='City:', ))
        self.city_input = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),
                                    cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.city_input)

        layout.add_widget(Label(text='State:', ))
        self.state_input = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),
                                     cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.state_input)

        layout.add_widget(Label(text='Zip Code:', ))
        self.Zip_input = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),
                                   cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.Zip_input)

        layout.add_widget(Label(text='Employee Login Status:', ))
        self.login_status_spinner = Spinner(text='Active', values=['Active', 'Inactive'],
                                            background_color=(0.004, 0.055, 0.102, 1.0))
        layout.add_widget(self.login_status_spinner)

        layout.add_widget(Label(text='Employee Level:', ))
        self.emp_level_spinner = Spinner(text='1', values=['1', '2', '3', '4', '5'],
                                         background_color=(0.004, 0.055, 0.102, 1.0))
        layout.add_widget(self.emp_level_spinner)
        layout.add_widget(Label(text='user_id:', ))
        self.user_id = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),
                                 cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.user_id)
        layout.add_widget(Label(text='Password:', ))
        self.password = TextInput(multiline=False, password=True, background_color=(0.004, 0.055, 0.102, 1.0),
                                  cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.password)
        layout.add_widget(Label(text='Confirm Password:', ))
        self.con_password = TextInput(multiline=False, password=True, background_color=(0.004, 0.055, 0.102, 1.0),
                                      cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.con_password)

        # Create a submit button
        submit_button = Button(text='Submit', background_color=(0.133, 0.855, 0.431, 1.0))
        submit_button.bind(on_press=self.submit_employee)
        layout.add_widget(submit_button)

        # Create a cancel button
        cancel_button = Button(text='Close', background_color=(0.133, 0.855, 0.431, 1.0))
        cancel_button.bind(on_press=self.dismiss_popup1)
        layout.add_widget(cancel_button)

        # Create a Popup with the layout and background color
        self.popup1 = Popup(title='Add Employee', content=layout, size_hint=(None, None), size=(720, 720),
                            background_color=(0.004, 0.055, 0.102, 1.0), auto_dismiss=False)
        self.popup1.open()

    def submit_employee(self, instance):
        # Retrieve employee data from input fields
        first_name = self.first_name_input.text
        last_name = self.last_name_input.text
        age = self.age.text
        phone = self.phone_input.text
        email = self.email_input.text
        street_address = self.street_address_input.text
        zip = self.Zip_input.text
        city = self.city_input.text
        state = self.state_input.text
        login_status = self.login_status_spinner.text
        emp_level = self.emp_level_spinner.text
        pass1 = self.password.text
        pass2 = self.con_password.text
        user = self.user_id.text

        # Perform validation checks
        if not all([first_name, last_name, phone, email, street_address, city, state, zip,pass1,pass2]):
            self.show_error_popup("All fields are required.")
            return
        if not age.isdigit():
            self.show_error_popup("Invalid Age.\n Age number must be  between 18-45.")
            return
        if len(phone) != 10 or not phone.isdigit():
            self.show_error_popup("Invalid phone number.\n Phone number must be 10 digits.")
            return

        if not email.endswith('@gmail.com') or not email[0].isalpha():
            self.show_error_popup("Invalid email address. \nEmail must end with @gmail.com")
            return
        if len(zip) != 6 or not zip.isdigit():
            self.show_error_popup("Invalid zip number.\n zip number must be 6 digits.")
            return
        if not user.isdigit():
            self.show_error_popup("Invalid user .\n user must be digit")
            return
        if pass1 != pass2:
            self.show_error_popup("Invalid password.\n password must be  same ")
            return
        # If all validation checks pass, save employee information to the database
        try:
            # Establish a connection to MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Vinay@143",
                database="grocerystore"
            )
            cursor = conn.cursor()
            number = self.add_dashes_to_number_with_existing_dashes(phone)
            # Execute INSERT query to insert employee details into the database
            insert_query = "INSERT INTO employee (emp_id,first_name, last_name, phone,zip, mail, street_address, city, state, employee_login_status, emp_level,emp_password,age) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (user,
                                          first_name, last_name, number, zip, email, street_address, city, state,
                                          login_status, emp_level, pass1, age))

            # Commit changes and close connection
            conn.commit()
            cursor.close()
            conn.close()

            # Show success popup
            self.show_success_popup("Employee details saved to database successfully.")

        except mysql.connector.Error as e:
            p = str(e)
            self.show_error_popup("Failed to add employee \n{}".format(
                p[13:].replace('Duplicate entry', 'Already Exist ').replace('employee.', 'in ').replace('for key',
                                                                                                        '  ')))

    def add_dashes_to_number_with_existing_dashes(self, number):
        # Convert number to string
        number_str = str(number)

        # Use regular expression to add dashes after every three digits for the first two groups
        # and after every four digits for the last group
        formatted_number = re.sub(r'(\d{3})(\d{3})(\d{4})', r'\1-\2-\3', number_str)

        return formatted_number

    def show_success_popup(self, message):
        # Display a success popup with the given message
        success_popup = Popup(title='Success', content=Label(text=message), size_hint=(None, None), size=(300, 200))
        success_popup.open()

    def show_error_popup(self, message):
        # Display an error popup with the given message
        popup_width = len(message) * 10  # Adjust the multiplier based on your preference
        popup_height = max(len(message) // 15,
                           1) * 40  # Adjust the divisor and multiplier based on your preference

        error_popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None),
                            size=(popup_width, popup_height))
        error_popup.open()

    def dismiss_popup1(self, instance=None):
        self.popup1.dismiss()

    def edit_employee(self):
        # Create a GridLayout to organize input fields
        layout = GridLayout(cols=2, spacing=5, padding=10)

        # Add labels and input fields for user ID and password
        layout.add_widget(Label(text='last_name:',))
        self.lastname_input = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.lastname_input)

        layout.add_widget(Label(text='phone:',))
        self.phonenumber_input = TextInput(multiline=False, password=True, background_color=(0.004, 0.055, 0.102, 1.0),cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.phonenumber_input)
        # Create a submit button
        submit_button = Button(text='Submit', background_color=(0.133, 0.855, 0.431, 1.0))
        submit_button.bind(on_press=self.authenticate_employee)
        layout.add_widget(submit_button)

        # Create a Popup with the layout
        self.popup = Popup(title='Select Employee', content=layout, size_hint=(None, None),
                           background_color=(0.004, 0.055, 0.102, 1.0), size=(400, 200))
        self.popup.open()

    def authenticate_employee(self, instance):
        # Retrieve user ID and password from input fields
        lastname = self.lastname_input.text.strip()
        phone = self.phonenumber_input.text.strip()
        if not all([lastname, phone]):
            self.show_error_popup1("All fields are required.")
            return
        if len(phone) != 10 or not phone.isdigit():
            self.show_error_popup1("Invalid phone number.\n Phone number must be 10 digits.")
            return
        # Perform authentication against the database
        try:
            # Establish a connection to MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Vinay@143",
                database="grocerystore"
            )
            cursor = conn.cursor()

            # Execute SELECT query to retrieve employee details based on user ID and password
            select_query = "SELECT * FROM employee WHERE last_name = %s AND phone = %s"
            cursor.execute(select_query, (lastname, self.add_dashes_to_number_with_existing_dashes(phone)))
            employee = cursor.fetchone()

            if employee:
                # Employee found, close current popup and display details in another popup
                self.popup.dismiss()
                self.show_employee_details(employee)
            else:
                # Employee not found, show error message
                self.show_error_popup1("Invalid lastname or phone number.")

            cursor.close()
            conn.close()

        except mysql.connector.Error as e:
            p = str(e)
            self.show_error_popup("Failed to authenticate \n{}".format(
                p[13:].replace('Duplicate entry', 'Already Exist ').replace('employee.', 'in ').replace('for key',
                                                                                                        '  ')))

    def show_employee_details(self, employee):
        # Convert the tuple to a dictionary
        employee_dict = {

            'first_name': employee[2],
            'last_name': employee[3],
            'Age': employee[4],
            'phone': employee[9],
            'email': employee[10],
            'street_address': employee[5],
            'city': employee[6],
            'state': employee[7],
            'zip': employee[8],
            'login_status': employee[11],
            'emp_level': employee[12],
            'id': employee[0],
            "password": employee[1]
        }

        # Create a Popup to display employee details
        self.selected_employee_popup = Popup(title='Selected Employee', size_hint=(None, None), auto_dismiss=False,
                                             background_color=(0.004, 0.055, 0.102, 1.0), size=(500, 500))

        # Create a GridLayout to organize employee details
        layout = GridLayout(cols=2, spacing=5, padding=10)

        # Add labels and employee details to the layout
        for key, value in employee_dict.items():
            layout.add_widget(Label(text=str(key), ))
            layout.add_widget(Label(text=str(value),))

        # Add an "Edit" button to allow editing employee details
        edit_button = Button(text='Edit', background_color=(0.133, 0.855, 0.431, 1.0))
        edit_button.bind(on_press=lambda instance: self.edit_employee1(employee_dict))
        layout.add_widget(edit_button)

        # Add the layout to the popup
        self.selected_employee_popup.content = layout

        # Open the popup with employee details
        self.selected_employee_popup.open()

    def edit_employee1(self, employee):
        self.selected_employee_popup.dismiss()
        values = list(employee.values())
        # Create a GridLayout to organize input fields
        layout = GridLayout(cols=2, spacing=10, padding=10, background_color=(0.004, 0.055, 0.102, 1.0))
        print(values)
        # Add labels and input fields for each attribute
        layout.add_widget(Label(text='First Name:', ))
        self.first_name_input1 = TextInput(multiline=False, text=str(values[0]),
                                           background_color=(0.004, 0.055, 0.102, 1.0),
                                           cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.first_name_input1)

        layout.add_widget(Label(text='Last Name:', ))
        self.last_name_input1 = TextInput(multiline=False, text=str(values[1]),
                                          background_color=(0.004, 0.055, 0.102, 1.0),
                                          cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.last_name_input1)

        layout.add_widget(Label(text='Age:', ))
        self.age1 = TextInput(multiline=False, text=str(values[2]), background_color=(0.004, 0.055, 0.102, 1.0),
                              cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.age1)

        layout.add_widget(Label(text='Phone:', ))
        self.phone_input1 = TextInput(multiline=False, text=str(values[3].replace('-', '')),
                                      background_color=(0.004, 0.055, 0.102, 1.0),
                                      cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.phone_input1)

        layout.add_widget(Label(text='Email:', ))
        self.email_input1 = TextInput(multiline=False, text=str(values[4]), background_color=(0.004, 0.055, 0.102, 1.0),
                                      cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.email_input1)

        layout.add_widget(Label(text='Street Address:', ))
        self.street_address_input1 = TextInput(multiline=True, text=str(values[5]),
                                               background_color=(0.004, 0.055, 0.102, 1.0),
                                               cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.street_address_input1)

        layout.add_widget(Label(text='City:',))
        self.city_input1 = TextInput(multiline=False, text=str(values[6]), background_color=(0.004, 0.055, 0.102, 1.0),
                                     cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.city_input1)

        layout.add_widget(Label(text='State:', ))
        self.state_input1 = TextInput(multiline=False, text=str(values[7]), background_color=(0.004, 0.055, 0.102, 1.0),
                                      cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.state_input1)

        layout.add_widget(Label(text='Zip Code:', ))
        self.Zip_input1 = TextInput(multiline=False, text=str(values[8]), background_color=(0.004, 0.055, 0.102, 1.0),
                                    cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.Zip_input1)

        layout.add_widget(Label(text='Employee Login Status:', ))
        self.login_status_spinner1 = Spinner(text=str(values[9]), values=['Active', 'Inactive'],
                                             background_color=(0.004, 0.055, 0.102, 1.0))
        layout.add_widget(self.login_status_spinner1)

        layout.add_widget(Label(text='Employee Level:', ))
        self.emp_level_spinner1 = Spinner(text=str(values[10]), values=['1', '2', '3', '4', '5'],
                                          background_color=(0.004, 0.055, 0.102, 1.0))
        layout.add_widget(self.emp_level_spinner1)
        layout.add_widget(Label(text='user_id:', ))
        self.user_id1 = TextInput(multiline=False, text=str(values[11]), background_color=(0.004, 0.055, 0.102, 1.0),
                                  cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.user_id1)
        layout.add_widget(Label(text='Password:', ))
        self.password1 = TextInput(multiline=False, text=str(values[12]), background_color=(0.004, 0.055, 0.102, 1.0),
                                   cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.password1)

        # Create a submit button
        submit_button1 = Button(text='Submit', background_color=(0.133, 0.855, 0.431, 1.0))
        submit_button1.bind(on_press=lambda instance: self.submit_employee1(values[11]))

        layout.add_widget(submit_button1)

        # Create a cancel button
        cancel_button1 = Button(text='Close', background_color=(0.133, 0.855, 0.431, 1.0))
        cancel_button1.bind(on_press=self.dismiss_popup11)
        layout.add_widget(cancel_button1)

        # Create a Popup with the layout and background color
        self.popup11 = Popup(title='Edit Employee', content=layout, size_hint=(None, None), size=(720, 720),
                             background_color=(0.004, 0.055, 0.102, 1.0), auto_dismiss=False)
        self.popup11.open()

    def submit_employee1(self, value):
        # Retrieve employee data from input fields
        first_name = self.first_name_input1.text
        last_name = self.last_name_input1.text
        age = self.age1.text
        phone = self.phone_input1.text
        email = self.email_input1.text
        street_address = self.street_address_input1.text
        zip = self.Zip_input1.text
        city = self.city_input1.text
        state = self.state_input1.text
        login_status = self.login_status_spinner1.text
        emp_level = self.emp_level_spinner1.text
        pass1 = self.password1.text
        user = self.user_id1.text

        # Perform validation checks
        if not all(
                [first_name, last_name, phone, email, street_address, city, state, zip, user, pass1, age, login_status,
                 emp_level]):
            self.show_error_popup("All fields are required.")
            return
        if not age.isdigit():
            self.show_error_popup("Invalid Age.\n Age number must be  between 18-45.")
            return
        if len(phone) != 10 or not phone.isdigit():
            self.show_error_popup("Invalid phone number.\n Phone number must be 10 digits.")
            return

        if not email.endswith('@gmail.com') or not email[0].isalpha():
            self.show_error_popup("Invalid email address. \nEmail must end with @gmail.com")
            return
        if len(zip) != 6 or not zip.isdigit():
            self.show_error_popup("Invalid zip number.\n zip number must be 6 digits.")
            return
        if not user.isdigit():
            self.show_error_popup("Invalid user .\n user must be digit")
            return
        # If all validation checks pass, save employee information to the database
        try:
            # Establish a connection to MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Vinay@143",
                database="grocerystore"
            )
            id = value
            phone = self.add_dashes_to_number_with_existing_dashes(phone)
            cursor = conn.cursor()
            # Construct the UPDATE query
            update_query = """
                        UPDATE employee
                        SET first_name = %s, last_name = %s, age = %s, phone = %s, mail = %s, 
                            street_address = %s, zip = %s, city = %s, state = %s, 
                            employee_login_status = %s, emp_level = %s, emp_password = %s,
                            emp_id = %s
                        WHERE emp_id = %s
                    """
            cursor.execute(update_query, (
                first_name, last_name, age, phone, email, street_address, zip,
                city, state, login_status, emp_level, pass1, user, id
            ))
            conn.commit()  # Commit the transaction

            # Close the cursor and connection
            cursor.close()
            conn.close()

            # Close the popup after update

            # Show success popup
            self.show_success_popup("Employee details \nupdated  to database successfully.")
            self.popup11.dismiss()

        except mysql.connector.Error as e:
            p = str(e)
            self.show_error_popup("Failed to add employee \n{}".format(
                p[13:].replace('Duplicate entry', 'Already Exist ').replace('employee.', 'in ').replace('for key',
                                                                                                        '  ')))

    def show_error_popup1(self, message):
        # Display an error popup with the given message
        error_popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(300, 200))
        error_popup.open()

    def delete_employee(self):

        # Create a GridLayout to organize input fields
        self.layout = GridLayout(cols=2, spacing=5, padding=10)

        # Add labels and input fields for user ID and password
        self.layout.add_widget(Label(text='emp_id:',))
        self.emp_id_d = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        self.layout.add_widget(self.emp_id_d)

        self.layout.add_widget(Label(text='password:', ))
        self.password_d = TextInput(multiline=False, password=True, background_color=(0.004, 0.055, 0.102, 1.0),cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        self.layout.add_widget(self.password_d)
        # Create a submit button
        self.submit_button = Button(text='Submit', background_color=(0.133, 0.855, 0.431, 1.0))
        self.submit_button.bind(on_press=self.dele_employee)
        self.layout.add_widget(self.submit_button)
        self.cancel = Button(text='Cancel', background_color=(0.133, 0.855, 0.431, 1.0))
        self.cancel.bind(on_press=self.dismiss_popup111)
        self.layout.add_widget(self.cancel)

        # Create a Popup with the layout
        self.popup111 = Popup(title='Select Employee', content=self.layout, size_hint=(None, None),
                           background_color=(0.004, 0.055, 0.102, 1.0), size=(400, 200))
        self.popup111.open()
    def dismiss_popup11(self, instance=None):
        self.popup11.dismiss()
    def dismiss_popup111(self, instance=None):
        self.popup111.dismiss()
    def dele_employee(self, instance):
        # Retrieve user ID and password from input fields
        emp_id1 = self.emp_id_d.text.strip()
        passs1 = self.password_d.text.strip()
        if not all([emp_id1,passs1]):
            self.show_error_popup1("All fields are required.")
            return
        if not emp_id1.isdigit():
            self.show_error_popup1("Invalid emp_id number.\n emp_id must be digit")
            return
        # Perform authentication against the database
        try:
            # Establish a connection to MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Vinay@143",
                database="grocerystore"
            )
            cursor = conn.cursor()

            # Execute SELECT query to retrieve employee details based on user ID and password
            select_query = "DELETE FROM employee WHERE emp_id = %s AND emp_password = %s"
            cursor.execute(select_query, (emp_id1, passs1))
            conn.commit()
            cursor.close()
            conn.close()

            # Show success popup
            if cursor.rowcount!=0:
                self.show_success_popup("Employee details Deleted  to database successfully.")
                self.popup111.dismiss()
            else:
                self.show_error_popup1('employee details not exist.')

        except mysql.connector.Error as e:
            p = str(e)
            self.show_error_popup("Failed to authenticate \n{}".format(
                p[13:].replace('Duplicate entry', 'Already Exist ').replace('employee.', 'in ').replace('for key',
                                                                                                        '  ')))