from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast
# ----------------------
import platform
from geopy.geocoders import Nominatim
from datetime import datetime
from email.message import EmailMessage
from pymongo import MongoClient
import bcrypt, secrets
import ssl, smtplib
import string
import re, random, sys

# Using Nominatim from geopy to get location based on IP address
def DeviceLocation():
    geolocator = Nominatim(user_agent="device_location_app")
    location = geolocator.geocode('')
    
    if location:
        return {
            'latitude': location.latitude,
            'longitude': location.longitude,
            'address': location.address
        }
    else:
        return None

# Using datetime to get the current time
def CurrentTime():
    current_time = datetime.now()
    return current_time.strftime('%Y-%m-%d %H:%M:%S')

# get_device_info
def DeviceInfo():
    return {
        "System": platform.system(),
        "Node": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor()
    }

# bcrypt
def generate_random_username(length=8):
    return ''.join(secrets.choice(string.ascii_letters) for _ in range(length))

def generate_random_password(length=12):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(password_characters) for _ in range(length))

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verify_password(password, hashed_password):
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    except:
        return password == hashed_password

# pymongo database
client = MongoClient("mongodbDataSheet_Name")
db = client.neuraldb
users = db.users

# db options
def AddUser(Username, Email, Full_Name):
    password = generate_random_username()
    user_data = {'Username': Username, 'Email': Email, 'Full Name': Full_Name, 'Password': password}
    users.insert_one(user_data)

def FindUser(input_value, search_key='Username'):
    query = {search_key: input_value}
    person = users.find_one(query)
    return person

def EditPerson(Username, full_name, edit_info_name, new_info):
    query = {'Username': Username, "Full Name": full_name}
    update_result = users.update_many(query, {'$set': {edit_info_name: new_info}})

def PrintDataBase():
    cursor = users.find()
    for user in cursor:
        print(user)

# show notification
def show_notification(check):
    if (check):
        toast('Sorry, Somthing has gone wrong')
    else:
        toast('Success')

# check email
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

# send email 
def SenderInfo(email_receiver, subject, body):
    email_sender = "Email"
    email_password = "emailPassword"
    email_receiver = email_receiver

    email = EmailMessage()
    email["From"] = email_sender
    email["To"] = email_receiver
    email["Subject"] = subject
    email.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', Number, context = context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, email.as_string())

# windows
class WindowManager(ScreenManager):
    pass

class LogInScreen(Screen):
    def check_input(self):
        self.LoginUsername_input = self.ids.username_input
        self.LoginPassword_input = self.ids.text_field
        self.LoginUsername = self.LoginUsername_input.text
        self.LoginPassword = self.LoginPassword_input.text

        if (len(self.LoginUsername) >= self.LoginUsername_input.max_text_length) or (len(self.LoginPassword) >= self.LoginPassword_input.max_text_length):
            show_notification(True)

        elif (bool(re.search(r"\s", self.LoginUsername))):
            show_notification(True)
        
        elif not self.LoginUsername or not self.LoginPassword:
            show_notification(True)
        
        elif any(char in string.punctuation for char in self.LoginUsername):
            show_notification(True)
        
        user = FindUser(input_value=self.LoginUsername, search_key='Username')
        if user and verify_password(self.LoginPassword, user.get('Password', '')):
            show_notification(False)
            location = DeviceLocation()
            current_time = CurrentTime()
            device_info = DeviceInfo()
            configBody = f"""Dear {user.get('Username', '')},
                        \n\t We are writing to inform you about recent login activity on your account. Details of the Login:
                        \n Date and Time: {location}
                        \n Location: {current_time}
                        \n Device: {device_info[1]}, {device_info[0]}
                        \n
                        \n\t If you recognize this activity, you can disregard this email. However, if you do not recognize this login or suspect unauthorized access to your account, please take the following steps immediately:
                        \n\t 1) Change your password: Visit the app and go to the login page. Click on the "Forgot Password" link to reset your password. Choose a strong, unique password that you have not used elsewhere.
                        \n\t 2) Review Account Activity: Check your account settings for any unfamiliar changes. Ensure that your contact information, especially your email address, is up-to-date.
                        \n\t 3) Enable Two-Factor Authentication (2FA): If you haven't already, consider enabling 2FA for an extra layer of security. This can usually be done in your account settings.
                        \n\t 4) Contact Support: If you continue to have concerns or need assistance, please contact our support team
                        \n\t Remember to be cautious of phishing attempts and only use official channels for communication regarding your account. We take the security of your account seriously and are here to help ensure your information remains safe.
                        \n\t Thank you for your attention to this matter.
                        \n\t Best regards,
                        """
            SenderInfo(email_receiver=user.get('Email', ''), subject="Login Detected", body=configBody)
        else:
            show_notification(True)
        PrintDataBase()
        self.clear()
    
    def clear(self):
        self.LoginUsername_input.text = ""
        self.LoginPassword_input.text = ""

class SignUpScreen(Screen):
    def check_input(self):
        self.SignUpFullName_input = self.ids.fullName_input
        self.SignUpEmail_input = self.ids.email_input
        self.SignUpFullName = self.SignUpFullName_input.text
        self.SignUpEmail = self.SignUpEmail_input.text
        
        if (len(self.SignUpFullName) >= self.SignUpFullName_input.max_text_length) or (len(self.SignUpEmail) >= self.SignUpEmail_input.max_text_length):
            show_notification(True)
        
        elif any(char in string.punctuation for char in self.SignUpFullName):
            show_notification(True)
        
        elif not self.SignUpFullName or not self.SignUpEmail or not is_valid_email(self.SignUpEmail):
            show_notification(True)
        
        elif any(char in string.punctuation for char in self.SignUpFullName):
            show_notification(True)
        
        elif FindUser(input_value=self.SignUpFullName, search_key='Full Name'):
            show_notification(True)
        
        elif FindUser(input_value=self.SignUpEmail, search_key='Email'):
            show_notification(True)
        
        else:
            show_notification(False)
            username = generate_random_username()
            AddUser(username,self.SignUpEmail,self.SignUpFullName)
            user = FindUser(input_value=self.SignUpFullName, search_key='Full Name')
            configBody = f"""
                        Dear {user.get('Full Name', '')},
                        \n\t Welcome to Greenville Unitarian universalist fellowship or (GUUF). We wanted to send you an email to officially welcome you to the GUUF IT department, and it associated application.
                        \n\t What you will have the ability to axis on this app: 
                        \n - Calender
                        \n - script maker
                        \n - Messaging softwere
                        \n - Password manager
                        \n - Manuls
                        \n\t welcome to the GUUF IT department
                        \t Security:
                        \n\t If you recognize this activity, you can disregard this email. However, if you do not recognize this login or suspect unauthorized access to your account, please take the following steps immediately:
                        \n\t 1) Change your password: Visit the app and go to the login page. Click on the "Forgot Password" link to reset your password. Choose a strong, unique password that you have not used elsewhere.
                        \n\t 2) Review Account Activity: Check your account settings for any unfamiliar changes. Ensure that your contact information, especially your email address, is up-to-date.
                        \n\t 3) Enable Two-Factor Authentication (2FA): If you haven't already, consider enabling 2FA for an extra layer of security. This can usually be done in your account settings.
                        \n\t 4) Contact Support: If you continue to have concerns or need assistance, please contact our support team
                        \n\t Remember to be cautious of phishing attempts and only use official channels for communication regarding your account. We take the security of your account seriously and are here to help ensure your information remains safe.
                        \n\t Thank you for your attention to this matter.
                        \n\t Best regards,
                        """
            SenderInfo(email_receiver=user.get('Email', ''), subject="Signup Detected", body=configBody)
        self.clear()

    def clear(self):
        self.SignUpFullName_input.text = ""
        self.SignUpEmail_input.text = ""

class ForgotPasswordScreen(Screen):
    def __init__(self, **kwargs):
        super(ForgotPasswordScreen, self).__init__(**kwargs)
        self.forgotUsername = ""
        self.forgotEmail = ""
        self.code = None

    def enter(self):
        # This method is called just before the screen is displayed
        self.forgotUsername_input = self.ids.username_input
        self.forgotEmail_input = self.ids.email_input
        self.forgotUsername = self.forgotUsername_input.text
        self.forgotEmail = self.forgotEmail_input.text
        self.code = None

    def check_input(self):
        self.enter()
        self.get_forgot_info()
        
        if (len(self.forgotUsername) >= self.forgotUsername_input.max_text_length) or (len(self.forgotEmail) >= self.forgotEmail_input.max_text_length):
            show_notification(True)

        elif (bool(re.search(r"\s", self.forgotUsername))):
            show_notification(True)
        
        elif not self.forgotUsername or not self.forgotEmail:
            show_notification(True)
        
        elif any(char in string.punctuation for char in self.forgotUsername):
            show_notification(True)
        
        user = FindUser(input_value=self.forgotUsername, search_key='Username')
        if user and self.forgotEmail == user.get('Email', ''):
            show_notification(False)
            '''configBody = f"""Dear {user.get('Username', '')},
                        \n\t On the behalf of the Greenville Unitarian universalist fellowship or (GUUF) the application called GUUF IT DepartmentApp would like to inform you that you may have forgotten your password.
                        \n\t If you do not reconise this email, place name, or application name. Please feel free to block or remove this email. 
                        \n\t If you keep on geeting messages and do not reconise any information on this email, please: 
                        \n\t 1) Review Account Activity
                        \n\t 2) Change your password and email
                        \n\t 3) black and report (if needed)
                        \n\t 4) unsubscribe
                        \n\t please use this code to change your password: {self.code},
                        \n\t Remember to be cautious of phishing attempts and only use official channels for communication regarding your account. We take the security of your account seriously and are here to help ensure your information remains safe.
                        \n\t Thank you for your attention to this matter.
                        \n\t Best regards,
                        """
            SenderInfo(email_receiver=user.get('Email', ''), subject="Forgot Password Detected", body=configBody)'''
            app = MDApp.get_running_app()
            app.root.current = 'EnterCodeScreen'
        else:
            show_notification(True)

    def clear(self):
        self.SignUpFullName_input.text = ""
        self.SignUpEmail_input.text = ""
    
    def get_forgot_info(self):
        return [self.forgotUsername, self.forgotEmail, self.code]

class EnterCodeScreen(Screen):
    def check_input(self):
        self.newPasswordText_field = self.ids.text_field
        self.code_input = self.ids.code_input
        self.newPassword = self.newPasswordText_field.text
        self.codeInput = self.code_input.text
        # ----
        self.getInfo = ForgotPasswordScreen()
        self.getInfo.get_forgot_info()
        print(self.getInfo.get_forgot_info())

        if (len(self.newPassword) >= self.newPasswordText_field.max_text_length) or (len(self.codeInput) > self.code_input.max_text_length):
            show_notification(True)
        
        elif not self.newPassword or not self.codeInput:
            show_notification(True)
        
        elif int(self.codeInput) != 1000:
            show_notification(True)
        
        elif FindUser(input_value = self.newPassword, search_key = 'Password'):
            show_notification(True)

        else:
            PrintDataBase()
            show_notification(False)
            location = DeviceLocation()
            current_time = CurrentTime()
            device_info = DeviceInfo()
            configBody = f"""Dear 'admin',
                        \n\t We are writing to inform you about recent login activity on your account. Details of the Login:
                        \n Date and Time: {location}
                        \n Location: {current_time}
                        \n Device: {device_info}
                        \n
                        \n\t If you recognize this activity, you can disregard this email. However, if you do not recognize this login or suspect unauthorized access to your account, please take the following steps immediately:
                        \n\t 1) Change your password: Visit the app and go to the login page. Click on the "Forgot Password" link to reset your password. Choose a strong, unique password that you have not used elsewhere.
                        \n\t 2) Review Account Activity: Check your account settings for any unfamiliar changes. Ensure that your contact information, especially your email address, is up-to-date.
                        \n\t 3) Enable Two-Factor Authentication (2FA): If you haven't already, consider enabling 2FA for an extra layer of security. This can usually be done in your account settings.
                        \n\t 4) Contact Support: If you continue to have concerns or need assistance, please contact our support team
                        \n\t Remember to be cautious of phishing attempts and only use official channels for communication regarding your account. We take the security of your account seriously and are here to help ensure your information remains safe.
                        \n\t Thank you for your attention to this matter.
                        \n\t Best regards,
                        """
            # SenderInfo(email_receiver=user.get('Email', ''), subject="Login Detected", body=configBody)
            # EditPerson(Username=Username, full_name=FindUser(input_value=Username, search_key="Full Name"), edit_info_name="Password", new_info=hash_password(self.newPassword))
            self.clear()
            PrintDataBase()

    def clear(self):
        self.newPasswordText_field.text = ""
        self.code_input.text = ""

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        self.WM = WindowManager()
        self.WM.add_widget(LogInScreen(name='LogInScreen'))
        return Builder.load_file('main.kv')

    def on_start(self):
        self.icon = "assets\channels4_profile-fotor-bg-remover-20240104154756.png"
        self.title = "GUUF IT Department App"
    
    def show_hide_password(self, instance):
        if instance.password:
            instance.password = False
            instance.icon_right = "eye"
        else:
            instance.password = True
            instance.icon_right = "eye-off"

if __name__ == '__main__':
    Window.size = (360, 640)
    MainApp().run()
