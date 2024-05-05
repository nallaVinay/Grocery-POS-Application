import re
import time
import mysql.connector
import datetime
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
import smtplib
import ssl
from email.message import EmailMessage
global id


class SecondWindow(Screen):
    def __init__(self, **kwargs):
        # Extract the 'id' argument if it's provided
        user_id = kwargs.pop('id', None)

        # Call the superclass's __init__ method
        super(SecondWindow, self).__init__(**kwargs)

        # Your initialization code here
        if user_id:
            global id
            id = user_id

    # Dictionary to store button name, price, and click count
    button_info = {}

    def show_customer_details_popup(self):
        # Create a popup
        self.popup = Popup(title='Customer Details', size_hint=(None, None), size=(500, 300),background_color=(0.004,0.055,0.102,1.0))

        # Layout for the popup content
        layout = GridLayout(cols=2, spacing=10, padding=10)

        # Text inputs for first name, last name, phone, and email
        self.first_name_input = TextInput(hint_text='First Name', height=35, multiline=False)
        self.last_name_input = TextInput(hint_text='Last Name', height=35, multiline=False)
        self.phone_input = TextInput(hint_text='Phone', height=35, multiline=False)
        self.email_input = TextInput(hint_text='Email', height=35, multiline=False)

        # Dropdown for payment method
        self.payment_dropdown = DropDown()
        payment_options = ['Cash', 'QR code']
        for option in payment_options:
            btn = Button(text=option, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.update_payment_button_text(btn.text))
            self.payment_dropdown.add_widget(btn)

        self.payment_button = Button(text='Payment Method',background_color=(0.53, 0.81, 0.92, 1),size_hint=(None, None), size=(150, 44))
        self.payment_button.bind(on_release=self.payment_dropdown.open)

        # Submit button
        submit_button = Button(text='Submit',background_color=(0.133, 0.855, 0.431, 1.0), size_hint=(None, None), size=(150, 44))
        submit_button.bind(on_press=lambda instance: self.display_button_info())

        # Add widgets to the layout
        layout.add_widget(self.first_name_input)
        layout.add_widget(self.last_name_input)
        layout.add_widget(self.phone_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.payment_button)
        layout.add_widget(submit_button)

        self.popup.content = layout
        self.popup.open()

        return self.popup

    # Function to update payment button text
    def update_payment_button_text(self, option):
        self.payment_button.text = option
        self.payment_dropdown.dismiss()

    def build_buttons(self):
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vinay@143",
            database="grocerystore"
        )
        cursor = connection.cursor()

        # Fetch data from the database
        cursor.execute("SELECT concat(product_name,weight_of_product),product_price from products order by product_name")
        data = cursor.fetchall()

        # Close database connection
        cursor.close()
        connection.close()

        # Clear existing widgets
        self.ids.buttons.clear_widgets()

        # Create buttons dynamically based on the data retrieved from the database
        for name, price in data:
            button = Button(text=f"{name.replace('grams','gm')}\nPrice: {price}", size_hint_y=None, height=40,
                            background_color=(0.8, 0.6, 0.2, 1.0))
            button.bind(on_press=self.add_selected_item)
            self.ids.buttons.add_widget(button)

    def insert_order(self, customer_id, id, payment, total):
        # Get the present date
        present_date = datetime.datetime.now().date()

        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vinay@143",
            database="grocerystore"
        )
        cursor = connection.cursor()

        try:
            # Insert order details into the orders table
            cursor.execute("INSERT INTO orders (emp_id,customer_id,order_date,total_amount,payment_id) "
                           "VALUES (%s, %s, %s, %s, %s)",
                           (id, customer_id, present_date, float(total), payment))
            connection.commit()

            # Get the ID of the newly inserted order
            order_id = cursor.lastrowid

        except mysql.connector.Error as err:
            # Handle error
            print("Error:", err)
            order_id = None

        finally:
            # Close cursor and connection
            cursor.close()
            connection.close()

        return order_id

    def insert_data(self, first_name, last_name, phone, email):
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vinay@143",
            database="grocerystore"
        )
        cursor = connection.cursor()

        try:
            phone = self.add_dashes_to_number_with_existing_dashes(phone)
            # Check if customer already exists based on email
            cursor.execute("SELECT customer_id FROM customer WHERE email = %s and cus_number=%s", (email, phone))
            existing_customer = cursor.fetchone()

            if existing_customer:
                # Customer already exists, return the customer ID
                customer_id = existing_customer[0]
            else:
                # Insert new customer into database
                phone = self.add_dashes_to_number_with_existing_dashes(phone)
                cursor.execute("INSERT INTO customer (first_name, last_name, cus_number, email) "
                               "VALUES (%s, %s, %s, %s)",
                               (first_name, last_name, phone, email))
                connection.commit()

                # Get the ID of the newly inserted customer
                customer_id = cursor.lastrowid

        except mysql.connector.Error as err:
            p = str(err)
            self.show_error_popup_1("Failed to authenticate \n{}".format(
                p[13:].replace('Duplicate entry', 'Already Exist ').replace('employee.', 'in ').replace('for key',
                                                                                                        '  ')))

            return

        finally:
            # Close cursor and connection
            cursor.close()
            connection.close()

        return customer_id

    def add_dashes_to_number_with_existing_dashes(self, number):
        # Convert number to string
        number_str = str(number)

        # Use regular expression to add dashes after every three digits for the first two groups
        # and after every four digits for the last group
        formatted_number = re.sub(r'(\d{3})(\d{3})(\d{4})', r'\1-\2-\3', number_str)

        return formatted_number

    def display_button_info(self):

        if not all(
                [self.first_name_input.text, self.last_name_input.text, self.phone_input.text, self.email_input.text]):
            self.show_error_popup_1('Error:\nAl Fields are required')
            return

            # Check if phone is numeric and has length 10
        if not (self.phone_input.text.isdigit() and len(self.phone_input.text) == 10):
            self.show_error_popup_1('Error:\nnumber must be digits with 10 numbers.')
            return

            # Check if email ends with '@gmail'
        if not self.email_input.text.endswith('@gmail.com'):
            self.show_error_popup_1('Error:\nemail should end with @gmail.com')
            return
        if self.payment_button.text == 'Payment Method':
            self.show_error_popup_1('Error:\nselect payment method.')
            return
        if self.button_info:
            first = self.first_name_input.text
            last = self.last_name_input.text
            email = self.email_input.text
            phone = self.phone_input.text
            total = self.ids.total.text
            payment = self.payment_button.text

            payment = payment.replace('Cash', '1').replace('QR code', '2')
            customer_id = self.insert_data(first, last, phone, email)
            total = total.replace('Total Amount with Tax: $', '')
            present_date1 = datetime.datetime.now().date()
            if customer_id != None:
                order_id = self.insert_order(customer_id=customer_id, id=id, payment=payment, total=total)
                try:
                    # Connect to the database
                    with mysql.connector.connect(
                            host="localhost",
                            user="root",
                            password="Vinay@143",
                            database="grocerystore"
                    ) as connection:
                        # Create a cursor
                        with connection.cursor(buffered=True) as cursor:
                            for button_name, info in self.button_info.items():
                                # Execute the query
                                query = 'SELECT product_id, product_available_quantity FROM products WHERE product_name = %s'
                                cleaned_text = re.sub(r'\d+\s*(kg|gm|ml|liter)', '', button_name)
                                cursor.execute(query, (cleaned_text,))
                                result = cursor.fetchone()
                                if result:  # Check if result is not None
                                    p_id, available_quantity = result
                                    o=order_id
                                    p = info['price']
                                    q = info['click_count']
                                    query1 = "INSERT INTO order_items_summary (order_id, product_id, quantity_of_product, amount_of_product) VALUE (%s, %s, %s, %s)"
                                    cursor.execute(query1,(o, p_id, q, p))
                                    connection.commit()
                                    q1 = available_quantity - q
                                    u_q = 'UPDATE PRODUCTS SET product_available_quantity = %s WHERE product_id = %s'
                                    cursor.execute(u_q, (q1, p_id))
                                    connection.commit()
                                else:
                                    # Handle case where no rows are returned
                                    pass  # or raise an exception, log an error, etc
                            # Commit the transaction after all operations
                    cursor.close()
                    connection.close()
                    self.show_success_popup_1("BILL sent to {} successfully".format(email))
                    self.popup.dismiss()
                    # Define email sender and receiver
                    email_sender = 'reddyvinay9777@gmail.com'
                    email_password = 'iwskizhnliiyblpr'
                    email_receiver = email

                    # Set the subject and body of the email
                    subject = 'Check out your bill here.'
                    # Calculate the width of the box dynamically based on the longest button_name
                    max_button_name_length = max(len(button_name) for button_name in self.button_info.keys())
                    box_width = max(32, max_button_name_length + 12)  # Minimum width of 32 characters

                    # Create the box format for the body
                    body = "╔" + "═" * (box_width - 2) + "╗\n"
                    body += "║{:^{width}} \n".format("BILL INFORMATION", width=box_width - 2)
                    body += "╠" + "═" * (box_width - 2) + "╣\n"
                    body += "║ Order ID: {}       Date:{} \n".format(order_id, present_date1)
                    body += "╠" + "═" * (box_width - 2) + "╣\n"
                    for button_name, info in self.button_info.items():
                        button_info_str = "  {} x {}".format(info['click_count'], info['price'])
                        padding = box_width - len(button_name) - len(button_info_str) - 10
                        body += "║ {}{}{} \n".format(button_name, " " * padding, button_info_str)
                    body += "╠" + "═" * (box_width - 2) + "╣\n"
                    body += "║  {} \n".format(self.ids.total.text)
                    body += "╚" + "═" * (box_width - 2) + "╝"

                    em = EmailMessage()
                    em['From'] = email_sender
                    em['To'] = email_receiver
                    em['Subject'] = subject
                    em.set_content(body.upper())

                   # Add SSL (layer of security)
                    context = ssl.create_default_context()
                   # Log in and send the email
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.sendmail(email_sender, email_receiver, em.as_string())
                    # Remove all selected items from the layout and dictionary
                    self.ids.Selected_items_layout.clear_widgets()
                    # Reset the total amount label
                    self.ids.total.text = 'Total Amount with Tax: $0.00'
                    # Clear button_info dictionary
                    self.button_info.clear()
                except mysql.connector.Error as err:
                    p = str(err)
                    self.show_error_popup_1("Failed to authenticate \n{}".format(
                        p[13:].replace('Duplicate entry', 'Already Exist ').replace('employee.', 'in ').replace(
                            'for key',
                            '  ')))

                    return








        else:
            self.show_error_popup_1('order not yet taken.')
            return

    def add_selected_item(self, instance):
        self.ids.dis1.disabled = False
        self.ids.dis2.disabled = False
        self.ids.dis3.disabled = False
        button_name, button_price = instance.text.split('\nPrice: ')

        # Update the selected items layout
        selected_item_label = Label(text=f"{button_name} - ${button_price}", padding=(2, 5, 2, 5))

        # Create remove button for each label
        remove_button = Button(text='Remove', size_hint=(None, None), size=(100, 40), background_normal='',
                               background_color=(0.004, 0.055, 0.102, 1.0),
                               on_press=lambda btn: self.remove_selected_item(btn, selected_item_label))

        # Add the label and remove button to the selected items layout
        self.ids.Selected_items_layout.add_widget(selected_item_label)
        self.ids.Selected_items_layout.add_widget(remove_button)

        # Update the total amount
        current_total = float(self.ids.total.text.split('$')[1])
        tax = float(button_price) * 0.06
        new_total = current_total + float(button_price) + tax
        self.ids.total.text = f'Total Amount with Tax: ${new_total:.2f}'

        # Update button_info dictionary
        if button_name in self.button_info:
            self.button_info[button_name]["click_count"] += 1
        else:
            self.button_info[button_name] = {"price": float(button_price), "click_count": 1}

    def remove_selected_item(self, instance, selected_item_label):
        # Find the index of the remove button in the selected items layout
        remove_button_index = self.ids.Selected_items_layout.children.index(instance)

        # Calculate the corresponding label index
        label_index = remove_button_index // 2

        # Check if the label index is within the valid range
        if 0 <= label_index < len(self.ids.Selected_items_layout.children):
            # Remove both the label and remove button from the layout
            self.ids.Selected_items_layout.remove_widget(selected_item_label)
            self.ids.Selected_items_layout.remove_widget(instance)

            # Extract the item name and price from the label text
            label_text_parts = selected_item_label.text.split(' - $')
            if len(label_text_parts) > 1:
                item_name = label_text_parts[0]
                item_price = float(label_text_parts[1])

                # Update the total amount
                current_total = float(self.ids.total.text.split('$')[1])
                tax = item_price * 0.06
                new_total = current_total - item_price - tax
                self.ids.total.text = f'Total Amount with Tax: ${new_total:.2f}'

                # Update button_info dictionary
                if item_name in self.button_info:
                    self.button_info[item_name]["click_count"] -= 1
                    if self.button_info[item_name]["click_count"] == 0:
                        del self.button_info[item_name]
            else:
                pass
        else:
            pass

    def remove_all_items(self, instance):
        # Remove all selected items from the layout and dictionary
        self.ids.Selected_items_layout.clear_widgets()
        self.ids.dis1.disabled = True
        self.ids.dis2.disabled = True
        self.ids.dis3.disabled = True

        # Reset the total amount label
        self.ids.total.text = 'Total Amount with Tax: $0.00'

        # Clear button_info dictionary
        self.button_info.clear()

    def apply_discount(self, discount_percentage):
        # Calculate the discounted total amount
        current_total = float(self.ids.total.text.split('$')[1])
        discounted_total = current_total * (1 - discount_percentage)
        self.ids.dis1.disabled = True
        self.ids.dis2.disabled = True
        self.ids.dis3.disabled = True

        # Update the total amount label with the discounted total
        self.ids.total.text = f'Total Amount with Tax: ${discounted_total:.2f}'

    def back(self, instance):
        self.ids.Selected_items_layout.clear_widgets()
        self.ids.total.text = 'Total Amount with Tax: $0.00'
        # Clear button_info dictionary
        self.button_info.clear()

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
