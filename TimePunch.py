from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from datetime import datetime

# Import necessary database modules
import mysql.connector
from kivy.uix.screenmanager import Screen


class TimePunch(Screen):
    def show_clock_popup(self, user):

        # Create an instance of the popup
        popup = ClockPopup(user_id=user)
        # Open the popup
        popup.open()


class ClockPopup(Popup):
    def __init__(self, user_id, **kwargs):
        super().__init__(**kwargs)
        self.title = "Clock In/Out"
        self.size_hint = (None, None)
        self.size = (700, 300)  # Larger size
        self.user = user_id
        self.background_color = (0.004, 0.055, 0.102, 1.0)
        self.auto_dismiss=False
        # Connect to the database
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vinay@143",
            database="grocerystore"
        )

        # Create layouts
        self.layout1 = BoxLayout(orientation="vertical",background_color=(0.004, 0.055, 0.102, 1.0))
        self.layout11 = BoxLayout(orientation="vertical",background_color=(0.004, 0.055, 0.102, 1.0))
        self.layout2 = GridLayout(cols=2, spacing=10, padding=10,background_color=(0.004, 0.055, 0.102, 1.0) )
        self.layout3 = GridLayout(cols=2, spacing=10, padding=10,background_color=(0.004, 0.055, 0.102, 1.0) )

        # First Layout: Close button at right corner
        self.close_button = Button(text="Close",background_color=(0.133, 0.855, 0.431, 1.0), size_hint=(None, None), size=(50, 50))
        self.close_button.bind(on_press=self.dismiss)
        self.layout1.add_widget(Label())  # Empty widget for spacing
        self.layout1.add_widget(self.close_button)
        self.name_label = Label(text="", size_hint=(None, None), size=(300, 50))
        self.layout11.add_widget(self.name_label)
        # Second Layout: Status and duration labels
        self.status_label = Label(text="Status: ", size_hint=(None, None), size=(300, 50))
        self.duration_label = Label(text="Duration: ", size_hint=(None, None), size=(300, 50))
        self.layout2.add_widget(self.status_label)
        self.layout2.add_widget(self.duration_label)

        # Third Layout: Clock in and clock out buttons
        self.clock_in_button = Button(text="Clock In",background_color=(0.133, 0.855, 0.431, 1.0), size_hint=(None, None), size=(150, 50))
        self.clock_out_button = Button(text="Clock Out",background_color=(0.133, 0.855, 0.431, 1.0), size_hint=(None, None), size=(150, 50))
        self.layout3.add_widget(self.clock_in_button)
        self.layout3.add_widget(self.clock_out_button)

        # Bind the clock_in and clock_out methods to the buttons' on_press event
        self.clock_in_button.bind(on_press=lambda instance: self.clock_in(self.user, instance))
        self.clock_out_button.bind(on_press=lambda instance: self.clock_out(self.user, instance))

        # Add layouts to the main layout
        self.layout = BoxLayout(orientation="vertical",background_color=(0.004, 0.055, 0.102, 1.0))
        self.layout.add_widget(self.layout1)
        self.layout.add_widget(self.layout11)
        self.layout.add_widget(self.layout2)
        self.layout.add_widget(self.layout3)

        self.add_widget(self.layout)

        self.clocked_in = False
        self.clock_start_time = None
        self.timer_event = None

        # Fetch initial clock-in status from the database
        self.fetch_clock_status(self.user)

    def fetch_clock_status(self, user):
        # Query to fetch the last clock-in status and time from the database
        query = "SELECT clock_type, emp_date, emp_time FROM timepunch WHERE emp_id = %s ORDER BY emp_date DESC, emp_time DESC LIMIT 1"
        user_id = user

        # Execute the query
        cursor = self.connection.cursor()
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        query1 = "SELECT concat(first_name,' ',last_name) from employee where emp_id=%s"
        user_id = user  # Assuming user ID is 1 for demonstration

        # Execute the query
        cursor = self.connection.cursor()
        cursor.execute(query1, (user_id,))
        result1 = cursor.fetchone()
        self.name_label.text = "Name :"+str(result1[0])

        # Update the status label and start the timer based on the fetched result
        if result:
            self.clocked_in = result[0] == 'clockin'
            if self.clocked_in:
                self.status_label.text = "Status: Clocked In"
                # Extract date and time components from the result
                clock_date = result[1]
                clock_time = result[2]
                # Convert time component to datetime.time
                clock_time = datetime.strptime(str(clock_time), '%H:%M:%S').time()
                # Combine date and time components
                clock_datetime = datetime.combine(clock_date, clock_time)
                self.start_timer(clock_datetime)  # Start the timer with the last clocked-in time
            else:
                self.status_label.text = "Status: Clocked Out"
            # Disable clock-in button if already clocked in, disable clock-out button if already clocked out
        if self.clocked_in:
            self.clock_in_button.disabled = True
            self.clock_out_button.disabled = False
        else:
            self.clock_in_button.disabled = False
            self.clock_out_button.disabled = True
        cursor.close()

    def start_timer(self, start_time):
        # Start the timer with the given start time
        self.clock_start_time = start_time
        self.update_timer()

        if self.timer_event:
            self.timer_event.cancel()

        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, *args):
        # Update the duration label with the elapsed time since the start time
        current_time = datetime.now()
        elapsed_time = current_time - self.clock_start_time
        hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        self.duration_label.text = "Duration: {:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

    def clock_in(self, user, instance):
        # Update clock-in status in the database
        self.update_clock_status('clockin', user)

    def clock_out(self, user, instance):
        # Stop the timer
        if self.timer_event:
            self.timer_event.cancel()
        # Disable clock-out button
        self.clock_out_button.disabled = True
        # Update clock-out status in the database
        self.update_clock_status('clockout', user)

    def update_clock_status(self, clock_in_status, user):
        # Insert a new row into the timepunch table with clock_type, emp_id, emp_date, and emp_time
        query = "INSERT INTO timepunch (clock_type, emp_id, emp_date, emp_time) VALUES (%s, %s, %s, %s)"
        user_id = user  # Assuming user ID is 1 for demonstration
        current_datetime = datetime.now()
        clock_date = current_datetime.date()
        clock_time = current_datetime.time()

        # Execute the insert query
        cursor = self.connection.cursor()
        cursor.execute(query, (clock_in_status, user_id, clock_date, clock_time))
        self.connection.commit()
        cursor.close()

        # Update the status label in the popup
        self.clocked_in = clock_in_status == 'clockin'
        if self.clocked_in:
            query1='update employee set employee_login_status=%s where emp_id=%s'
            cursor=self.connection.cursor()
            cursor.execute(query1,('ACTIVE',user_id))
            self.connection.commit()
            cursor.close()
            self.status_label.text = "Status: Clocked In"
            self.start_timer(current_datetime)  # Start timer if clocked in
        else:
            query2 = 'update employee set employee_login_status=%s where emp_id=%s'
            cursor = self.connection.cursor()
            cursor.execute(query2, ('INACTIVE', user_id))
            self.connection.commit()
            cursor.close()
            self.status_label.text = "Status: Clocked Out"
            current_time = datetime.now()
            elapsed_time = current_time - self.clock_start_time
            hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            self.duration_label.text = "Duration: {:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
        # Reset duration label if clocked out
        self.clock_in_button.disabled = True
        self.clock_out_button.disabled = True
