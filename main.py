import datetime
from EmployeeScreen import *
from TimePunch import *
from orders import *
from price import *
from delivery import *
from orders_for_suppliers import *
import time
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window


Window.clearcolor = 0.0, 0.0, 0.0, 0.0
Window.size = 900, 600



class MainWindow(Screen):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_time, 1)  # Update time every 1 second

    def update_time(self, dt):
        current_time = time.strftime("%H:%M")
        self.ids.clock.text = f'  {current_time}'

    def show_login_popup(self, text):
        text1 = text
        # Create a pop-up window for entering user ID and password
        content = BoxLayout(orientation='vertical', spacing=10, background_normal=''
                            , background_color=(0.004, 0.055, 0.102, 1.0))

        # Create a layout for the close button
        close_button_layout = BoxLayout(size_hint_y=None, height=5, padding=1, spacing=1, background_normal=''
                                        , background_color=(0.004, 0.055, 0.102, 1.0))

        # Add a "Close" button to the top-right corner
        close_button = Button(text='x', size_hint=(None, None), size=(30, 30), on_press=self.dismiss_popup,
                              background_normal=''
                              , background_color=(0.004, 0.055, 0.102, 1.0))
        close_button_layout.add_widget(Label())  # Add an empty label for spacing
        close_button_layout.add_widget(close_button)

        # Add the close button layout to the main content
        content.add_widget(close_button_layout)

        user_id_input = TextInput(hint_text='User ID', background_normal=''
                                  , background_color=(0.004, 0.055, 0.102, 1.0), foreground_color=(1, 1, 1, 1),
                                  multiline=False)
        password_input = TextInput(hint_text='Password', password=True, background_normal=''
                                   , background_color=(0.004, 0.055, 0.102, 1.0), foreground_color=(1, 1, 1, 1),
                                   multiline=False)
        login_button = Button(text='Login',
                              on_press=lambda btn: self.check_credentials(user_id_input.text, password_input.text,
                                                                          text1),
                              background_normal=''
                              , background_color=(0.004, 0.055, 0.102, 1.0))

        content.add_widget(user_id_input)
        content.add_widget(password_input)
        content.add_widget(login_button)

        self.popup = Popup(title='Login', content=content, size_hint=(None, None), size=(300, 300),
                           background_color=(0, 0, 0, 0))
        self.popup.open()

    def dismiss_popup(self, instance):
        if hasattr(self, 'popup') and self.popup:
            self.popup.dismiss()

    def check_credentials(self, user_id, password, text):

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vinay@143",
            port='3306',
            database='grocerystore'
        )
        cursor = conn.cursor()

        # Fetch specific columns (first_name, last_name, emp_id, phone) from the database
        cursor.execute("SELECT employee_login_status,emp_level FROM employee where emp_id=%s and emp_password=%s",
                       (user_id, password))

        employees_data = cursor.fetchone()

        # Close the database connection
        cursor.close()
        conn.close()
        if employees_data is not None:
            # For simplicity, check if user ID and password are correct
            if text == 'clock-in & clock-out':
                self.dismiss_popup(self)
                TimePunch.show_clock_popup(self, user_id)

            elif employees_data[0].upper() == 'ACTIVE' and text == "Ring Order":
                self.dismiss_popup(self)
                s = self.manager
                SecondWindow(id=user_id)
                s.current = "second"

                s.transition.direction = "left"

            elif employees_data[0].upper() == 'ACTIVE' and int(employees_data[1]) in [5] and text == "Employee Management":
                self.dismiss_popup(self)
                s = self.manager
                s.current = "Labor"
                s.transition.direction = "right"

            elif employees_data[0].upper() == 'ACTIVE' and int(employees_data[1]) in [4, 5] and text == "Order Reports":
                self.dismiss_popup(self)
                s = self.manager
                s.current = "order_list"
                s.transition.direction = "right"
            elif employees_data[0].upper() == 'ACTIVE' and int(employees_data[1]) in [4, 5] and text == "Delivery and supplier":
                self.dismiss_popup(self)
                s = self.manager
                s.current = "Delivery_list"
                s.transition.direction = "right"
            elif employees_data[0].upper() == 'ACTIVE' and int(employees_data[1]) in [4, 5] and text == "Add product and \n pricing update":
                self.dismiss_popup(self)
                s = self.manager
                s.current = "price_update"
                s.transition.direction = "right"
            else:
                # Show an error message in the pop-up
                error_label = Label(text='You dont have Access !')
                self.popup.content.add_widget(error_label)

                # Remove the error label after a short delay (adjust as needed)
                Clock.schedule_once(lambda dt: self.popup.content.remove_widget(error_label), 0.7)


        else:
            # Show an error message in the pop-up
            error_label = Label(text='Incorrect credentials. Please try again.')
            self.popup.content.add_widget(error_label)

            # Remove the error label after a short delay (adjust as needed)
            Clock.schedule_once(lambda dt: self.popup.content.remove_widget(error_label), 0.7)

    def show_main_window(self):
        # Close the pop-up and show the main window
        self.dismiss_popup()
        self.layout.clear_widgets()

        pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()
