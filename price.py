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


class Price(Screen):

    def show_all_products(self):
        # Establish a connection to your MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vinay@143",
            database='grocerystore'
        )
        cursor = conn.cursor()

        # Fetch specific columns (first_name, last_name, emp_id, phone) from the database
        cursor.execute(
            "SELECT PRODUCT_ID,PRODUCT_NAME,WEIGHT_OF_PRODUCT,PRODUCT_PRICE,PRODUCT_AVAILABLE_QUANTITY FROM PRODUCTS")
        PRODUCTS_data = cursor.fetchall()
        # Close the database connection
        cursor.close()
        conn.close()

        # Create a BoxLayout to organize the labels and the scroll view
        content_layout = BoxLayout(orientation='vertical', padding=10, spacing=40,
                                   background_color=(0.004, 0.055, 0.102, 1.0))

        # Create a GridLayout for the labels
        labels_layout = GridLayout(cols=5, size_hint_y=None, height='40dp', padding=10, spacing=40)

        # Set fixed widths for columns
        column_widths = [150, 150, 150, 150]

        # Add column labels
        labels_layout.add_widget(Label(text='PRODUCT_ID', size_hint_x=None, width=column_widths[0]))
        labels_layout.add_widget(Label(text='PRODUCT_NAME', size_hint_x=None, width=column_widths[1]))
        labels_layout.add_widget(Label(text='WEIGHT', size_hint_x=None, width=column_widths[2]))
        labels_layout.add_widget(Label(text='PRICE', size_hint_x=None, width=column_widths[3]))
        labels_layout.add_widget(Label(text='REMANING_QUANTITY', size_hint_x=None, width=column_widths[3]))

        # Add labels layout to content layout
        content_layout.add_widget(labels_layout)

        # Create a ScrollView with GridLayout inside to allow scrolling
        layout = GridLayout(cols=5, size_hint_y=None, padding=10, spacing=40)
        layout.bind(minimum_height=layout.setter('height'))

        # Add employee data
        for product in PRODUCTS_data:
            id = Label(text=str(product[0]), size_hint_x=None, width=column_widths[0], height='40dp',
                       )
            name = Label(text=product[1], size_hint_x=None, width=column_widths[1], height='40dp',
                         )
            weight = Label(text=product[2], size_hint_x=None, width=column_widths[2], height='40dp',
                           )
            price = Label(text=str(product[3]), size_hint_x=None, width=column_widths[3], height='40dp',
                          )
            quantity = Label(text=str(product[4]), size_hint_x=None, width=column_widths[3], height='40dp',
                             )

            layout.add_widget(id)
            layout.add_widget(name)
            layout.add_widget(weight)
            layout.add_widget(price)
            layout.add_widget(quantity)

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
        self.popup = Popup(title='All Products', content=content_layout, size_hint=(None, None), size=(940, 700),
                           background_color=(0.004, 0.055, 0.102, 1.0), auto_dismiss=False)
        self.popup.open()

    def dismiss_popup(self, instance):
        if hasattr(self, 'popup') and self.popup:
            self.popup.dismiss()

    def edit_prdouct(self):
        # Create a GridLayout to organize input fields
        layout = GridLayout(cols=2, spacing=5, padding=10)

        # Add labels and input fields for user ID and password
        layout.add_widget(Label(text='product_id:', ))
        self.product_id = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),
                                    cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.product_id)

        layout.add_widget(Label(text='product_name', ))
        self.product_name = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),
                                      cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.product_name)
        # Create a submit button
        submit_button1 = Button(text='Submit', background_color=(0.133, 0.855, 0.431, 1.0))
        submit_button1.bind(on_press=self.authenticate_product)
        layout.add_widget(submit_button1)

        # Create a Popup with the layout
        self.popup = Popup(title='Select product', content=layout, size_hint=(None, None),
                           background_color=(0.004, 0.055, 0.102, 1.0), size=(400, 200))
        self.popup.open()

    def authenticate_product(self, instance):
        # Retrieve user ID and password from input fields
        proid = self.product_id.text.strip()
        proname = self.product_name.text.strip()
        if not all([proname, proid]):
            self.show_error_popup("All fields are required.")
            return
        if not proid.isdigit():
            self.show_error_popup("Invalid product id  number.\n product id  number must be digits.")
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
            select_query = "SELECT * FROM products WHERE product_name = %s AND product_id = %s"
            cursor.execute(select_query, (proname, proid))
            product_e = cursor.fetchone()

            if product_e:
                # product found, close current popup and display details in another popup
                self.popup.dismiss()
                self.show_product_details(product_e)
            else:
                # Employee not found, show error message
                self.show_error_popup("Invalid product_id or product_name.")

            cursor.close()
            conn.close()

        except mysql.connector.Error as e:
            p = str(e)
            self.show_error_popupp("Failed to authenticate \n{}".format(
                p[13:].replace('Duplicate entry', 'Already Exist ').replace('employee.', 'in ').replace('for key',
                                                                                                        '  ')))

    def show_product_details(self, products):
        # Convert the tuple to a dictionary
        employee_dict = {

            'product_id': products[0],
            'product_name': products[1],
            'weight': products[2],
            'pprice': products[3],
            'available_quantity': products[4],
        }

        # Create a Popup to display employee details
        self.selected_employee_popup = Popup(title='Selected product', size_hint=(None, None), auto_dismiss=False,
                                             background_color=(0.004, 0.055, 0.102, 1.0), size=(500, 500))

        # Create a GridLayout to organize employee details
        layout = GridLayout(cols=2, spacing=5, padding=10)

        # Add labels and employee details to the layout
        for key, value in employee_dict.items():
            layout.add_widget(Label(text=str(key), ))
            layout.add_widget(Label(text=str(value), ))

        # Add an "Edit" button to allow editing employee details
        edit_button = Button(text='Edit', background_color=(0.133, 0.855, 0.431, 1.0))
        edit_button.bind(on_press=lambda instance: self.edit_product1(employee_dict))
        layout.add_widget(edit_button)

        # Add the layout to the popup
        self.selected_employee_popup.content = layout

        # Open the popup with employee details
        self.selected_employee_popup.open()

    def edit_product1(self, product):
        self.selected_employee_popup.dismiss()
        values = list(product.values())
        # Create a GridLayout to organize input fields
        layout = GridLayout(cols=2, spacing=10, padding=10, background_color=(0.004, 0.055, 0.102, 1.0))
        # Add labels and input fields for each attribute
        layout.add_widget(Label(text='Product_id:', ))
        self.productid = TextInput(multiline=False, text=str(values[0]),
                                   background_color=(0.004, 0.055, 0.102, 1.0),
                                   cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.productid)

        layout.add_widget(Label(text='Product_name:', ))
        self.productname = TextInput(multiline=False, text=str(values[1]),
                                     background_color=(0.004, 0.055, 0.102, 1.0),
                                     cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.productname)

        layout.add_widget(Label(text='Weight of product :', ))
        self.Weightofproduct = TextInput(multiline=False, text=str(values[2]),
                                         background_color=(0.004, 0.055, 0.102, 1.0),
                                         cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.Weightofproduct)

        layout.add_widget(Label(text='Price:', ))
        self.priceofproduct = TextInput(multiline=False, text=str(values[3]),
                                        background_color=(0.004, 0.055, 0.102, 1.0),
                                        cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.priceofproduct)

        layout.add_widget(Label(text='Quantity available:', ))
        self.quantityavailable = TextInput(multiline=False, text=str(values[4]),
                                           background_color=(0.004, 0.055, 0.102, 1.0),
                                           cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.quantityavailable)
        # Create a submit button
        submit_buttonp = Button(text='Submit', background_color=(0.133, 0.855, 0.431, 1.0))
        submit_buttonp.bind(on_press=lambda instance: self.submit_product1(values[0]))

        layout.add_widget(submit_buttonp)

        # Create a cancel button
        cancel_buttonp = Button(text='Close', background_color=(0.133, 0.855, 0.431, 1.0))
        cancel_buttonp.bind(on_press=self.dismiss_popupp)
        layout.add_widget(cancel_buttonp)

        # Create a Popup with the layout and background color
        self.popup11 = Popup(title='Edit product', content=layout, size_hint=(None, None), size=(720, 720),
                             background_color=(0.004, 0.055, 0.102, 1.0), auto_dismiss=False)
        self.popup11.open()

    def submit_product1(self, value):
        # Retrieve employee data from input fields
        p_id = self.productid.text
        p_name = self.productname.text
        weight_p = self.Weightofproduct.text
        price_p = self.priceofproduct.text
        quantity_p = self.quantityavailable.text
        # replacing the kg,grams
        new_weight = self.Weightofproduct.text.replace('kg', '').replace('grams', '')
        # Perform validation checks
        if not all(
                [p_id, p_name, weight_p, price_p, quantity_p]):
            self.show_error_popup("All fields are required.")
            return
        if not p_id.isdigit():
            self.show_error_popup("Invalid id.\n id  number must be number.")
            return
        if not isinstance(float(price_p), float):
            self.show_error_popup("Invalid price number.\n price number must be digits.")
            return

        weight_parts = weight_p.split(' ')
        if len(weight_parts) != 2:
            self.show_error_popup("Invalid weight format.\n Please use format like '250 grams'.")
            return

        # Check if the first part is a number
        if not weight_parts[0].isdigit():
            self.show_error_popup("Invalid weight format.\n First part of weight must be a number.")
            return

        # Check if the second part is a valid unit
        if weight_parts[1] not in ('kg', 'grams', 'liter', 'ml'):
            self.show_error_popup("Invalid weight unit.\n Valid units are: kg, grams, liter, ml.")
            return
        if not quantity_p.isdigit():
            self.show_error_popup("Invalid quantity .\nquantity must be digit")
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

            id = value

            # Construct the UPDATE query
            update_query = """
                        UPDATE products
                        SET product_id= %s, product_name = %s, weight_of_product = %s, product_price = %s,product_available_quantity = %s
                            
                        WHERE product_id = %s
                    """
            cursor.execute(update_query, (p_id, p_name, weight_p, float(price_p), float(quantity_p), id
                                          ))
            conn.commit()  # Commit the transaction

            # Close the cursor and connection
            cursor.close()
            conn.close()

            # Close the popup after update

            # Show success popup
            self.show_success_popup("product details \nupdated  to database successfully.")
            self.popup11.dismiss()

        except mysql.connector.Error as e:
            p = str(e)
            self.show_error_popup("Failed to update product \n{}".format(
                p[13:].replace('Duplicate entry', 'Already Exist ').replace('employee.', 'in ').replace('for key',
                                                                                                        '  ')))

    def add_product(self):
        # Create a GridLayout to organize input fields
        layout = GridLayout(cols=2, spacing=10, padding=10, background_color=(0.004, 0.055, 0.102, 1.0))

        # Add labels and input fields for each attribute

        layout.add_widget(Label(text='Product_name:', ))
        productname = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),
                                cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(productname)

        layout.add_widget(Label(text='Weight of product :', ))
        weightofproduct = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),
                                    cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(weightofproduct)

        layout.add_widget(Label(text='Price:', ))
        priceofproduct = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),
                                   cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(priceofproduct)

        layout.add_widget(Label(text='Quantity available:', ))
        quantityavailable = TextInput(multiline=False, background_color=(0.004, 0.055, 0.102, 1.0),
                                      cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(quantityavailable)

        # Create a submit button
        submit_buttonp = Button(text='Submit', background_color=(0.133, 0.855, 0.431, 1.0))
        submit_buttonp.bind(
            on_press=lambda instance: self.submit_product2(productname.text, weightofproduct.text,
                                                           priceofproduct.text, quantityavailable.text))

        layout.add_widget(submit_buttonp)

        # Create a cancel button
        cancel_buttonp = Button(text='Close', background_color=(0.133, 0.855, 0.431, 1.0))
        cancel_buttonp.bind(on_press=self.dismiss_popupp1)
        layout.add_widget(cancel_buttonp)

        # Create a Popup with the layout and background color
        self.popup = Popup(title='Add Product', content=layout, size_hint=(None, None), size=(720, 720),
                           background_color=(0.004, 0.055, 0.102, 1.0), auto_dismiss=False)
        self.popup.open()

    def submit_product2(self, p_name, weight_p, price_p, quantity_p):
        # Perform validation checks
        if not all([p_name, weight_p, price_p, quantity_p]):
            self.show_error_popup("All fields are required.")
            return
        if not isinstance(float(price_p), float):
            self.show_error_popup("Invalid price.\n price must be digits.")
            return
        weight_parts = weight_p.split(' ')
        if len(weight_parts) != 2:
            self.show_error_popup("Invalid weight format.\n Please use format like '250 grams'.")
            return

        # Check if the first part is a number
        if not weight_parts[0].isdigit():
            self.show_error_popup("Invalid weight format.\n First part of weight must be a number.")
            return

        # Check if the second part is a valid unit
        if weight_parts[1] not in ('kg', 'grams', 'liter', 'ml'):
            self.show_error_popup("Invalid weight unit.\n Valid units are: kg, grams, liter, ml.")
            return
        if not quantity_p.isdigit():
            self.show_error_popup("Invalid quantity.\n quantity must be digit.")
            return

        try:
            # Establish a connection to MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Vinay@143",
                database="grocerystore"
            )
            cursor = conn.cursor()

            # Check if the product ID already exists
            cursor.execute("SELECT * FROM products WHERE product_name = %s", (p_name,))
            existing_product = cursor.fetchone()

            if existing_product:
                self.show_error_popup("Product with ID {} already exists.".format(p_name))
                return

            # Construct the INSERT query
            insert_query = """
                            INSERT INTO products (product_name, weight_of_product, product_price, product_available_quantity)
                            VALUES (%s, %s, %s, %s)
                        """
            cursor.execute(insert_query, (p_name, weight_p, price_p, quantity_p))
            conn.commit()  # Commit the transaction

            # Close the cursor and connection
            cursor.close()
            conn.close()

            # Close the popup after successful addition
            self.dismiss_popupp1()

            # Show success popup
            self.show_success_popup("Product added to database successfully.")

        except mysql.connector.Error as e:
            p = str(e)
            self.show_error_popup("Failed to add product.\n{}".format(
                p[13:].replace('Duplicate entry', 'Already Exist ').replace('employee.', 'in ').replace('for key',
                                                                                                        '  ')))

    def show_error_popup(self, message):
        # Display an error popup with the given message
        error_popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(300, 200))
        error_popup.open()

    def dismiss_popupp(self, instance=None):
        self.popup11.dismiss()

    def dismiss_popupp1(self, instance=None):
        self.popup.dismiss()

    def show_success_popup(self, message):
        # Display a success popup with the given message
        success_popup = Popup(title='Success', content=Label(text=message), size_hint=(None, None), size=(300, 200))
        success_popup.open()
