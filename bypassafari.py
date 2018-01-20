from selenium import webdriver
import sqlite3
from datetime import datetime, timedelta


def banner():
    """Neb: Banner."""
    print("""Version 0.1
      _         _ _ _
  ___( ) __ ___(_) | |_   _
 / _ \/ '__/ _ \ | | | | | |
| (_) | | |  __/ | | | |_| |
 \___/|_|  \___|_|_|_|\__, |
                      |___/ \n""")


def dbconnection():
    """Neb: Used to db connection."""
    try:
        conn = sqlite3.connect('safaritesting.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS accounts (
                  ID INTEGER PRIMARY KEY AUTOINCREMENT,
                   data TEXT, username TEXT, password TEXT)''')
        return c, conn
    except Exception as err:
        print("Errore: ", err)


def user_creation():
    """Neb: Function for user creation."""
    # Db connection
    c, conn = dbconnection()

    # Getting time
    print(f'\n[?] Actual time: {datetime.now()} [?]')
    mytime = datetime.now()
    # Db relationship
    flag = False
    for row in c.execute('SELECT * FROM accounts ORDER BY ID DESC LIMIT 1'):
        if flag is not True:
            print("\nThe last user activated: ")
        oldtime = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f')
        dbemail = row[2]
        dbpass = row[3]
        flag = True

    if flag is True:
        # Checking if the time is up!

        print("Time: ", oldtime)
        print("E-mail: ", dbemail)
        print("Password: ", dbpass)
        oldtime = oldtime + timedelta(days=10)
        print("[!] Time is Up [!]" if mytime >= oldtime else
              "[!] You have time yet [!]")
        print(f'You now have other {oldtime - mytime}')


    choose = input("\n:: Do you want to make a new account? [Y/n] ")
    if choose.upper() == "Y":
        # Making new account
        namemail = input("\nInsert the name of email: ")

        global driver
        driver = webdriver.Firefox()

        driver.get("https://www.mohmal.com/it")
        driver.find_element_by_id("choose").click()

        objname = driver.find_element_by_name("name")
        objname.send_keys(namemail)

        tempemail = namemail + "@mozej.com"
        passtext = "password@01!"
        driver.find_element_by_id("next").click()
        driver.find_element_by_id("create").click()

        c.execute("INSERT INTO accounts(username) VALUES (?)", [tempemail])
        print("[!] E-MAIL MAKED: %s [!]" % (tempemail))

        driver.get("https://www.safaribooksonline.com/public/free-trial/")

        print("[!] INSTANCE MAKED [!]")

        name = driver.find_element_by_id("id_first_name")
        surname = driver.find_element_by_id("id_last_name")

        email = driver.find_element_by_id("id_email")
        password = driver.find_element_by_id("id_password1")

        name.send_keys("test")
        surname.send_keys("tests")

        email.send_keys(tempemail)
        password.send_keys(passtext)

        # End of the program
        c.execute("UPDATE accounts SET data=(?), password=(?) \
                  WHERE username = (?)", (mytime, passtext, tempemail,))
        driver.find_element_by_id("trial-button").click()
        conn.commit()
        c.close()
        driver.close()


def get_path():
    """Neb: Function that is useful for giving data."""
    driver.get("https://www.safaribooksonline.com/s/")


def main():
    """Neb: Main."""
    banner()
    user_creation()


if __name__ == '__main__':
    main()
