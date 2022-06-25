"""Password Manager Main file"""
from tkinter import *
from tkinter import messagebox
import json
import pyperclip
from password_generator import password_generator

#  UI COLORS AND FONT 
WINDOW_BG = "#111d5e"
FIELD_COLORS = "#dddddd"
FIELD_FONT_COLOR = "#c70039"
LABEL_COLOR = "white"
FONT = ("Courier", 15, "normal")

#  PASSWORD GENERATOR 
class manager():
    def get_password():
    
        password = password_generator()
    
        pyperclip.copy(password)
    # clear password entry widget
        password_entry.delete(0, END)
    
        password_entry.insert(END, password)


#  SAVE PASSWORD (ALL JSON)
    def database_manager(new_user_entry):
        try:
        # seeing if there is any old passwords data file
            with open("data.json", mode="r") as old_password_file:
                password_data = json.load(old_password_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open("data.json", mode="w") as new_password_file:
                json.dump(new_user_entry, new_password_file, indent=4)
    # if there is old password data
        else:
        #  New user entry json data will be updated to the old passwords data
            password_data.update(new_user_entry)
        # Writing either the updated password data or the new user entry json data
            with open("data.json", mode="w") as old_password_file:
                json.dump(password_data, old_password_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


    def save_password():
        website = website_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        if len(website) == 0 or len(password) == 0:
            messagebox.showwarning(title="Oops", message="Please make sure you have not left any fields empty")
        else:
            is_ok = messagebox.askokcancel(title="Confirm entries", message=f"These are the details you entered\n"
                                                                        f"Email: {email}"
                                                                        f"\nPassword: {password}\nIs it okay to save ?")
            if is_ok:
                pyperclip.copy(password)
                new_entry_in_json = {
                    website:
                        {
                            "Email": email,
                            "Password": password
                        }
                }
                manager.database_manager(new_entry_in_json)


#  SAVE PASSWORD 
    def search_password():
    # Getting user website entry
        website = website_entry.get()
    # Get password data
        if len(website) == 0:
            messagebox.showwarning(title="Oops", message="Please enter a website to search")
        else:
        # Try to see if password files exit ,is in JSON, and not blank
            try:
                with open("data.json", mode="r") as old_password_file:
                # reading old password data
                    password_data = json.load(old_password_file)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                messagebox.showwarning(title="No passwords saved", message="Sorry, you have not saved any password before")
            else:
                if website in password_data:
                    email = password_data[website]["Email"]
                    password = password_data[website]["Password"]
                    is_clipboard = messagebox.askokcancel(title=website, message=f"Email: {email}\nPassword: {password}"
                                                                             f"\n\nSave to clipboard ?")
                    if is_clipboard:
                        pyperclip.copy(password)
                        messagebox.showinfo(title="Saved to clipboard", message="Password has been saved to clipboard")
            # IF the searched website is not in the database
                else:
                    messagebox.showwarning(title="Password not saved for this website", message=f"The password for {website}\n"
                                                                                         f"has not been saved")


# Fronend SETUP 
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, bg=WINDOW_BG)

#  WIDGETS SETUP 
PASS_IMG = PhotoImage(file="lock.png")
canvas = Canvas(width=250, height=200, bg=WINDOW_BG, highlightthickness=0)
canvas.config()
canvas.create_image(100, 100, image=PASS_IMG)
canvas.grid(column=1, row=0)

# Label
website_label = Label(text="Website", bg=WINDOW_BG, padx=20, font=FONT, fg=LABEL_COLOR)
website_label.grid(column=0, row=1, sticky=W)

# Label for Email/Username
email_label = Label(text="Email/Username", bg=WINDOW_BG, padx=20, font=FONT, fg=LABEL_COLOR)
email_label.grid(column=0, row=2, sticky=W)

# Label for Password
password_label = Label(text="Password", bg=WINDOW_BG, padx=20, font=FONT, fg=LABEL_COLOR)
password_label.grid(column=0, row=3,sticky=W)
window.grid_columnconfigure(1, weight=1)
# Entry widgets
website_entry = Entry(width=30, bg=FIELD_COLORS, fg=FIELD_FONT_COLOR, font=FONT)
website_entry.insert(END, string="")
website_entry.grid(column=1, row=1)
# starting cursor focus
website_entry.focus()
email_entry = Entry(width=30, bg=FIELD_COLORS, fg=FIELD_FONT_COLOR, font=FONT)
email_entry.insert(END, string="")
email_entry.grid(column=1, row=2)
# set default email
email_entry.insert(0, "prathameshwani1933@gmail.com")

password_entry = Entry(width=30, bg=FIELD_COLORS, fg=FIELD_FONT_COLOR, font=FONT)
password_entry.insert(END, string="")
password_entry.grid(column=1, row=3)

# buttons
search_button = Button(text="Search", padx=95, font=FONT, command=manager.search_password)
search_button.grid(column=3, row=1)

generate_button = Button(text="Generate Password", command=manager.get_password, font=FONT)
generate_button.grid(column=3, row=3)

add_button = Button(text="Add", width=36, command=manager.save_password, font=FONT)
add_button.grid(column=1, row=5, columnspan=2, sticky=W)

window.mainloop()