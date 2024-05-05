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


class Orders(Screen):
    def show_all_orders(self):
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
        cursor.execute(
            "select product_id, product_name, weight_of_product,product_price,product_available_quantity from products order by product_available_quantity ")
        order = cursor.fetchall()

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
        labels_layout.add_widget(Label(text='product_id', size_hint_x=None, width=column_widths[0]))
        labels_layout.add_widget(Label(text='product name', size_hint_x=None, width=column_widths[1]))
        labels_layout.add_widget(Label(text='product_weight', size_hint_x=None, width=column_widths[2]))
        labels_layout.add_widget(Label(text='price', size_hint_x=None, width=column_widths[3]))
        labels_layout.add_widget(Label(text='available_qty', size_hint_x=None, width=column_widths[3]))
        # Add labels layout to content layout
        content_layout.add_widget(labels_layout)

        # Create a ScrollView with GridLayout inside to allow scrolling
        layout = GridLayout(cols=5, size_hint_y=None, padding=10, spacing=40)
        layout.bind(minimum_height=layout.setter('height'))

        # Add employee data
        for ord in order:
            p_id = Label(text=str(ord[0]), size_hint_x=None, width=column_widths[0], height='40dp',
                         )
            p_name = Label(text=str(ord[1]), size_hint_x=None, width=column_widths[1], height='40dp',
                           )
            p_weight = Label(text=str(ord[2]), size_hint_x=None, width=column_widths[2], height='40dp',
                             )
            p_price = Label(text=str(ord[3]), size_hint_x=None, width=column_widths[3], height='40dp',
                            )
            p_q_a = Label(text=str(ord[4]), size_hint_x=None, width=column_widths[3], height='40dp',
                          )

            layout.add_widget(p_id)
            layout.add_widget(p_name)
            layout.add_widget(p_weight)
            layout.add_widget(p_price)
            layout.add_widget(p_q_a)

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
        self.popup = Popup(title='Order list', content=content_layout, size_hint=(None, None), size=(950, 600),
                           background_color=(0.004, 0.055, 0.102, 1.0), auto_dismiss=False)
        self.popup.open()

    def dismiss_popup(self, instance):
        if hasattr(self, 'popup') and self.popup:
            self.popup.dismiss()

    def order_id_check(self):
        # Create the first layout with the back button
        first_layout = GridLayout(cols=1, padding=10, size_hint_y=0.06, background_color=(0.004, 0.055, 0.102, 1.0))
        back_button = Button(text='cancel', size_hint=(None, None), size=(59, 30), background_color=(1, 0, 0, 1))

        # Define callback function for the back button
        def back_callback(instance):
            popup.dismiss()

        # Bind the callback function to the back button
        back_button.bind(on_release=back_callback)

        # Add the back button to the first layout
        first_layout.add_widget(back_button)

        # Create the second layout with input fields and submit button
        second_layout = GridLayout(cols=2, padding=15, spacing=15, size_hint_y=0.20,
                                   background_color=(0.004, 0.055, 0.102, 1.0))
        last_name_input = TextInput(hint_text='Last Name', background_color=(0.004, 0.055, 0.102, 1.0),
                                    cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        phone_input = TextInput(hint_text='Phone Number', background_color=(0.004, 0.055, 0.102, 1.0),
                                cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        submit_button = Button(text='Submit', background_color=(0.133, 0.855, 0.431, 1.0))

        # Define callback function for the submit button
        def submit_callback(instance):
            last_name = last_name_input.text
            phone_number = phone_input.text
            if not all([phone_number, last_name]):
                self.show_error_popup("All fields are required.")
                return
            if len(phone_number) != 10 or not phone_number.isdigit():
                self.show_error_popup("Invalid phone number.\n Phone number must be 10 digits.")
                return
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Vinay@143",
                    database="grocerystore"
                )
                phone = self.add_dashes_to_number_with_existing_dashes(phone_number)
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT order_id, order_date, total_amount,case when payment_id=1 then 'cash' else 'QR code' end as payment_id"
                    " FROM orders where customer_id=(select  customer_id from customer where last_name=%s and cus_number=%s) order by order_date desc",
                    (last_name, phone))
                orders = cursor.fetchall()

                # Add order details to ScrollView
                scroll_layout = GridLayout(cols=4, padding=20, spacing=20, size_hint_y=None,
                                           background_color=(0.004, 0.055, 0.102, 1.0))
                scroll_layout.bind(
                    minimum_height=scroll_layout.setter('height'))  # Allow ScrollView to scroll vertically
                scroll_layout.clear_widgets()
                for order in orders:
                    for detail in order:
                        scroll_layout.add_widget(Label(text=str(detail)))

                cursor.close()
                connection.close()

                # Create a ScrollView and add the scrollable layout to it
                scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
                scroll_view.add_widget(scroll_layout)

                # Add labels layout and ScrollView to the third layout
                third_layout.clear_widgets()  # Clear previous content
                third_layout.add_widget(labels_layout)
                third_layout.add_widget(scroll_view)


            except mysql.connector.Error as e:

                p = str(e)

                self.show_error_popup("Failed to get orders \n{}".format(

                    p[13:].replace('Duplicate entry', 'Already Exist ').replace('employee.', 'in ').replace('for key',

                                                                                                            '  ')))

        # Bind the callback function to the submit button
        submit_button.bind(on_release=submit_callback)

        # Add input fields and submit button to the second layout
        second_layout.add_widget(last_name_input)
        second_layout.add_widget(phone_input)
        second_layout.add_widget(submit_button)

        # Create the third layout with labels and ScrollView
        third_layout = GridLayout(cols=1, padding=2, size_hint_y=0.81, background_color=(0.004, 0.055, 0.102, 1.0))
        labels_layout = GridLayout(cols=4, padding=5, spacing=5, size_hint_y=0.05,
                                   background_color=(0.004, 0.055, 0.102, 1.0))
        labels_layout.add_widget(Label(text='Order ID', ))
        labels_layout.add_widget(Label(text='Order Date', ))
        labels_layout.add_widget(Label(text='Total Amount', ))
        labels_layout.add_widget(Label(text='Payment Method', ))

        # Create the popup window
        popup = Popup(title='customers orders details', auto_dismiss=False, size_hint=(None, None), size=(700, 700),
                      background_color=(0.004, 0.055, 0.102, 1.0))

        # Combine the layouts in a parent layout
        parent_layout = GridLayout(cols=1)
        parent_layout.add_widget(first_layout)
        parent_layout.add_widget(second_layout)
        parent_layout.add_widget(third_layout)

        # Set the parent layout as the content of the popup
        popup.content = parent_layout

        # Set the position of the back button to the top right corner
        back_button.pos_hint = {'right': 1, 'top': 1}

        # Open the popup
        popup.open()

    def add_dashes_to_number_with_existing_dashes(self, number):
        # Convert number to string
        number_str = str(number)

        # Use regular expression to add dashes after every three digits for the first two groups
        # and after every four digits for the last group
        formatted_number = re.sub(r'(\d{3})(\d{3})(\d{4})', r'\1-\2-\3', number_str)

        return formatted_number

    def show_error_popup(self, message):
        # Display an error popup with the given message
        popup_width = len(message) * 10  # Adjust the multiplier based on your preference
        popup_height = max(len(message) // 15,
                           1) * 40  # Adjust the divisor and multiplier based on your preference

        error_popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None),
                            size=(popup_width, popup_height))
        error_popup.open()

    def order_check(self):
        # Create the first layout with the back button
        first_layout = GridLayout(cols=1, padding=10, size_hint_y=0.06, background_color=(0.004, 0.055, 0.102, 1.0))
        back_button = Button(text='cancel', size_hint=(None, None), size=(59, 30), background_color=(1, 0, 0, 1))

        # Define callback function for the back button
        def back_callback(instance):
            popup.dismiss()

        # Bind the callback function to the back button
        back_button.bind(on_release=back_callback)

        # Add the back button to the first layout
        first_layout.add_widget(back_button)

        # Create the second layout with input fields and submit button
        second_layout = GridLayout(cols=2, padding=15, spacing=15, size_hint_y=0.10,
                                   background_color=(0.004, 0.055, 0.102, 1.0))
        last_name_input = TextInput(hint_text='Enter order_id', background_color=(0.004, 0.055, 0.102, 1.0),
                                    cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1))
        submit_button = Button(text='Search', background_color=(0.133, 0.855, 0.431, 1.0))

        # Define callback function for the submit button
        def submit_callback(instance):
            last_name = last_name_input.text
            if not all(last_name):
                self.show_error_popup("All fields are required.")
                return
            if not last_name.isdigit():
                self.show_error_popup("Invalid order number.\n order number must be a digits.")
                return
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Vinay@143",
                    database="grocerystore"
                )

                cursor = connection.cursor()
                cursor.execute(
                    " select product_name,weight_of_product,product_price ,quantity_of_product,amount_of_product from orders o join order_items_summary os on o.order_id=os.order_id join products p on p.product_id=os.product_id where o.order_id=%s",
                    [last_name, ])
                orders = cursor.fetchall()
                cursor.execute(
                    " select  order_date,total_amount from orders where order_id=%s",
                    [last_name, ])
                orderd = cursor.fetchone()
                if orderd!= None:
                    l2.text = str(orderd[0])
                    l4.text = str(orderd[1])

                # Add order details to ScrollView
                scroll_layout = GridLayout(cols=5, padding=23, spacing=23, size_hint_y=None,
                                           background_color=(0.004, 0.055, 0.102, 1.0))
                scroll_layout.bind(
                    minimum_height=scroll_layout.setter('height'))  # Allow ScrollView to scroll vertically
                scroll_layout.clear_widgets()
                for order in orders:
                    for detail in order:
                        scroll_layout.add_widget(Label(text=str(detail)))

                cursor.close()
                connection.close()

                # Create a ScrollView and add the scrollable layout to it
                scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
                scroll_view.add_widget(scroll_layout)

                # Add labels layout and ScrollView to the third layout
                third_layout.clear_widgets()  # Clear previous content
                third_layout.add_widget(labels_layout)
                third_layout.add_widget(scroll_view)


            except mysql.connector.Error as e:
                print(e)

                p = str(e)

                self.show_error_popup("Failed to get orders \n{}".format(

                    p[13:].replace('Duplicate entry', 'Already Exist ').replace('employee.', 'in ').replace('for key',

                                                                                                            '  ')))

        # Bind the callback function to the submit button
        submit_button.bind(on_release=submit_callback)

        # Add input fields and submit button to the second layout
        second_layout.add_widget(last_name_input)
        second_layout.add_widget(submit_button)
        second_layout2 = GridLayout(cols=4, padding=20, spacing=20, size_hint_y=0.10,
                                    background_color=(0.004, 0.055, 0.102, 1.0))
        l1 = Label(text='order date')
        l2 = Label(text=' ', )
        l3 = Label(text='total_amount', )
        l4 = Label(text='', )
        second_layout2.add_widget(l1)
        second_layout2.add_widget(l2)
        second_layout2.add_widget(l3)
        second_layout2.add_widget(l4)

        # Create the third layout with labels and ScrollView
        third_layout = GridLayout(cols=1, padding=2, size_hint_y=0.81, background_color=(0.004, 0.055, 0.102, 1.0))
        labels_layout = GridLayout(cols=5, padding=5, spacing=5, size_hint_y=0.05,
                                   background_color=(0.004, 0.055, 0.102, 1.0))
        labels_layout.add_widget(Label(text='product_name',))
        labels_layout.add_widget(Label(text='prdouct_weight', ))
        labels_layout.add_widget(Label(text='product_price', ))
        labels_layout.add_widget(Label(text='product_quantity', ))
        labels_layout.add_widget(Label(text='total_of_product', ))

        # Create the popup window
        popup = Popup(title='customers orders details', auto_dismiss=False, size_hint=(None, None), size=(750, 750),
                      background_color=(0.004, 0.055, 0.102, 1.0))

        # Combine the layouts in a parent layout
        parent_layout = GridLayout(cols=1)
        parent_layout.add_widget(first_layout)
        parent_layout.add_widget(second_layout)
        parent_layout.add_widget(second_layout2)
        parent_layout.add_widget(third_layout)

        # Set the parent layout as the content of the popup
        popup.content = parent_layout

        # Set the position of the back button to the top right corner
        back_button.pos_hint = {'right': 1, 'top': 1}

        # Open the popup
        popup.open()
