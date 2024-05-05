import mysql.connector
from kivy.uix.screenmanager import Screen
from datetime import datetime
import re
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
import mysql.connector


class Delivery(Screen):

    def show_all_suppliers(self):
        # Establish a connection to your MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vinay@143",
            port='3306',
            database='grocerystore'
        )
        cursor = conn.cursor()

        # Fetch specific columns (first_name, last_name, sup_id, phone) from the database
        cursor.execute("SELECT first_name, last_name, sup_id, phone FROM supplier")
        supplier_data = cursor.fetchall()

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
        labels_layout.add_widget(Label(text='supplier id', size_hint_x=None, width=column_widths[2]))
        labels_layout.add_widget(Label(text='Phone no.', size_hint_x=None, width=column_widths[3]))

        # Add labels layout to content layout
        content_layout.add_widget(labels_layout)

        # Create a ScrollView with GridLayout inside to allow scrolling
        layout = GridLayout(cols=4, size_hint_y=None, padding=10, spacing=40)
        layout.bind(minimum_height=layout.setter('height'))
        # Add  data
        for supplier in supplier_data:
            first_name_label = Label(text=supplier[0], size_hint_x=None, width=column_widths[0], height='40dp',
                                     )
            last_name_label = Label(text=supplier[1], size_hint_x=None, width=column_widths[1], height='40dp',
                                    )
            emp_id_label = Label(text=str(supplier[2]), size_hint_x=None, width=column_widths[2], height='40dp',
                                 )
            phone_label = Label(text=supplier[3], size_hint_x=None, width=column_widths[3], height='40dp',
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
        self.popup = Popup(title='All suppliers', content=content_layout, size_hint=(None, None), size=(800, 600),
                           background_color=(0.004, 0.055, 0.102, 1.0), auto_dismiss=False)
        self.popup.open()

    def dismiss_popup(self, instance):
        if hasattr(self, 'popup') and self.popup:
            self.popup.dismiss()

    def add_supplier(self):
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

        # Create a submit button
        submit_button = Button(text='Submit', background_color=(0.133, 0.855, 0.431, 1.0))
        submit_button.bind(on_press=self.submit_supplier)
        layout.add_widget(submit_button)

        # Create a cancel button
        self.cancel_button = Button(text='Close', background_color=(0.133, 0.855, 0.431, 1.0))
        self.cancel_button.bind(on_press=self.dismiss_popup1)
        layout.add_widget(self.cancel_button)

        # Create a Popup with the layout and background color
        self.popup1 = Popup(title='Add supplier', content=layout, size_hint=(None, None), size=(720, 720),
                            background_color=(0.004, 0.055, 0.102, 1.0), auto_dismiss=False)
        self.popup1.open()

    def submit_supplier(self, instance):
        # Retrieve employee data from input fields
        first_name = self.first_name_input.text
        last_name = self.last_name_input.text
        phone = self.phone_input.text
        email = self.email_input.text
        street_address = self.street_address_input.text
        zip = self.Zip_input.text
        city = self.city_input.text
        state = self.state_input.text

        # Perform validation checks
        if not all([first_name, last_name, phone, email, street_address, city, state, zip]):
            self.show_error_popup("All fields are required.")
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
            insert_query = "INSERT INTO supplier (first_name, last_name, phone,zip, emial, street, city, state) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (
                first_name, last_name, number, zip, email, street_address, city, state))

            # Commit changes and close connection
            conn.commit()
            cursor.close()
            conn.close()

            # Show success popup
            self.show_success_popup("supplier details saved to database successfully.")

        except mysql.connector.Error as e:
            p = str(e)
            self.show_error_popup("Failed to add supplier \n{}".format(
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

    def dismiss_popup_1(self, instance=None):
        self.popup1.dismiss()

    def edit_supplier(self):
        # Create a GridLayout to organize input fields
        layout = GridLayout(cols=2, spacing=5, padding=10)

        # Add labels and input fields for user ID and password
        layout.add_widget(Label(text='last_name:', ))
        self.lastname_input = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),
                                        cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.lastname_input)

        layout.add_widget(Label(text='phone:', ))
        self.phonenumber_input = TextInput(multiline=False, password=True,
                                           background_color=(0.004, 0.055, 0.102, 1.0), cursor_color=(1, 1, 1, 1),
                                           foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.phonenumber_input)
        # Create a submit button
        submit_button = Button(text='Submit', background_color=(0.133, 0.855, 0.431, 1.0))
        submit_button.bind(on_press=self.authenticate_supplier)
        layout.add_widget(submit_button)

        # Create a Popup with the layout
        self.popup = Popup(title='Select supplier', content=layout, size_hint=(None, None),
                           background_color=(0.004, 0.055, 0.102, 1.0), size=(400, 200))
        self.popup.open()

    def authenticate_supplier(self, instance):
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
            select_query = "SELECT * FROM supplier WHERE last_name = %s AND phone = %s"
            cursor.execute(select_query, (lastname, self.add_dashes_to_number_with_existing_dashes(phone)))
            sup = cursor.fetchone()

            if sup:
                # Employee found, close current popup and display details in another popup
                self.popup.dismiss()
                self.show_supplier_details(sup)
            else:
                # Employee not found, show error message
                self.show_error_popup1("Invalid lastname or phone number.")

            cursor.close()
            conn.close()

        except mysql.connector.Error as e:
            p = str(e)
            self.show_error_popup("Failed to authenticate \n{}".format(
                p[13:].replace('Duplicate entry', 'Already Exist ').replace('supplier.', 'in ').replace('for key',
                                                                                                        '  ')))

    def show_supplier_details(self, employee):
        # Convert the tuple to a dictionary
        employee_dict = {

            'first_name': employee[1],
            'last_name': employee[2],
            'phone': employee[3],
            'email': employee[4],
            'street_address': employee[5],
            'city': employee[6],
            'state': employee[7],
            'zip': employee[8],
            'id': employee[0]
        }

        # Create a Popup to display employee details
        self.selected_employee_popup = Popup(title='Selected supplier', size_hint=(None, None), auto_dismiss=False,
                                             background_color=(0.004, 0.055, 0.102, 1.0), size=(500, 500))

        # Create a GridLayout to organize employee details
        layout = GridLayout(cols=2, spacing=5, padding=10)

        # Add labels and employee details to the layout
        for key, value in employee_dict.items():
            layout.add_widget(Label(text=str(key), ))
            layout.add_widget(Label(text=str(value), ))

        # Add an "Edit" button to allow editing employee details
        edit_button = Button(text='Edit', background_color=(0.133, 0.855, 0.431, 1.0))
        edit_button.bind(on_press=lambda instance: self.edit_supplier1(employee_dict))
        layout.add_widget(edit_button)

        # Add the layout to the popup
        self.selected_employee_popup.content = layout

        # Open the popup with employee details
        self.selected_employee_popup.open()

    def edit_supplier1(self, employee):
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

        layout.add_widget(Label(text='Phone:', ))
        self.phone_input1 = TextInput(multiline=False, text=str(values[2].replace('-', '')),
                                      background_color=(0.004, 0.055, 0.102, 1.0),
                                      cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.phone_input1)

        layout.add_widget(Label(text='Email:', ))
        self.email_input1 = TextInput(multiline=False, text=str(values[3]),
                                      background_color=(0.004, 0.055, 0.102, 1.0),
                                      cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.email_input1)

        layout.add_widget(Label(text='Street Address:', ))
        self.street_address_input1 = TextInput(multiline=True, text=str(values[4]),
                                               background_color=(0.004, 0.055, 0.102, 1.0),
                                               cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.street_address_input1)

        layout.add_widget(Label(text='City:', ))
        self.city_input1 = TextInput(multiline=False, text=str(values[5]),
                                     background_color=(0.004, 0.055, 0.102, 1.0),
                                     cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.city_input1)

        layout.add_widget(Label(text='State:', ))
        self.state_input1 = TextInput(multiline=False, text=str(values[6]),
                                      background_color=(0.004, 0.055, 0.102, 1.0),
                                      cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.state_input1)

        layout.add_widget(Label(text='Zip Code:', ))
        self.Zip_input1 = TextInput(multiline=False, text=str(values[7]),
                                    background_color=(0.004, 0.055, 0.102, 1.0),
                                    cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.Zip_input1)

        # Create a submit button
        submit_button1 = Button(text='Submit', background_color=(0.133, 0.855, 0.431, 1.0))
        submit_button1.bind(on_press=lambda instance: self.submit_supplier1(values[8]))

        layout.add_widget(submit_button1)

        # Create a cancel button
        cancel_button1 = Button(text='Close', background_color=(0.133, 0.855, 0.431, 1.0))
        cancel_button1.bind(on_press=self.dismiss_popup11)
        layout.add_widget(cancel_button1)

        # Create a Popup with the layout and background color
        self.popup11 = Popup(title='Edit Employee', content=layout, size_hint=(None, None), size=(720, 720),
                             background_color=(0.004, 0.055, 0.102, 1.0), auto_dismiss=False)
        self.popup11.open()

    def submit_supplier1(self, value):
        # Retrieve employee data from input fields
        first_name = self.first_name_input1.text
        last_name = self.last_name_input1.text
        phone = self.phone_input1.text
        email = self.email_input1.text
        street_address = self.street_address_input1.text
        zip = self.Zip_input1.text
        city = self.city_input1.text
        state = self.state_input1.text

        # Perform validation checks
        if not all(
                [first_name, last_name, phone, email, street_address, city, state, zip]):
            self.show_error_popup("All fields are required.")
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
                            UPDATE supplier
                            SET first_name = %s, last_name = %s, phone = %s, emial = %s, 
                                street = %s, zip = %s, city = %s, state = %s
                                
                            WHERE sup_id = %s
                        """
            cursor.execute(update_query, (
                first_name, last_name, phone, email, street_address, zip,
                city, state, id
            ))
            conn.commit()  # Commit the transaction

            # Close the cursor and connection
            cursor.close()
            conn.close()

            # Close the popup after update

            # Show success popup
            self.show_success_popup("supplier details \nupdated  to database successfully.")
            self.popup11.dismiss()

        except mysql.connector.Error as e:
            p = str(e)
            self.show_error_popup("Failed to add supplier\n{}".format(
                p[13:].replace('Duplicate entry', 'Already Exist ').replace('employee.', 'in ').replace('for key',
                                                                                                        '  ')))

    def show_error_popup1(self, message):
        # Display an error popup with the given message
        error_popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(300, 200))
        error_popup.open()

    def delete_supplier(self):

        # Create a GridLayout to organize input fields
        layout = GridLayout(cols=2, spacing=5, padding=10)

        # Add labels and input fields for user ID and password
        layout.add_widget(Label(text='sup_id:', ))
        self.emp_id_d = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),
                                  cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.emp_id_d)

        layout.add_widget(Label(text='phone:', ))
        self.phone_d = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),
                                 cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.phone_d)
        # Create a submit button
        submit_button = Button(text='Submit', background_color=(0.133, 0.855, 0.431, 1.0))
        submit_button.bind(on_press=self.dele_supplier)
        layout.add_widget(submit_button)
        cancel = Button(text='Cancel', background_color=(0.133, 0.855, 0.431, 1.0))
        cancel.bind(on_press=self.dismis)
        layout.add_widget(cancel)

        # Create a Popup with the layout
        self.popup111 = Popup(title='Select supplier', content=layout, auto_dismiss=False, size_hint=(None, None),
                              background_color=(0.004, 0.055, 0.102, 1.0), size=(400, 200))
        self.popup111.open()

    def dismiss_popup11(self, instance=None):
        self.popup11.dismiss()

    def dele_supplier(self, instance):
        # Retrieve user ID and password from input fields
        emp_id1 = self.emp_id_d.text.strip()
        passs1 = self.phone_d.text.strip()
        if not all([emp_id1, passs1]):
            self.show_error_popup1("All fields are required.")
            return
        if len(passs1) != 10 or not emp_id1.isdigit():
            self.show_error_popup1("Invalid suplier id number.\n supplier id must be digit")
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
            phone1 = self.add_dashes_to_number_with_existing_dashes(passs1)
            # Execute SELECT query to retrieve employee details based on user ID and password
            select_query = "DELETE FROM supplier WHERE sup_id = %s AND phone = %s"
            cursor.execute(select_query, (emp_id1, phone1))
            conn.commit()
            cursor.close()
            conn.close()

            # Show success popup
            if cursor.rowcount != 0:
                self.show_success_popup("Employee details Deleted  to database successfully.")
                self.popup111.dismiss()
            else:
                self.show_error_popup1('employee details not exist.')

        except mysql.connector.Error as e:
            p = str(e)
            self.show_error_popup("Failed to authenticate \n{}".format(
                p[13:].replace('Duplicate entry', 'Already Exist ').replace('employee.', 'in ').replace('for key',
                                                                                                        '  ')))

    def dismis(self, instance=None):
        self.popup111.dismiss()

    def fetch_products_from_database(self):
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vinay@143",
            database="grocerystore"
        )

        # Create a cursor object to execute queries
        cursor = connection.cursor()

        # Execute the query to fetch products
        cursor.execute("SELECT product_name FROM products order by product_name")

        # Fetch all the products
        products = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Extract the product names from the fetched data
        product_names = [product[0] for product in products]

        return product_names

    def delivery_details(self):
        # Fetch products from the database
        products = self.fetch_products_from_database()

        # First layout with back button
        first_layout = BoxLayout(orientation='vertical', size_hint_y=0.10, background_color=(0.004, 0.055, 0.102, 1.0))
        back_button = Button(text="Back", background_color=(0.133, 0.855, 0.431, 1.0), size_hint=(None, None),
                             size=(59, 30))
        back_button.bind(on_press=self.dismiss_popup_1)
        first_layout.add_widget(back_button)

        # Second layout with inputs
        second_layout = GridLayout(cols=4, padding=15, spacing=20, size_hint_y=0.25)
        self.delivery_id_input = TextInput(multiline=False, hint_text="Ex:1,2,3",
                                      background_color=(0.004, 0.055, 0.102, 1.0),
                                      cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        self.delivery_date_input = TextInput(multiline=False, hint_text="yyyy-mm-dd",
                                        background_color=(0.004, 0.055, 0.102, 1.0),
                                        cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        self.total_amount_input = TextInput(multiline=False, hint_text="Ex:33.3",
                                       background_color=(0.004, 0.055, 0.102, 1.0),
                                       cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        self.supplier_id_input = TextInput(multiline=False, hint_text="Ex: mail@gmail.com",
                                      background_color=(0.004, 0.055, 0.102, 1.0),
                                      cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))

        second_layout.add_widget(Label(text="Delivery ID:"))
        second_layout.add_widget(self.delivery_id_input)
        second_layout.add_widget(Label(text="Delivery Date:"))
        second_layout.add_widget(self.delivery_date_input)
        second_layout.add_widget(Label(text="Total Amount:"))
        second_layout.add_widget(self.total_amount_input)
        second_layout.add_widget(Label(text="Supplier Email_ID:"))
        second_layout.add_widget(self.supplier_id_input)

        # Third layout with dropdown and input fields
        third_layout = GridLayout(cols=5, padding=3, spacing=2, size_hint_y=0.60,
                                  background_color=(0.004, 0.055, 0.102, 1.0))
        dropdown_button = Button(text="Select Product", size_hint_y=None, size_hint_x=0.8, height=40,
                                 background_color=(0.004, 0.055, 0.102, 1.0))
        dropdown = DropDown()
        for product in products:
            btn = Button(text=product, size_hint_x=0.8, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        dropdown_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(dropdown_button, 'text', x))
        third_layout.add_widget(dropdown_button)
        self.quantity_input = TextInput(hint_text="Qnty", multiline=False, size_hint_x=0.2, size_hint_y=None,
                                   height=40, background_color=(0.004, 0.055, 0.102, 1.0),
                                   cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        self.amount_of_product_input = TextInput(hint_text="Price", multiline=False, size_hint_x=0.3, size_hint_y=None,
                                            height=40, background_color=(0.004, 0.055, 0.102, 1.0),
                                            cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        third_layout.add_widget(self.quantity_input)
        third_layout.add_widget(self.amount_of_product_input)
        second_layout2 = GridLayout(cols=4, padding=15, spacing=20, size_hint_y=0.25,
                                    background_color=(0.004, 0.055, 0.102, 1.0))
        second_layout2.add_widget(Label(text='Delivery_id'))
        second_layout2.add_widget(Label(text='product_name'))
        second_layout2.add_widget(Label(text='Quantity'))
        second_layout2.add_widget(Label(text='Amount'))
        # Fourth layout with ScrollView
        fourth_layout = GridLayout(cols=4, padding=15, spacing=20, size_hint_y=None,
                                   background_color=(0.004, 0.055, 0.102, 1.0))
        fourth_layout.bind(minimum_height=fourth_layout.setter('height'))

        # Fifth layout with "Submit Order" and "Clear" buttons
        fifth_layout = BoxLayout(orientation='horizontal', padding=10, spacing=23, size_hint_y=0.10,
                                 background_color=(0.004, 0.055, 0.102, 1.0))
        submit_order_button = Button(text="Submit Order", padding=15, size_hint_x=None, width=120,
                                     background_color=(0.133, 0.855, 0.431, 1.0))

        # List to store row-by-row values
        row_values = []

        def on_submit_order(instance):
            # Clear the list before adding new values
            row_values.clear()
            # Iterate over the widgets in fourth_layout and add their text values to row_values list
            for i in range(len(fourth_layout.children) // 4):
                row = []
                for j in range(4):
                    widget = fourth_layout.children[i * 4 + j]
                    row.append(widget.text)
                row_values.append(row)
            try:
                # Establish a connection to MySQL database
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Vinay@143",
                    database="grocerystore"
                )
                cursor = conn.cursor()
                query = "SELECT sup_id FROM supplier WHERE emial = %s"
                cursor.execute(query, [self.supplier_id_input.text, ])
                id = cursor.fetchall()
                if len(id) == 0:
                    self.show_error_popup_1(
                        "Failed to add delivery. Error: {}".format(str('email entered is wrong')))
                    return
                cursor.execute('Select * from delivery where delivery_id=%s', (self.delivery_id_input.text,))
                e = cursor.fetchall()

                if len(e) != 0:
                    self.show_error_popup_1(
                        "Failed to add delivery. Error: {}".format(str('this delivery already exist')))
                    return
                # Execute INSERT query to insert delivery details into the database
                delivery_query = "INSERT INTO delivery (delivery_id, delivery_date, total_amount, sup_id) VALUES (%s, %s, %s,%s)"
                cursor.execute(delivery_query, (
                    self.delivery_id_input.text, self.delivery_date_input.text, self.total_amount_input.text, id[0][0]))
                # Commit changes
                conn.commit()

                # Execute INSERT queries to insert detail delivery details into the database
                for r in row_values:
                    p_id = "SELECT product_id,product_available_quantity FROM products WHERE product_name = %s"
                    cursor.execute(p_id, (r[2],))
                    r_data = cursor.fetchall()
                    conn.commit()
                    sum = float(r_data[0][1]) + float(r[1])

                    u_q = 'UPDATE PRODUCTS SET product_available_quantity=%s where product_id=%s'
                    cursor.execute(u_q, (sum, r_data[0][0]))
                    detail_delivery_query = "INSERT INTO detail_delivery (delivery_id, product_id, quantity, amount_of_product) VALUES (%s,%s, %s, %s)"
                    detail_delivery_data = (r[3], r_data[0][0], r[1], r[0])
                    cursor.execute(detail_delivery_query, detail_delivery_data)
                    # Commit changes for each row
                    conn.commit()

                # Close cursor and connection
                cursor.close()
                conn.close()

                # Show success popup
                self.show_success_popup_1("Delivery details saved to database successfully.")

            except mysql.connector.Error as e:
                # Show error popup
                print(e)
                self.show_error_popup_1("Failed to add delivery. Error: {}".format(str(e)))

        submit_order_button.bind(on_release=on_submit_order)
        submit_order_button.disabled = True
        fifth_layout.add_widget(submit_order_button)

        def on_clear(instance):
            # Clear the content of fourth layout
            fourth_layout.clear_widgets()
            # Enable input fields in layout 2

            self.delivery_id_input.disabled = False
            self.delivery_date_input.disabled = False
            self.total_amount_input.disabled = False
            self.supplier_id_input.disabled = False
            self.delivery_id_input.clear_widgets()
            self.delivery_date_input.clear_widgets()
            self.total_amount_input.clear_widgets()
            self.supplier_id_input.clear_widgets()
            self.quantity_input.clear_widgets()
            self.amount_of_product_input.clear_widgets()
        clear_button = Button(text="Clear", background_color=(0.133, 0.855, 0.431, 1.0), padding=15, size_hint_x=None,
                              width=120)
        clear_button.bind(on_release=on_clear)
        fifth_layout.add_widget(clear_button)
        submit_order_button.disabled = True

        # Disable input fields in layout 2 when Submit Product button is clicked
        def on_submit(instance):
            # Check if all fields in layout 2 are filled
            if not all([self.delivery_id_input.text, self.delivery_date_input.text, self.total_amount_input.text,
                        self.supplier_id_input.text]):
                show_error_popup("Please fill in all fields .")
                return

            # Check if the dropdown, quantity, and amount fields in layout 3 are filled
            if dropdown_button.text == "Select Product" or not self.quantity_input.text or not self.amount_of_product_input.text:
                show_error_popup("Please select a product and fill in the quantity and amount fields ")
                return

            # Perform additional validations
            delivery_id = self.delivery_id_input.text
            delivery_date = self.delivery_date_input.text
            total_amount = self.total_amount_input.text
            supplier_id = self.supplier_id_input.text
            quantity = self.quantity_input.text
            amount_of_product = self.amount_of_product_input.text

            if not delivery_id.isdigit():
                show_error_popup("Delivery ID must be an integer.")
                return

            try:
                datetime.strptime(delivery_date, "%Y-%m-%d")
            except ValueError:
                show_error_popup("Delivery date must be in the format YYYY-MM-DD.")
                return

            try:
                float(total_amount)
            except ValueError:
                show_error_popup("Total amount must be a float.")
                return

            if not re.match(r".+@gmail\.com$", supplier_id):
                show_error_popup("Supplier ID must end with @gmail.com.")
                return

            if not quantity.isdigit():
                show_error_popup("Quantity must be an integer.")
                return

            try:
                float(amount_of_product)
            except ValueError:
                show_error_popup("Amount must be a float.")
                return

            # Disable input fields in layout 2
            self.delivery_id_input.disabled = True
            self.delivery_date_input.disabled = True
            self.total_amount_input.disabled = True
            self.supplier_id_input.disabled = True

            # Add data to fourth layout
            fourth_layout.add_widget(Label(text=str(delivery_id)))
            fourth_layout.add_widget(Label(text=dropdown_button.text))
            fourth_layout.add_widget(Label(text=str(quantity)))
            fourth_layout.add_widget(Label(text=str(amount_of_product)))
            submit_order_button.disabled = False

        def show_error_popup(message):
            popup = Popup(title='Error', background_color=(0.004, 0.055, 0.102, 1.0), content=Label(text=message),
                          size_hint=(None, None), size=(400, 200))
            popup.open()

        submit_button = Button(text="Submit Product", size=(30, 30), background_color=(0.133, 0.855, 0.431, 1.0))
        submit_button.bind(on_release=on_submit)

        # ScrollView for fourth layout
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
        scroll_view.add_widget(fourth_layout)

        # Create the popup
        popup_content = GridLayout(cols=1, background_color=(0.004, 0.055, 0.102, 1.0))
        popup_content.add_widget(first_layout)
        popup_content.add_widget(second_layout)

        # Add submit button beside third layout
        submit_container = GridLayout(cols=2, padding=15, spacing=20, size_hint_y=None,
                                      background_color=(0.004, 0.055, 0.102, 1.0))
        submit_container.add_widget(third_layout)
        submit_container.add_widget(submit_button)
        popup_content.add_widget(submit_container)
        popup_content.add_widget(second_layout2)
        popup_content.add_widget(scroll_view)
        popup_content.add_widget(fifth_layout)

        self.popup = Popup(title='My Popup', content=popup_content, size_hint=(None, None), auto_dismiss=False,
                           size=(900, 890), background_color=(0.004, 0.055, 0.102, 1.0))
        self.popup.open()

    def show_success_popup_1(self, message):
        # Display a success popup with the given message
        success_popup = Popup(title='Success', content=Label(text=message), size_hint=(None, None), size=(300, 200))
        success_popup.open()

    def show_error_popup_1(self, message):
        # Display an error popup with the given message
        popup_width = len(message) * 10  # Adjust the multiplier based on your preference
        popup_height = max(len(message) // 15,
                           1) * 40  # Adjust the divisor and multiplier based on your preference

        error_popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None),
                            size=(popup_width, popup_height,))
        error_popup.open()
    def dismiss_popup1(self, instance):
        if self.popup1:
            self.popup1.dismiss()

    def dismiss_popup_1(self,instance=None):
        self.popup.dismiss()
