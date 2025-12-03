import os
import time
import threading
import zipfile

# Colors
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
P = '\033[95m'
C = '\033[96m'
W = '\033[97m'
N = '\033[0m'

clear = lambda: os.system('clear')

#######################################
# BANNERS
#######################################
def banner():
    clear()
    print(f"""
{R}***********************************
{G}*   LINUX EXPERT           V2.0   
{B}*       IMRAN AFRIDI              
{P}*          ZIP CRACKER TOOL       
{C}*   V2.0      AUTO DETECT MODE    
{R}***********************************
{N}""")

def banner2():
    print(f"""
{Y}***************************************
{G}* MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
{B}* M                             M
{P}* M IMRAN AFRIDI                M
{C}* M       AUTO ZIP DETECTOR     M
{R}* MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
{G}* CODED BY IMRAN AFRIDI
{Y}***************************************
{N}""")

#######################################
# SEARCH ZIP FILE
#######################################
def auto_search(filename):
    if filename.lower() == "back":
        return "BACK"

    root_path = "/storage/emulated/0"
    print(f"{Y}Searching for: {filename}{N}\n")

    for root, dirs, files in os.walk(root_path):
        if filename in files:
            found = os.path.join(root, filename)
            print(f"{G}✔ Found: {found}{N}")
            return found

    print(f"{R}✘ File not found!{N}")
    return None


#######################################
# GLOBAL
#######################################
stop_flag = False
counter_lock = threading.Lock()
attempt_counter = {4:0, 5:0, 6:0, 7:0, 8:0}

def update_counter(digits):
    with counter_lock:
        attempt_counter[digits] += 1
        print(f"{C}[{digits}-digit] Tr: {attempt_counter[digits]}{N}", end='\r')


#######################################
# BRUTEFORCE FUNCTION
#######################################
def digit_bruteforce(zip_path, digits, label):
    global stop_flag
    stop_flag = False
    attempt_counter[digits] = 0

    start_time = time.time()    # ⬅️ Timer start

    start_num = 0
    end_num = 10 ** digits

    for number in range(start_num, end_num):
        if stop_flag:
            return

        pwd = str(number).zfill(digits)

        update_counter(digits)

        print(f"{G}Trying: {pwd}{N}", end="\r")

        try:
            with zipfile.ZipFile(zip_path) as zf:
                zf.extractall(pwd=pwd.encode())

            stop_flag = True
            total_time = round(time.time() - start_time, 2)   # ⬅️ Timer stop

            print(f"\n\n{P}[{label}] PASSWORD FOUND → {pwd}{N}")
            print(f"{Y}Time taken: {total_time} seconds{N}")   # ⬅️ Display time

            return

        except:
            pass

    print(f"\n{R}Password not found in {digits}-digit range!{N}")


#######################################
# START SINGLE DIGIT ATTACK
#######################################
def start_single_digit_attack(zip_path, digits):
    print(f"\n{Y}Starting {digits}-digit brute-force...{N}\n")

    t = threading.Thread(target=digit_bruteforce, args=(zip_path, digits, f"{digits}-digit"))
    t.start()
    t.join()

    input(f"\n{G}Press ENTER to go back...{N}")


#######################################
# WORDLIST ATTACK
#######################################
def crack_zip_wordlist(zip_path, wordlist):
    print(f"{Y}\nUsing wordlist: {wordlist}{N}")

    try:
        with open(wordlist, 'r') as f:
            for password in f:
                password = password.strip()
                print(f"{C}Trying: {password}{N}", end='\r')

                try:
                    with zipfile.ZipFile(zip_path) as zf:
                        zf.extractall(pwd=password.encode())
                    print(f"\n{P}Password found: {password}{N}")
                    break
                except:
                    pass
            else:
                print(f"{R}\nPassword not found in wordlist!{N}")

    except:
        print(f"{R}Wordlist read error!{N}")

    input(f"\n{G}Press ENTER to go back...{N}")


#######################################
# DIGIT MENU
#######################################
def digit_menu(zip_path):
    while True:
        print(f"""
{Y}Select PIN length:{N}
{G}1.{N} 4-digit PIN
{G}2.{N} 5-digit PIN
{G}3.{N} 6-digit PIN
{G}4.{N} 7-digit PIN
{G}5.{N} 8-digit PIN
{R}6.{N} Back
""")

        choice = input(f"{C}Enter choice: {N}")

        if choice == "1": start_single_digit_attack(zip_path, 4)
        elif choice == "2": start_single_digit_attack(zip_path, 5)
        elif choice == "3": start_single_digit_attack(zip_path, 6)
        elif choice == "4": start_single_digit_attack(zip_path, 7)
        elif choice == "5": start_single_digit_attack(zip_path, 8)
        elif choice == "6": return
        else:
            print(f"{R}Invalid choice!{N}")


#######################################
# METHOD MENU
#######################################
def method_menu(zip_path):
    while True:
        print(f"""
{Y}Choose method:{N}
{G}1.{N} Numeric PIN (4–8 digit)
{B}2.{N} Wordlist attack
{R}3.{N} Back
""")

        choice = input(f"{C}Enter choice: {N}")

        if choice == "1":
            digit_menu(zip_path)
        elif choice == "2":
            wordlist_menu(zip_path)
        elif choice == "3":
            return
        else:
            print(f"{R}Invalid choice!{N}")


#######################################
# WORDLIST MENU
#######################################
def wordlist_menu(zip_path):
    while True:
        wl = input(f"{B}Enter wordlist filename (or 'back'): {N}")

        wl_path = auto_search(wl)

        if wl_path == "BACK":
            return
        if wl_path:
            crack_zip_wordlist(zip_path, wl_path)
            return


#######################################
# ZIP MENU
#######################################
def zip_menu():
    while True:
        zip_name = input(f"{Y}Enter ZIP filename (or 'back'): {N}")
        zip_path = auto_search(zip_name)

        if zip_path == "BACK":
            return

        if zip_path:
            method_menu(zip_path)
            return


#######################################
# MAIN MENU
#######################################
def main_menu():
    while True:
        banner()
        banner2()

        print(f"{G}1.{N} Crack ZIP")
        print(f"{R}2.{N} Exit\n")

        choice = input(f"{C}Enter choice: {N}")

        if choice == "1":
            zip_menu()
        elif choice == "2":
            print(f"{G}Exiting...{N}")
            return
        else:
            print(f"{R}Invalid choice!{N}")
            time.sleep(1)


#######################################
# START PROGRAM
#######################################
main_menu()
