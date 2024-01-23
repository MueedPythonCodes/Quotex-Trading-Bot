import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

ID = 32878617           # Taking the User Account ID in Static so that it varies from account to account
first_trade = True      # Boolean variable for executing the First Trade


# Reading Email and Password from the File for Security of our User Sensitive Information
with open("account_details.txt", "r") as file:
    data = file.read()
    data_list = data.split(",")
    email = data_list[0]
    password = data_list[1]

# Taking input from the user about how much profit the user wants
desired_profit = float(input("Enter the profit you want: $"))

# Website link = https://qxbroker.com/en
driver = uc.Chrome()
driver.get("https://qxbroker.com/en")
driver.maximize_window()               # This will maximize our window so that we will clearly see the location of web elememts
time.sleep(3)




# ///////////////////////////////////////// All Functions ////////////////////////////////////////////////////

# Up Button Function
def press_up():
    """ This Function will Press the Up Button """
    btn_Up = driver.find_element(By.XPATH, '//div[@class="section-deal__success  percent"]')
    btn_Up.click()


# Down Button Function
def press_down():
    """ This Function will Press the Down Button """
    btn_Down = driver.find_element(By.XPATH, "//button[@class='button button--danger button--spaced put-btn section-deal__button ']")
    btn_Down.click()



# Initial Trading Amount Function
def initial_trade_value(initial_amount):
    """ This Function will set the initial value for the First trade 
        when we are Randomly Pressing a Button"""

    # Locate the investment section (adjust the XPath accordingly based on the website's structure)
    investment_section =driver.find_element(By.XPATH,'//*[@id="root"]/div/div[1]/main/div[2]/div[1]/div/div[5]/div[2]/div/div/input')
    # Click on the investment section
    investment_section.click()
    # Select all information for deleting
    investment_section.send_keys(Keys.CONTROL + 'a')
    # Deleting the amount by pressing backspace
    investment_section.send_keys(Keys.BACK_SPACE)
    # Set the initial amount
    investment_section.send_keys(initial_amount)



# Changing Amount Function
def click_investment_section(new_amount):
    """ This Function will set the value for the next trades after the first trade
        is done by a Random Button Press"""
    
    # Locate the investment section (adjust the XPath accordingly based on the website's structure)
    investment_section =driver.find_element(By.XPATH,'//*[@id="root"]/div/div[1]/main/div[2]/div[1]/div/div[5]/div[2]/div/div/input')
    # Click on the investment section
    investment_section.click()
    # Select all information for deleting
    investment_section.send_keys(Keys.CONTROL + 'a')
    # Deleting the amount by pressing backspace
    investment_section.send_keys(Keys.BACK_SPACE)
    # Set the new amount
    investment_section.send_keys(new_amount)



# Getting Time
def current_time():
    """ Returns Every Second of a Minute"""
    timer = driver.find_element(By.XPATH, '//div[@class="server-time online"]')
    sp = timer.text.split()
    real_time = sp[0]
    # Extract the seconds part (last 2 characters in the time string)
    seconds_part = real_time[-2:]
    # time.sleep(1)
    return seconds_part



# //////////////////////////////////////////////////////////////////////////////////////////




# Starting of the Code



# Clicking on Login Button
element = driver.find_element(By.XPATH, "//*[@id='top']/div/div[1]/a[2]")
element.click()



# Giving Email and Password then  Clicking on the Signin Button
time.sleep(2)
email_entry = driver.find_element(By.XPATH, "//*[@id='tab-1']/form/div[1]/input").send_keys(f"{email}")
password_entry = driver.find_element(By.XPATH, "//*[@id='tab-1']/form/div[2]/input").send_keys(f"{password}")
signin_button = driver.find_element(By.XPATH, "//*[@id='tab-1']/form/button/div").click()



# Providing time to handle any verification code sent through email
time.sleep(5)
input()            # Here we have given an input to write the code if it is sent through email



# Demo Account Selection


# Clicking on the Header Menu to open the Account options
u_menu = driver.find_element(By.XPATH, "//div[@class='usermenu__info-wrapper']")
u_menu.click()

# User ID Checking
time.sleep(3)
span_user_id = driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/header/div[8]/div[2]/div[2]/ul[1]/li[1]/div[2]/div/span")
# ------- Picking The text of span_tag containing User ID in a String "ID: 32878617"
user_id_string = span_user_id.text

# ------- Converting the String into a list by splitting it through the space
#         so that we have a list = ["ID:", "32878617"].Now we have the ID Number separate
#         so that we can match it Easily

user_id_list = user_id_string.split()
real_user_id = int(user_id_list[1])               # Converting String ID into integer


# Selecting Demo Account By Matching the User-ID With the Given ID
time.sleep(3)

try:
    if real_user_id == ID:
        dm_ac_menu = driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/header/div[8]/div[2]/div[2]/ul[1]/li[3]/a")
        dm_ac_menu.click()


        time.sleep(3)


        # Initialize current profit
        current_profit = 0


        # Initialize the initial trading amount according to the user desire
        initial_trading_amount = int(input("Set your initial trading amount here: $"))
        current_trading_amount = initial_trading_amount  # Track the current trading amount
        initial_trade_value(initial_trading_amount)

        # Initialize previous demo account money
        demo_account_money = driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/header/div[8]/div[2]/div/div[3]/div[2]")
        dollars = demo_account_money.text
        previous_demo_account_money = float(dollars[1:].replace(',', ''))


        buttons = [press_up, press_down]
        current_btn = random.choice(buttons)


        # Starting the loop for doing the tradings until the User gets his Desired Profit

        while True:
            string_seconds = current_time()
            d = int(string_seconds)

            # Condition to place a trade at the start of each minute (when seconds are 0)
            if d == 0:
                # time.sleep(2)
                # Choose a random button to press in the first trade
                if first_trade:
                    current_btn = random.choice(buttons)
                    current_btn()
                    first_trade = False
                    time.sleep(2)
                    # continue
                else:
                    # time.sleep(1)
                    print(previous_demo_account_money)
                    # Calculate profit after the trade
                    demo_account_money = driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/header/div[8]/div[2]/div/div[3]/div[2]")
                    dollars = demo_account_money.text
                    current_demo_account_money = float(dollars[1:].replace(',', ''))
                    print(current_demo_account_money)
                    profit = current_demo_account_money - previous_demo_account_money
                    r_profit = profit         # Introducing r_profit variable for storing the changes made in every 
                                              # individual trade by making it empty at the end of every iteration 
                    
                    
                    # Update current profit for the next iteration
                    current_profit += int(profit)

                    print(f"Profit after trade: ${profit}")
                    print(f"Current Profit: ${current_profit}")

                    # Update previous demo account money for the next iteration
                    previous_demo_account_money = current_demo_account_money

                    # time.sleep(1)

                    # Check if the desired profit is reached
                    if current_profit >= desired_profit:
                        print(f"Desired profit of ${desired_profit} reached. Stopping the program.")
                        driver.quit()
                        break
                    
                    
                    # Reset the amount to the initial value after a profit
                    if r_profit >= 0:
                        time.sleep(0.5)
                        current_trading_amount = initial_trading_amount
                        # Click the button and update the investment amount
                        click_investment_section(current_trading_amount)
                        current_btn()

                    else:
                        time.sleep(1)
                        # Double the amount in the next iteration if there is a loss
                        current_trading_amount = str(int(current_trading_amount) * 2)
                        # Switch the button in the next iteration
                        current_btn = press_down if current_btn == press_up else press_up

                        # Click the button and update the investment amount
                        click_investment_section(current_trading_amount)
                        current_btn()

                    r_profit=0       # Here we are making r_profit zero or empty
                    
except:
    print("Something went wrong.")