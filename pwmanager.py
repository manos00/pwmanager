import os
from cryptography.fernet import Fernet
import clipboard
import random
import getpass
import string
import hashlib


appdata = os.environ.get('AppData')
pw_path = appdata + '/pwmanager/pw.txt'
key_path = appdata + '/pwmanager/key.key'
master_path = appdata + '/pwmanager/master.file'
counter = 0
counter2 = 0


def write_key():
    if os.path.exists(key_path):
        pass
    else:
        key = Fernet.generate_key()
        with open(key_path, 'wb') as key_file:
            key_file.write(key)


def load_key():
    return open(key_path, 'rb').read()


def master_password():
    tries = 0
    done = False
    if os.path.exists(master_path):
        while not done:
            if tries == 0:
                sha512obj = hashlib.sha512()
                pwin = getpass.getpass('Enter master password or (q)uit: ')
                with open(master_path, 'r') as f:
                    mpw = f.read()
                    sha512obj.update(str.encode(pwin))
                    if sha512obj.hexdigest() == mpw:
                        print('\nWelcome to PWMANAGER v0.0.1!')
                        done = True
                    elif pwin == "q":
                        done = True
                        quit()
                    else:
                        tries += 1
            elif tries > 0:
                sha512obj = hashlib.sha512()
                pwin = getpass.getpass('Password wrong! Try agian: ')
                with open(master_path, 'r') as f:
                    mpw = f.read()
                    sha512obj.update(str.encode(pwin))
                    if sha512obj.hexdigest() == mpw:
                        print('\nWelcome to PWMANAGER v0.0.1!')
                        done = True
                    elif pwin == "q":
                        done = True
                        quit()
                    else:
                        tries += 1
    else:
        try:
            sha512obj = hashlib.sha512()
            os.mkdir(appdata + '/pwmanager')
            with open(master_path, 'w') as f:
                pwin = input('Create master password or (q)uit: ')
                sha512obj.update(str.encode(pwin))
                f.write(sha512obj.hexdigest())
                print('\nWelcome to PWMANAGER v0.0.1!')
                f.close
            with open(appdata + '/pwmanager/help.txt', 'w') as f:
                f.write("there is no help")
                f.close()
        except FileExistsError:
            sha512obj = hashlib.sha512()
            with open(master_path, 'w') as f:
                pwin = input('Create master password or (q)uit: ')
                sha512obj.update(str.encode(pwin))
                f.write(sha512obj.hexdigest())
            with open(appdata + '/pwmanager/help.txt', 'w') as f:
                f.write("there is no help")
                f.close()
            print('\nWelcome to PWMANAGER v0.0.1!')


def encrypt(filename, key):
    f = Fernet(key)
    with open(filename, 'rb') as file:
        FileContents = file.read()
        ContentsEncrypted = f.encrypt(FileContents)
    with open(filename, 'wb') as file:
        file.write(ContentsEncrypted)


def decrypt(filename, key):
    f = Fernet(key)
    with open(filename, 'rb') as file:
        ContentsEncrypted = file.read()
        ContentsDecrypted = f.decrypt(ContentsEncrypted)
    with open(filename, 'wb') as file:
        file.write(ContentsDecrypted)


def CreatePath():
    if os.path.exists(pw_path):
        pass
    else:
        try:
            os.mkdir(appdata + '/pwmanager')
            with open(pw_path, 'w'):
                os.close
        except FileExistsError:
            with open(pw_path, 'w'):
                os.close


def help():
    help = open(appdata + '/pwmanager/help.txt').read()
    return help


def MainMenu():
    global counter
    if counter <= 0:
        MenuIn = input(
            '\nDo you want to (r)ead all, (s)earch for, (e)dit or (a)dd a password? Else (q)uit or get (h)elp.\n\n')
    elif counter > 0:
        MenuIn = input(
            '\nPlease only answer with \"r\", \"s\", \"a\", \"e\" or \"q\"!\n\n')
    if MenuIn == "a":
        counter = 0
        AddPw()
    elif MenuIn == "r":
        counter = 0
        ReadAll()
    elif MenuIn == "s":
        counter = 0
        PrintServices()
        search()
    elif MenuIn == "e":
        counter = 0
        edit()
    elif MenuIn == "h":
        counter = 0
        print(help())
        MainMenu()
    elif MenuIn == "q":
        quit()
    else:
        counter += 1
        MainMenu()


def AddPw():
    decrypt(pw_path, key)
    global counter2
    with open(pw_path, 'a') as pwfile:
        print()
        ServiceIn = input("Enter Service: ")
        if ServiceIn == "cancel":
            encrypt(pw_path, key)
            MainMenu()
        elif ServiceIn == "":
            print("\nService can't be blank!")
            AddPw()
        else:
            pass
        FileContent = open(pw_path).read().splitlines()
        for index, line in enumerate(FileContent):
            if counter2 <= 0:
                if "Service" in line and ServiceIn in line:
                    print("\nService maybe already saved, please double check:\n")
                    print(FileContent[index+0:index+3])
                    still_save = input(
                        "\nDo you still want to register a new password? (y/n)\n")
                    if still_save == "y":
                        counter2 += 1
                        pass
                    elif still_save == "n":
                        encrypt(pw_path, key)
                        MainMenu()
                    else:
                        print("Please only answer with \"y\" or \"n\"\n")
                else:
                    pass
        else:
            username = input("Enter username: ")
            passwordin = input("Enter password: ")
            if passwordin == 'random':
                chars = string.digits + '!@#$%^&*()'
                length = int(input('Length of password:'))
                if length < 3:
                    print('Password must at least be 3 characters long!')
                    encrypt(pw_path, key)
                    MainMenu()
                total = length
                password = ''
                for i in range(length-2):
                    password += random.choice(chars)
                    total -= 1
                counter = len(string.ascii_letters)
                for letter in string.ascii_letters:
                    counter -= 1
                    if letter in password:
                        break
                    elif counter == 1:
                        password += random.choice(string.ascii_letters)
                        total -= 1
                counter = len(string.ascii_letters)
                for digit in string.digits:
                    counter -= 1
                    if digit in password:
                        break
                    elif counter == 1:
                        password += random.choice(string.digits)
                        total -= 1
                counter = len('!@#$%^&*()')
                for char in '!@#$%^&*()':
                    counter -= 1
                    if char in password:
                        break
                    elif counter == 1:
                        password += random.choice('!@#$%^&*()')
                        total -= 1
                while total != 0:
                    password += random.choice(chars)
                    total -= 1
                print()
                print(f'Your new password is "{password}".')
                clipboard.copy(password)
                print()
                srvice = "Service: " + ServiceIn + "\n"
                usrnm = "Username: " + username + "\n"
                pswrd = "Password: " + password + "\n"
                pwfile.write("------------------------------------" + "\n")
                pwfile.write(srvice)
                pwfile.write(usrnm)
                pwfile.write(pswrd)
                pwfile.close()
            else:
                print()
                srvice = "Service: " + ServiceIn + "\n"
                usrnm = "Username: " + username + "\n"
                pswrd = "Password: " + passwordin + "\n"
                pwfile.write("------------------------------------" + "\n")
                pwfile.write(srvice)
                pwfile.write(usrnm)
                pwfile.write(pswrd)
                pwfile.close()
            counter2 = 0
            encrypt(pw_path, key)
            MainMenu()

# this might seem a little confusing as i tried to make a method to edit the passwords but it didnt work so i just made it open notepad


def edit():
    decrypt(pw_path, key)
    os.system('notepad ' + pw_path)
    # found = False
    # is_skipped = False
    # file = open(pw_path).read().splitlines()
    # SearchIn = input("\nEnter Service you want to delete: ")
    # if SearchIn == "":
    #     print("\nSearch can't be blank!")
    #     edit()
    # elif SearchIn == "cancel":
    #     MainMenu()
    # else:
    #     pass
    # temp_file_path = pw_path + '.bak'
    # temp_file = open(temp_file_path, 'w')
    # temp_file.close()
    # for index, line in enumerate(file):
    #     if 'Service: ' in line and SearchIn in line:
    #         found = True
    #         password_section = file[index-1:index+3]
    #         # password_section = ' '.join(password_sectionw)
    #         # print(password_section)
    #     if found:
    #         with open(temp_file_path, 'a') as temp_file:
    #             for lines in enumerate(file):
    #                 if 'Service: ' not in line and SearchIn not in line:
    #                     temp_file.write(line)
    #                 else:
    #                     is_skipped = True
    #             if is_skipped:
    #                 os.remove('D:/Libraries/Documents/resources_py/pwtest.txt')
    #                 os.rename('D:/Libraries/Documents/resources_py/pwtest.txt.bak', 'D:/Libraries/Documents/resources_py/pwtest.txt')
    #             else:
    #                 os.remove('D:/Libraries/Documents/resources_py/pwtest.txt.bak')
    #         if not found:
    #             print("\nPassword for " + SearchIn + " was not found.")
    #             edit()
    encrypt(pw_path, key)
    MainMenu()


def ReadAll():
    decrypt(pw_path, key)
    with open(pw_path, 'r') as pw:
        content = pw.read()
        print(content)
        pw.close()
    encrypt(pw_path, key)
    MainMenu()


def PrintServices():
    decrypt(pw_path, key)
    print("\nAvailable Services:\n")
    with open(pw_path, 'r') as pw:
        for line in pw:
            if 'Service' in line:
                out = line.replace('Service:', '')
                out = out.strip()
                print(out)
    encrypt(pw_path, key)


def search():
    decrypt(pw_path, key)
    pw = open(pw_path).read().splitlines()
    SearchIn = input("\nEnter Service: ")
    if SearchIn == "":
        print("\nSearch can't be blank!")
        encrypt(pw_path, key)
        search()
    elif SearchIn == "cancel":
        encrypt(pw_path, key)
        MainMenu()
    else:
        pass
    print()
    found = False
    for index, line in enumerate(pw):
        if 'Service:' in line and SearchIn in line:
            print(pw[index+0:index+3])
            password_itself = (pw[index+2]).replace('Password: ', '')
            clipboard.copy(password_itself)
            found = True
    if not found:
        print("Password for " + SearchIn + " was not found.")
        encrypt(pw_path, key)
        search()
    encrypt(pw_path, key)
    MainMenu()


master_password()
write_key()
key = load_key()
CreatePath()
try:
    decrypt(pw_path, key)
    encrypt(pw_path, key)
except:
    encrypt(pw_path, key)
    print("\nYour passwords have not been encrypted since the last time you used pwmanager.",
          "This error is most likely caused by an unexpected shutdown of the program during an unfinished action.")
# time.sleep(5)
MainMenu()
