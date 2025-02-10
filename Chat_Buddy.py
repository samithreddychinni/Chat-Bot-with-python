import os   #Imports the os module to interact with the operating system
import psutil  # Imports the psutil library for system monitoring
import requests  #Enables making HTTP requests to external APIs
import webbrowser   #Allows the opening of web pages in the default browser.
from fuzzywuzzy import process  #Provides string-matching functions
from prettytable import PrettyTable #Allows for creating formatted tables in the console.
from datetime import datetime #Used for date and time functions.
import pyautogui  #Provides screen automation, allowing control of the mouse and keyboard.
import time  #Allows time-related functions, such as delays.
import csv  #For reading/writing to CSV files.
from datetime import date #Used for date functions


# Contains ANSI escape codes to format console text with colors.
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'    #API KEY FROM "OPENWEATHER" TO GET REAL TIME WEATHER REPORT!!
CITY_NAME = 'Ettimadai'                         #CITY NAME FOR WHICH THE WEATHER REPORT IS GENERATING!!

contacts = {                                                          
            
            "contact-name" : "123-456-7890",       #CONTACTS TO SEND MESSAGES THROUGH WHATSAPP!!

}

# Lists holidays by name and date.
holidays = [
    ("New Year's Day", date(2024, 1, 1)),
    ("Republic Day", date(2024, 1, 26)),
    ("Maha Shivaratri", date(2024, 3, 10)),
    ("Good Friday", date(2024, 3, 29)),
    ("Labour Day", date(2024, 5, 1)),
    ("Independence Day", date(2024, 8, 15)),
    ("Gandhi Jayanti", date(2024, 10, 2)),
    ("Dussehra", date(2024, 10, 10)),
    ("Diwali", date(2024, 11, 1)),
    ("Christmas Day", date(2024, 12, 25)),
    ("Eid ul-Fitr", date(2024, 4, 21)),
    ("Eid ul-Adha", date(2024, 6, 17)),
    ("Raksha Bandhan", date(2024, 8, 19)),
    ("Janmashtami", date(2024, 8, 28)),
    ("Onam", date(2024, 9, 6)),
    ("Karva Chauth", date(2024, 10, 30)),
    ("Baisakhi", date(2024, 4, 13)),
    ("Amma's Birthday", date(2024, 9, 27))
]
DEFAULT_PATH = r"C:\Users\User\OneDrive\Desktop"       #SYSTEM PATH WHERE SCREENSHOTS TAKEN ARE GOING TO BE STORED!!
TASKS_FILE=r"C:\Users\User\OneDrive\Desktop"           #SYSTEM PATH WHERE TO-DO TASKS ARE GOING TO BE STORED!!

#Prints a separator line in the console for readability.
def print_separator():
    print("\n" + "=" * 50 + "\n")

#Based on temperature and UV index, returns suggestions for user actions.
def suggest_weather_action(temp, uv_index):
    suggestion = ""
    if temp > 30:
        suggestion = "It's quite hot today! Stay hydrated and try to stay indoors or in the shade."
    elif temp < 15:
        suggestion = "It's pretty cold outside. Make sure to wear warm clothes."
    else:
        suggestion = "The temperature is moderate today. Enjoy your day outside!"
    
    if uv_index > 6:
        suggestion += " The UV index is high, so remember to wear sunscreen if you go outside."
    
    return suggestion

#Fetches weather data using the OpenWeather API, formats it in a table, and displays it.
def get_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME},IN&appid={API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        main = data['main']
        weather = data['weather'][0]
        uv_url = f"http://api.openweathermap.org/data/2.5/uvi?lat={data['coord']['lat']}&lon={data['coord']['lon']}&appid={API_KEY}"
        uv_response = requests.get(uv_url)
        uv_response.raise_for_status()
        uv_index = uv_response.json()['value']

        temp = main['temp']
        humidity = main['humidity']
        description = weather['description']
        wind_speed = data['wind']['speed']
        pressure = main['pressure']

        weather_table = PrettyTable()
        weather_table.field_names = ["City", "Temperature (°C)", "Humidity (%)", "Description", "Wind Speed (m/s)", "Pressure (hPa)", "UV Index"]
        weather_table.add_row([CITY_NAME, temp, humidity, description.capitalize(), wind_speed, pressure, uv_index])
        
        print_separator()
        print(Colors.HEADER + "🌤️ Weather Information 🌤️" + Colors.ENDC)
        print(weather_table)
        print(Colors.HEADER + "Suggestions" + Colors.ENDC)
        print(suggest_weather_action(temp, uv_index))
        print_separator()
        return "Weather information displayed above."

    except requests.exceptions.RequestException as e:
        return Colors.FAIL + f"Error: {str(e)}" + Colors.ENDC

#Opens Google homepage
def open_google():
    webbrowser.open(f"https://www.google.com")
    return Colors.OKGREEN + f"Opening Google...." + Colors.ENDC

#performs a search based on the query.
def open_google_and_search(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")
    return Colors.OKGREEN + f"🔍 Searching Google for: {query}" + Colors.ENDC

#Opens YouTube
def open_youtube():
    webbrowser.open(f"https://www.youtube.com")
    return Colors.OKGREEN + f"Opening youtube...." + Colors.ENDC

#searches for a query on YouTube.
def open_youtube_and_search(query):
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    return Colors.OKGREEN + f" 📹 Searching YouTube for: {query}" + Colors.ENDC

#Returns the current time.
def get_time():
    return datetime.now().strftime("%H:%M:%S")

#Sends a message to a contact on WhatsApp using pyautogui to automate typing.
def send_whatsapp_message():
    print("Bot:- Who would you like to send a message to? (Please enter the recipient's name):")
    recipient_name = input("You:- ").strip()
    phone_number = contacts.get(recipient_name)
    
    if not phone_number:
        print("Bot:- I couldn't find that contact. Please check the name and try again.")
        return

    print("Bot:- What would you like to send?")
    message = input("You:- ").strip()
    
    # Open WhatsApp Web for the contact
    webbrowser.open(f"https://wa.me/{phone_number}")
    time.sleep(8)  # Increased wait time to ensure WhatsApp is loaded

    # Click on the message input box (adjust coordinates based on your screen resolution)
    pyautogui.click(x=1092, y=1049)  # Change coordinates to where the message box is
    time.sleep(1)  # Short pause to ensure the message box is focused

    # Type the message and send it
    pyautogui.typewrite(message)
    pyautogui.press('enter')  
    print(f"Bot:- Message to {recipient_name} has been sent.")

#Opens the Windows Camera app and takes a photo using pyautogui.
def open_camera_and_take_photo():
    try:
        os.system("start microsoft.windows.camera:")  
        time.sleep(5)  
        pyautogui.press('space')
        time.sleep(2)  
        pyautogui.hotkey('alt', 'f4')  
        return Colors.OKGREEN + "📸 Photo taken successfully!" + Colors.ENDC
    except Exception as e:
        return Colors.FAIL + f"❌ Failed to open camera: {str(e)}" + Colors.ENDC

#Takes a screenshot and saves it to DEFAULT_PATH.
def take_screenshot():
    try:
        screenshot = pyautogui.screenshot()
        screenshot_path = os.path.join(DEFAULT_PATH, "screenshot.png")
        screenshot.save(screenshot_path)
        return Colors.OKGREEN + f"🖼️ Screenshot taken and saved to {screenshot_path}" + Colors.ENDC
    except Exception as e:
        return Colors.FAIL + f"❌ Failed to take screenshot: {str(e)}" + Colors.ENDC

#Opens Notepad using os.system
def open_notepad():
    try:
        os.system("notepad")  
        return Colors.OKGREEN + "Notepad opened successfully!" + Colors.ENDC
    except Exception as e:
        return Colors.FAIL + f"Failed to open Notepad: {str(e)}" + Colors.ENDC

#Opens the Microsoft Store and searches for an app.
def open_store_and_search(app_name):
    try:
        
        webbrowser.open(f"ms-windows-store://search/?query={app_name}")
        return Colors.OKGREEN + f"Opening Microsoft Store to search for '{app_name}'..." + Colors.ENDC
    except Exception as e:
        return Colors.FAIL + f"Failed to open Microsoft Store: {str(e)}" + Colors.ENDC

#Opens the file explorer.
def open_file_explorer():
    try:
        os.startfile('explorer')  
        return Colors.OKGREEN + "File Explorer opened successfully!" + Colors.ENDC
    except Exception as e:
        return Colors.FAIL + f"Failed to open File Explorer: {str(e)}" + Colors.ENDC

#Opens Google Maps at my location.
def show_location(latitude=0.0, longitude=0.0):
    try:
        
        url = f"https://www.google.com/maps/@{latitude},{longitude},15z"  
        webbrowser.open(url)
        return Colors.OKGREEN + "Opening Google Maps to show your location..." + Colors.ENDC
    except Exception as e:
        return Colors.FAIL + f"Failed to open Google Maps: {str(e)}" + Colors.ENDC

#Locates a place on Google Maps.
def locate_place(place_name):
    try:
        
        url = f"https://www.google.com/maps/search/?api=1&query={place_name.replace(' ', '+')}"
        webbrowser.open(url)
        return Colors.OKGREEN + f"Opening Google Maps to locate {place_name}..." + Colors.ENDC
    except Exception as e:
        return Colors.FAIL + f"Failed to open Google Maps: {str(e)}" + Colors.ENDC


#Shows the current CPU usage.
def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return Colors.OKGREEN + f"🖥️ CPU Usage: {cpu_usage}% " + Colors.ENDC

#Shows the current memory usage.
def get_memory_usage():
    memory = psutil.virtual_memory()
    return Colors.OKGREEN + f"💾 Memory Usage: {memory.percent}% " + Colors.ENDC

#Shows the current disk usage.
def get_disk_usage():
    disk = psutil.disk_usage('/')
    return Colors.OKGREEN + f"💻 Disk Usage: {disk.percent}% " + Colors.ENDC

#Load tasks from TASK_FILE.
class to_do:
    def _init_(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        try:
            with open('tasks.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.tasks.append({'task': row['task'], 'status': row['status']})
        except FileNotFoundError:
            pass  # If file doesn't exist, skip loading

    def save_tasks(self):
        with open('tasks.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['task', 'status'])
            writer.writeheader()
            writer.writerows(self.tasks)

    def add_task(self, task):
        self.tasks.append({'task': task, 'status': 'Pending'})
        self.save_tasks()

    def view_tasks(self):
        if not self.tasks:
            return Colors.WARNING + "Your To-Do List is empty." + Colors.ENDC
        task_table = PrettyTable()
        task_table.field_names = ["Task No", "Task", "Status"]
        for idx, task in enumerate(self.tasks, 1):
            task_table.add_row([idx, task['task'], task['status']])
        return str(task_table)

    def mark_complete(self, task_number):
        if 0 < task_number <= len(self.tasks):
            self.tasks[task_number - 1]['status'] = 'Complete'
            self.save_tasks()
            return Colors.OKGREEN + f"Task {task_number} marked as Complete." + Colors.ENDC
        else:
            return Colors.FAIL + "Invalid task number." + Colors.ENDC

todo_instance=to_do()

#Opens Gmail inbox.
def open_gmail_inbox():
    # URL for Gmail inbox
    gmail_url = "https://mail.google.com/mail/u/0/#inbox"
    
    # Open the URL in the default web browser
    webbrowser.open(gmail_url)

#Manages a basic to-do list with methods to add tasks, view tasks, and mark tasks as complete.    
class to_do:
    def _init_(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        try:
            with open('tasks.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.tasks.append({'task': row['task'], 'status': row['status']})
        except FileNotFoundError:
            pass  # If file doesn't exist, skip loading

    def save_tasks(self):
        with open('tasks.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['task', 'status'])
            writer.writeheader()
            writer.writerows(self.tasks)

    def add_task(self, task):
        self.tasks.append({'task': task, 'status': 'Pending'})
        self.save_tasks()

    def view_tasks(self):
        if not self.tasks:
            return Colors.WARNING + "Your To-Do List is empty." + Colors.ENDC
        task_table = PrettyTable()
        task_table.field_names = ["Task No", "Task", "Status"]
        for idx, task in enumerate(self.tasks, 1):
            task_table.add_row([idx, task['task'], task['status']])
        return str(task_table)

    def mark_complete(self, task_number):
        if 0 < task_number <= len(self.tasks):
            self.tasks[task_number - 1]['status'] = 'Complete'
            self.save_tasks()
            return Colors.OKGREEN + f"Task {task_number} marked as Complete." + Colors.ENDC
        else:
            return Colors.FAIL + "Invalid task number." + Colors.ENDC

#Initiate WhatsApp videocall.
def whatsapp_videocall():
    name = input("Enter the name of the contact to start a video call: ")
    
    # Check if the name is in the contacts dictionary
    if name in contacts:
        phone_number = contacts[name]
        
        # WhatsApp Web URL for a specific phone number
        url = f"https://wa.me/{phone_number}"
        
        # Open the URL in the default web browser
        webbrowser.open(url)
        time.sleep(8)
        pyautogui.click(1775, 86)
    else:
        print("Contact not found in the directory.")

# Initiate WhatsApp videocalls.
def whatsapp_voicecall():
    name = input("Enter the name of the contact to start a call: ")
    
    # Check if the name is in the contacts dictionary
    if name in contacts:
        phone_number = contacts[name]
        
        # WhatsApp Web URL for a specific phone number
        url = f"https://wa.me/{phone_number}"
        
        # Open the URL in the default web browser
        webbrowser.open(url)
        time.sleep(8)
        pyautogui.click(1823, 81)
    else:
        print("Contact not found in the directory.")

# Finds and returns the next holiday from holidays
def next_holiday():
    today = date.today()
    
    # Find the next holiday
    future_holidays = [holiday for holiday in holidays if holiday[1] > today]
    
    # If no holidays left this year, return a message
    if not future_holidays:
        return "No holidays left this year!"
    
    # Find the next holiday (sorted by date)
    next_holiday = min(future_holidays, key=lambda x: x[1])
    holiday_name, holiday_date = next_holiday
    return f"The next holiday is {holiday_name} on {holiday_date.strftime('%B %d, %Y')}."


#Asks the user for a rating, with feedback depending on the rating.
def Chat_Buddy_rating():
    rating_loop = 1
    while True:
        rating = int(input("Please rate me out of 15: "))
        
        if rating >= 14:
            print("Thank you! 😊")
            break
        else:
            if rating_loop == 2:
                print("😭 Please give a better rating next time! If not, don't use me again!")
                exit()
            else:
                print("I think you can give a better rating...!! 😠")
                rating_loop += 1

#Processes user queries by matching keywords and executing the appropriate function.            
def handle_command(user_query):
    user_query = user_query.lower()
    if "weather" in user_query:
        return get_weather()
    elif "open google and search" in user_query:
        query = user_query.replace("open google and search", "").strip()
        return open_google_and_search(query)
    elif "launch google" in user_query:
        return open_google()
    elif "launch youtube" in user_query:
        return open_youtube()
    elif "open youtube and search" in user_query:
        query = user_query.replace("open youtube and search", "").strip()
        return open_youtube_and_search(query)
    elif "time" in user_query:
        return Colors.OKGREEN + f"The current time is: {get_time()}" + Colors.ENDC
    elif "whatsapp" in user_query:
        send_whatsapp_message()
    elif "cpu usage" in user_query:
        return get_cpu_usage()
    elif "memory usage" in user_query:
        return get_memory_usage()
    elif "disk usage" in user_query:
        return get_disk_usage()
    elif "take photo" in user_query:
        return open_camera_and_take_photo()
    elif "take screenshot" in user_query:
        return take_screenshot()
    elif "open store and search" in user_query:
        app_name = user_query.replace("open store and search", "").strip()
        return open_store_and_search(app_name)
    elif "open file explorer" in user_query:
        return open_file_explorer()
    elif "show my location" in user_query:
        return show_location(0.00000000000,0.000000000) #replace with logitude and latitude 
    elif "locate" in user_query:
        place = user_query.replace("locate", "").strip()
        return locate_place(place)
    elif "add task" in user_query:
        task = user_query.replace("add task", "").strip()
        todo_instance.add_task(task)  # Call the method without returning it
        return Colors.OKGREEN + f"Task '{task}' added to your To-Do list." + Colors.ENDC
    elif "view tasks" in user_query or "view task" in user_query:
        return todo_instance.view_tasks()  # Remove the 'task' argument, as view_tasks() doesn't take any
    elif "completed task " in user_query:
        try:
            task_number = int(user_query.split()[-1])
            return todo_instance.mark_complete(task_number)
        except ValueError:
            return Colors.FAIL + "Please specify the task number correctly." + Colors.ENDC
    elif "open my inbox" in user_query:
        return open_gmail_inbox()
    elif "start a video call" in user_query:
        return whatsapp_videocall()
    elif "make a call" in user_query:
        return whatsapp_voicecall()
    elif "when is the next holiday" in user_query:
        return next_holiday()
    else:
        return Colors.FAIL + "Sorry, I didn't understand that." + Colors.ENDC

# Main loop to get user input and run commands
def main():
    loop = 0
    print(Colors.HEADER + "🌐 Welcome to the Chat Buddy 🌐" + Colors.ENDC)
    while True:
        if loop < 1:
            print("Chat Buddy 🤖: How can I assist you today?")
            user_query = input("You: ")
        else:
            print("Chat Buddy 🤖: What Next.....?")
            user_query = input("You: ")

        # Check if the user wants to exit
        if user_query.lower() in ["exit", "quit", "kill me"]:
            Chat_Buddy_rating()
            break

        response = handle_command(user_query)
        print(response)
        loop += 1

#Runs the main loop if the script is executed as the main file.
if __name__ == "__main__":
    main()
