from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

class UserManager:
    def __init__(self):
        self.users = {}

    def register(self, username, password, email):
        if username in self.users:
            return False
        self.users[username] = User(username, password, email)
        return True

    def login(self, username, password):
        if username in self.users and self.users[username].password == password:
            return True
        return False

class Child:
    def __init__(self, name, date_of_birth):
        self.name = name
        self.date_of_birth = date_of_birth
        self.vaccination_records = []

    def add_vaccination(self, vaccine_name, date_administered):
        self.vaccination_records.append({
            "vaccine_name": vaccine_name,
            "date_administered": date_administered
        })

    def view_vaccination_records(self):
        if not self.vaccination_records:
            return []
        return self.vaccination_records

class Parent(User):
    def __init__(self, username, password, email):
        super().__init__(username, password, email)
        self.children = []

    def add_child(self, child_name, date_of_birth):
        child = Child(child_name, date_of_birth)
        self.children.append(child)

    def view_children(self):
        return [(child.name, child.date_of_birth) for child in self.children]

class Appointment:
    def __init__(self, child_name, vaccine_name, appointment_date):
        self.child_name = child_name
        self.vaccine_name = vaccine_name
        self.appointment_date = appointment_date

class AppointmentManager:
    def __init__(self):
        self.appointments = []

    def schedule_appointment(self, child_name, vaccine_name, days_from_now):
        appointment_date = datetime.now() + timedelta(days=days_from_now)
        appointment = Appointment(child_name, vaccine_name, appointment_date)
        self.appointments.append(appointment)

    def view_appointments(self):
        return [(appointment.child_name, appointment.vaccine_name, appointment.appointment_date) for appointment in self.appointments]

class NotificationManager:
    def __init__(self, smtp_server, smtp_port, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(self, to_email, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                text = msg.as_string()
                server.sendmail(self.username, to_email, text)
        except Exception as e:
            print(f"Failed to send email: {e}")

    def send_reminders(self, appointments):
        for appointment in appointments:
            days_until_appointment = (appointment.appointment_date - datetime.now()).days
            if days_until_appointment <= 7:
                subject = "Upcoming Vaccination Appointment Reminder"
                body = (f"Dear Parent,\n\n"
                        f"This is a reminder for your child's upcoming vaccination appointment.\n"
                        f"Child: {appointment.child_name}\n"
                        f"Vaccine: {appointment.vaccine_name}\n"
                        f"Date: {appointment.appointment_date.strftime('%Y-%m-%d')}\n\n"
                        f"Please ensure you are prepared for the appointment.\n\n"
                        f"Best regards,\n"
                        f"Vaccination Management System")
                self.send_email("parent1@example.com", subject, body)

class VaccinationSystem:
    def __init__(self):
        self.user_manager = UserManager()
        self.appointment_manager = AppointmentManager()
        self.notification_manager = NotificationManager("smtp.example.com", 587, "your-email@example.com", "your-password")
        self.current_user = None

    def register(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        email = input("Enter email: ")
        success = self.user_manager.register(username, password, email)
        if success:
            print("Registration successful!")

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        if self.user_manager.login(username, password):
            self.current_user = self.user_manager.users[username]
            print("Login successful!")
            self.user_menu()
        else:
            print("Login failed.")

    def user_menu(self):
        while True:
            print("\n--- User Menu ---")
            print("1. Add Child")
            print("2. View Children")
            print("3. Schedule Appointment")
            print("4. View Appointments")
            print("5. Logout")
            choice = input("Enter choice: ")

            if choice == '1':
                self.add_child()
            elif choice == '2':
                self.view_children()
            elif choice == '3':
                self.schedule_appointment()
            elif choice == '4':
                self.view_appointments()
            elif choice == '5':
                self.current_user = None
                print("Logged out.")
                break
            else:
                print("Invalid choice.")

    def add_child(self):
        if isinstance(self.current_user, Parent):
            name = input("Enter child's name: ")
            dob = input("Enter child's date of birth (YYYY-MM-DD): ")
            self.current_user.add_child(name, dob)
            print(f"Child {name} added successfully!")

    def view_children(self):
        if isinstance(self.current_user, Parent):
            children = self.current_user.view_children()
            if not children:
                print("No children found.")
            else:
                print("Children:")
                for name, dob in children:
                    print(f"Name: {name}, Date of Birth: {dob}")

    def schedule_appointment(self):
        if isinstance(self.current_user, Parent):
            child_name = input("Enter child's name: ")
            vaccine_name = input("Enter vaccine name: ")
            days_from_now = int(input("Enter days from now for the appointment: "))
            self.appointment_manager.schedule_appointment(child_name, vaccine_name, days_from_now)
            print(f"Appointment scheduled for {child_name} on {datetime.now() + timedelta(days=days_from_now)} for {vaccine_name} vaccine.")

    def view_appointments(self):
        appointments = self.appointment_manager.view_appointments()
        if not appointments:
            print("No appointments scheduled.")
        else:
            print("Scheduled Appointments:")
            for child_name, vaccine_name, appointment_date in appointments:
                print(f"Child: {child_name}, Vaccine: {vaccine_name}, Date: {appointment_date}")

if __name__ == "__main__":
    system = VaccinationSystem()

    while True:
        print("\n--- Main Menu ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            system.register()
        elif choice == '2':
            system.login()
        elif choice == '3':
            print("Exiting system.")
            break
        else:
            print("Invalid choice.")
