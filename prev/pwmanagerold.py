import os.path
import os
from cryptography.fernet import Fernet
import time
import clipboard

fileee = 'D:/Libraries/Documents/resources_py/pw.txt'


def write_key():
    if os.path.exists("D:/Libraries/Documents/resources_py/key.key"):
        pass
    else:
        key = Fernet.generate_key()
        with open("D:/Libraries/Documents/resources_py/key.key", "wb") as key_file:
            key_file.write(key)


def load_key():
    return open("D:/Libraries/Documents/resources_py/key.key", "rb").read()


def master_password():
    if os.path.exists('D:/Libraries/Documents/resources_py/master.txt'):
        password = input("Enter master password or (q)uit: ")
        with open('D:/Libraries/Documents/resources_py/master.txt', 'r') as f:
            content = f.read()
        if password == content:
            print("\nWelcome to PWMANAGER v0.0.1!")
        elif password == "q":
            f.close()
            quit()
        else:
            print("Password wrong! Try agian: ")
            f.close()
            master_password()
    else:
        with open('D:/Libraries/Documents/resources_py/master.txt', 'w') as f:
            password = input("Create master password or (q)uit: ")
            f.write(password)


def encrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
        encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def decrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
    with open(filename, "wb") as file:
        file.write(decrypted_data)


def create_file():
    if os.path.exists(fileee):
        pass
    else:
        file = open(fileee, 'w')
        file.close()


def get_help():
    with open('help.txt') as helpfile:
        content = helpfile.read()
        print(content)
        startup()


def startup():
    choose = input(
        "\nDo you want to (r)ead all, (s)earch for, (e)dit or (a)dd a password? Else (q)uit or get (h)elp." + "\n" + "\n")
    if choose == "a":
        add_password()
    elif choose == "r":
        read_all_passwords()
    elif choose == "s":
        print_all_service_names()
        search_passwords()
    elif choose == "e":
        edit_passwords()
    elif choose == "h":
        get_help()
    elif choose == "q":
        encrypt(fileee, key)
        quit()
    else:
        startup2()


def startup2():
    choose = input(
        "\nPlease only answer with \"r\", \"s\", \"a\", \"e\" or \"q\"!" + "\n\n")
    if choose == "a":
        add_password()
    elif choose == "r":
        read_all_passwords()
    elif choose == "s":
        print_all_service_names()
        search_passwords()
    elif choose == "e":
        edit_passwords()
    elif choose == "q":
        encrypt(fileee, key)
        quit()
    else:
        startup2()


def add_password():
    file = open(fileee, 'a')
    print()
    service = input("Enter service: ")
    if service == "cancel":
        startup()
    else:
        pass
    if service == "":
        print("\nService can't be blank!")
        add_password()
    else:
        pass
    file_content = open(fileee).read().splitlines()
    if "Service" in file_content and service in file_content:
        print("\nService maybe already saved, please double check:\n")
    for index, line in enumerate(file_content):
        if "Service" in line and service in line:
            print(file_content[index+0:index+3])
    for line in file_content:
        if "Service" in line and service in line:
            still_save = input(
                "\nIs the Service you want to add in this list? (y/n)\n")
            if still_save == "y":
                startup()
            elif still_save == "n":
                add_password2()
            else:
                print("Please only answer with \"y\" or \"n\"\n")
    else:
        username = input("Enter username: ")
        password = input("Enter password: ")
        print()
        srvice = "Service: " + service + "\n"
        usrnm = "Username: " + username + "\n"
        pswrd = "Password: " + password + "\n"
        file.write("------------------------------------" + "\n")
        file.write(srvice)
        file.write(usrnm)
        file.write(pswrd)
        file.close()
        startup()


def add_password2():
    file = open(fileee, 'a')
    print()
    service = input("Enter service: ")
    if service == "cancel":
        startup()
    else:
        username = input("Enter username: ")
        password = input("Enter password: ")
        print()
        srvice = "Service: " + service + "\n"
        usrnm = "Username: " + username + "\n"
        pswrd = "Password: " + password + "\n"
        file.write("------------------------------------" + "\n")
        file.write(srvice)
        file.write(usrnm)
        file.write(pswrd)
        file.close()
        startup()


def edit_passwords():
    os.system('notepad ' + fileee)
    # found = False
    # is_skipped = False
    # file = open(fileee).read().splitlines()
    # search = input("\nEnter Service you want to delete: ")
    # if search == "":
    #     print("\nSearch can't be blank!")
    #     edit_passwords()
    # elif search == "cancel":
    #     startup()
    # else:
    #     pass
    # temp_file_path = fileee + '.bak'
    # temp_file = open(temp_file_path, 'w')
    # temp_file.close()
    # for index, line in enumerate(file):
    #     if 'Service: ' in line and search in line:
    #         found = True
    #         password_section = file[index-1:index+3]
    #         # password_section = ' '.join(password_sectionw)
    #         # print(password_section)
    #     if found:
    #         with open(temp_file_path, 'a') as temp_file:
    #             for lines in enumerate(file):
    #                 if 'Service: ' not in line and search not in line:
    #                     temp_file.write(line)
    #                 else:
    #                     is_skipped = True
    #             if is_skipped:
    #                 os.remove('D:/Libraries/Documents/resources_py/pw.txt')
    #                 os.rename('D:/Libraries/Documents/resources_py/pw.txt.bak', 'D:/Libraries/Documents/resources_py/pw.txt')
    #             else:
    #                 os.remove('D:/Libraries/Documents/resources_py/pw.txt.bak')
    #         if not found:
    #             print("\nPassword for " + search + " was not found.")
    #             edit_passwords()
    startup()


def read_all_passwords():
    file = open(fileee, 'r')
    content = file.read()
    print(content)
    file.close()
    startup()


def print_all_service_names():
    print("\nAvailable Services:\n")
    with open(fileee,  'r') as fo:
        for line in fo:
            if 'Service' in line:
                out = line.replace('Service:', '')
                out = out.strip()
                print(out)


def search_passwords():
    file = open(fileee).read().splitlines()
    search = input("\nEnter service: ")
    if search == "":
        print("\nSearch can't be blank!")
        search_passwords()
    elif search == "cancel":
        startup()
    else:
        pass
    print()
    found = False
    for index, line in enumerate(file):
        if 'Service:' in line and search in line:
            print(file[index+0:index+3])
            password_itself = (file[index+2]).replace('Password: ', '')
            clipboard.copy(password_itself)
            found = True
    if not found:
        print("Password for " + search + " was not found.")
        search_passwords()
    startup()


master_password()
create_file()
key = load_key()
try:
    decrypt(fileee, key)
except:
    EnvironmentError
    print("\nYou forgot to encrypt your passwords last time you quit the program!\n" +
          "Always remember to quit the program by entering \"q\" in the console!")
    time.sleep(5)
startup()
