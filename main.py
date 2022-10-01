import json
from tkinter import *
from tkinter import messagebox
from random import choice, shuffle
import pyperclip


# ---------------------------- SEARCH ------------------------------- #
# Lets users search for their login information based on the website.

def search():
    website_name = website_entry.get()
    try:
        with open("data.json", "r") as read_file:
            data = json.load(read_file)
    except FileNotFoundError:
        messagebox.showinfo(title="No credentials", message="You don't have an account saved on that website.")
    else:
        if website_name in data:
            email = data[website_name]["email"]
            password = data[website_name]["password"]
            messagebox.showinfo(title=f"{website_name}", message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="No credentials", message="You don't have an account saved on that website.")
    website_entry.delete(0, END)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    new_password = [choice(letters) for _ in range(8)]

    new_password += [choice(numbers) for _ in range(4)]

    new_password += [choice(symbols) for _ in range(4)]

    shuffle(new_password)

    random_password = "".join(new_password)

    password_label_entry.insert(0, random_password)
    pyperclip.copy(random_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website_name = website_entry.get()
    email_name = email_username_entry.get()
    password = password_label_entry.get()
    new_data = {
        website_name: {
            "email": email_name,
            "password": password,
        }
    }

    if len(website_name) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Hey, you left some fields blank!")
    else:
        try:
            with open("data.json", "r") as login_credentials:
                data = json.load(login_credentials)
        except FileNotFoundError:
            with open("data.json", "w") as login_credentials:
                json.dump(new_data, login_credentials, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as login_credentials:
                json.dump(data, login_credentials, indent=4)
        finally:
            website_entry.delete(0, END)
            password_label_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
# This is the User Interface. User can insert the website name, generate a new password, and add their information
# to a txt file.

window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

website = Label(text="Website:")
website.grid(column=0, row=1)
website_entry = Entry(width=34, borderwidth=2)
website_entry.focus()
website_entry.grid(column=1, row=1)

email_username = Label(text="Email/Username:")
email_username.grid(column=0, row=2)
email_username_entry = Entry(width=53, borderwidth=2)
# You can input your email here for quick generations and saving.
email_username_entry.insert(0, "Mianlanddev@gmail.com")
email_username_entry.grid(column=1, row=2, columnspan=2)

password_label = Label(text="Password:", width=21)
password_label.grid(column=0, row=3)
password_label_entry = Entry(width=34, borderwidth=2)
password_label_entry.grid(column=1, row=3, sticky=E)

search_button = Button(text="Search", width=15, command=search)
search_button.grid(column=2, row=1, sticky=W)

gen_pass = Button(text="Generate Password", width=15, command=generate_password)
gen_pass.grid(column=2, row=3, sticky=W)

add_button = Button(text="Add", width=45, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
