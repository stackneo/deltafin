import json

import selenium.common
from bs4 import BeautifulSoup

# Exclusively for automatic login.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login_func(client):
    choice = input('Choose your authentication method (1 = Local, 2 = Reverse Proxy): ')

    # Local Authentication
    if choice == '1':
        client.config.data["auth.ssl"] = False
        server = input('Enter your server IP and Port: ')
        connection_status = client.auth.connect_to_address(server)
        if connection_status['State'] != 0:
            username = input('Enter your username: ')
            password = input('Enter your password: ')
            if client.auth.login('http://' + server, username, password):
                print("Successfully logged in! Your credentials have been saved.")
                credentials = client.auth.credentials.get_credentials()
                server = credentials['Servers'][0]
                server["username"] = 'username'
                json.dump(server, open('.credentials.json', 'w'))

    # Reverse Proxy Authentication
    elif choice == '2':
        client.config.data["auth.ssl"] = True
        server = input('Enter your server URL (without http(s) prefix):  ')
        connection_status = client.auth.connect_to_address(server)
        if connection_status['State'] != 0:
            choice = input(
                "Do you want to pick a user to automatically login to (assuming they have no password) (y/n): ")
            if choice == "y":
                # TODO: Find a better way to scrape existing users (this is slow)
                # Setup BeautifulSoup to scrape the server's login page
                driver = webdriver.Firefox()
                driver.get('https://' + server)
                # Gives 3 attempts to grab the usernames.
                for i in range(3):
                    try:
                        # Wait until the divs are loaded
                        WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "cardText singleCardText cardTextCentered"))
                        )
                        break
                        # If the divs are not loaded, try again
                    except selenium.common.TimeoutException:
                        continue
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                divs = soup.find_all('div', attrs={'class': 'cardText singleCardText cardTextCentered'})
                if divs:
                    print('Publicly available user names:')
                    for div in divs:
                        print(div.text.strip())
                    username = input('Enter your username: ')
                    if client.auth.login('https://' + server, username, ''):
                        print("Successfully logged in! Your credentials have been saved.")
                        credentials = client.auth.credentials.get_credentials()
                        server = credentials['Servers'][0]
                        server["username"] = 'username'
                        json.dump(server, open('.credentials.json', 'w'))
                else:
                    print('No publicly available user names found.')
            else:
                username = input('Enter your username: ')
                password = input('Enter your password: ')
                if client.auth.login('https://' + server, username, password):
                    print("Successfully logged in! Your credentials have been saved.")
                    credentials = client.auth.credentials.get_credentials()
                    server = credentials['Servers'][0]
                    server["username"] = 'username'
                    json.dump(server, open('.credentials.json', 'w'))
                else:
                    print("Invalid credentials! Please try again.")
        else:
            print("Invalid URL! Please try again.")
    else:
        print('Invalid choice. Please try again.')
