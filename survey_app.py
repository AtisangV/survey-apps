import tkinter as tk
from tkinter import messagebox
import sqlite3


import sqlite3
from tkinter import ttk
def connect_db():
    return sqlite3.connect('survey.db')


# Function to add survey to database
def submit_survey():
    full_name = entry_name.get()
    email = entry_email.get()
    age  = entry_age.get()
    contact_number = entry_contact.get()
    favorite_foods = [var_pizza.get(), var_pasta.get(), var_pap.get(), var_chicken.get(), var_beef.get(), var_other.get()]
    favorite_foods = [food for food in favorite_foods if food]  # Filter out empty strings
    favorite_foods = ", ".join(favorite_foods)
    ratings = [str(var_watch_movies.get()), str(var_listen_radio.get()), str(var_eat_out.get()), str(var_watch_tv.get())]
    ratings = ", ".join(ratings)



    if not full_name or not email or not age or not contact_number or not favorite_foods or not ratings:
        messagebox.showerror("Error", "Please fill out all fields")
        return

    if not (5 <= int(age) <= 120):
        messagebox.showerror("Error", "Age must be between 5 and 120")
        return

    conn = sqlite3.connect('survey.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO survey (full_name, email, age, contact_number, favorite_foods, ratings)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (full_name, email, age, contact_number, favorite_foods, ratings))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Survey submitted successfully!")
    clear_form()

   

# Function to clear the form
def clear_form():
    entry_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_contact.delete(0, tk.END)
    var_pizza.set("")
    var_pasta.set("")
    var_pap.set("")
    var_chicken.set("")
    var_beef.set("")
    var_other.set("")
    var_watch_movies.set(0)
    var_listen_radio.set(0)
    var_eat_out.set(0)
    var_watch_tv.set(0)

# Function to view survey results
def view_results():
    conn = sqlite3.connect('survey.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM survey')
    surveys = cursor.fetchall()
    conn.close()

    if not surveys:
        messagebox.showinfo("Info", "No surveys available")
        return

    # Calculations
    total_surveys = len(surveys)
    ages = [int(survey[3]) for survey in surveys]
    avg_age = sum(ages) / total_surveys
    oldest_age = max(ages)
    pizza_lovers = sum([1 for survey in surveys if 'Pizza' in survey[5].split(', ')])
    pizza_percentage = (pizza_lovers / total_surveys) * 100
    ratings = [[int(r) for r in survey[6].split(', ')] for survey in surveys]
    avg_ratings = [sum(r) / total_surveys for r in zip(*ratings)]

    results_text = f"""
    Total number of surveys: {total_surveys}
    Average age of participants: {avg_age:.1f}
    Oldest participant age: {oldest_age}
    Percentage of people who like Pizza: {pizza_percentage:.1f}%
    people who like to watch movie: {avg_ratings[0]:.1f}
    people who like to listen to radio: {avg_ratings[1]:.1f}
    people who like to eat out: {avg_ratings[2]:.1f}
    people who like to watch tv: {avg_ratings[3]:.1f}
    """

    messagebox.showinfo("Survey Results", results_text)

# Create the main application window
root = tk.Tk()
root.title("Survey Application")

# Create the frames for navigation and content
frame_nav = tk.Frame(root)
frame_nav.pack(side=tk.TOP, fill=tk.X)

frame_content = tk.Frame(root)
frame_content.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Navigation buttons
def show_survey_form():
    for widget in frame_content.winfo_children():
        widget.destroy()
    create_survey_form(frame_content)

def show_survey_results():
    for widget in frame_content.winfo_children():
        widget.destroy()
    view_results()

btn_survey_form = tk.Button(frame_nav, text="Fill Out Survey", command=show_survey_form)
btn_survey_form.pack(side=tk.LEFT)

btn_survey_results = tk.Button(frame_nav, text="View Survey Results", command=show_survey_results)
btn_survey_results.pack(side=tk.LEFT)

# Survey form
def create_survey_form(parent):
    tk.Label(parent, text="Full Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    global entry_name
    entry_name = tk.Entry(parent)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(parent, text="Email:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    global entry_email
    entry_email = tk.Entry(parent)
    entry_email.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(parent, text="Age:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
    global entry_age
    entry_age = tk.Entry(parent)
    entry_age.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(parent, text="Contact Number:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
    global entry_contact
    entry_contact = tk.Entry(parent)
    entry_contact.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(parent, text="Favorite Foods:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
    global var_pizza, var_pasta, var_pap, var_chicken, var_beef, var_other
    var_pizza = tk.StringVar()
    var_pasta = tk.StringVar()
    var_pap = tk.StringVar()
    var_chicken = tk.StringVar()
    var_beef = tk.StringVar()
    var_other = tk.StringVar()
    tk.Checkbutton(parent, text="Pizza", variable=var_pizza, onvalue="Pizza", offvalue="").grid(row=4, column=1, sticky=tk.W)
    tk.Checkbutton(parent, text="Pasta", variable=var_pasta, onvalue="Pasta", offvalue="").grid(row=4, column=2, sticky=tk.W)
    tk.Checkbutton(parent, text="Pap and Wors", variable=var_pap, onvalue="Pap and Wors", offvalue="").grid(row=4, column=3, sticky=tk.W)
    tk.Checkbutton(parent, text="Chicken Stir Fry", variable=var_chicken, onvalue="Chicken Stir Fry", offvalue="").grid(row=4, column=4, sticky=tk.W)
    tk.Checkbutton(parent, text="Beef Stir Fry", variable=var_beef, onvalue="Beef Stir Fry", offvalue="").grid(row=4, column=5, sticky=tk.W)
    tk.Checkbutton(parent, text="Other", variable=var_other, onvalue="Other", offvalue="").grid(row=4, column=6, sticky=tk.W)

    tk.Label(parent, text="Rate the following from 1 to 5,with 1 being ''strongly agree'' and 5 being ''strongly disagree.''").grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)
    global var_watch_movies, var_listen_radio, var_eat_out, var_watch_tv
    var_watch_movies = tk.IntVar()
    var_listen_radio = tk.IntVar()
    var_eat_out = tk.IntVar()
    var_watch_tv = tk.IntVar()

    tk.Label(parent, text="I like to watch movies:").grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
    tk.Radiobutton(parent, text="1", variable=var_watch_movies, value=1).grid(row=6, column=1)
    tk.Radiobutton(parent, text="2", variable=var_watch_movies, value=2).grid(row=6, column=2)
    tk.Radiobutton(parent, text="3", variable=var_watch_movies, value=3).grid(row=6, column=3)
    tk.Radiobutton(parent, text="4", variable=var_watch_movies, value=4).grid(row=6, column=4)
    tk.Radiobutton(parent, text="5", variable=var_watch_movies, value=5).grid(row=6, column=5)

    tk.Label(parent, text="I like to listen to radio:").grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
    tk.Radiobutton(parent, text="1", variable=var_listen_radio, value=1).grid(row=7, column=1)
    tk.Radiobutton(parent, text="2", variable=var_listen_radio, value=2).grid(row=7, column=2)
    tk.Radiobutton(parent, text="3", variable=var_listen_radio, value=3).grid(row=7, column=3)
    tk.Radiobutton(parent, text="4", variable=var_listen_radio, value=4).grid(row=7, column=4)
    tk.Radiobutton(parent, text="5", variable=var_listen_radio, value=5).grid(row=7, column=5)

    print(tk.Label(parent, text="I like to eat out:").grid(row=8, column=0, padx=10, pady=5, sticky=tk.W))
    tk.Radiobutton(parent, text="1", variable=var_eat_out, value=1).grid(row=8, column=1)
    tk.Radiobutton(parent, text="2", variable=var_eat_out, value=2).grid(row=8, column=2)
    tk.Radiobutton(parent, text="3", variable=var_eat_out, value=3).grid(row=8, column=3)
    tk.Radiobutton(parent, text="4", variable=var_eat_out, value=4).grid(row=8, column=4)
    tk.Radiobutton(parent, text="5", variable=var_eat_out, value=5).grid(row=8, column=5)

    tk.Label(parent, text="I like to watch TV:").grid(row=9, column=0, padx=10, pady=5, sticky=tk.W)
    tk.Radiobutton(parent, text="1", variable=var_watch_tv, value=1).grid(row=9, column=1)
    tk.Radiobutton(parent, text="2", variable=var_watch_tv, value=2).grid(row=9, column=2)
    tk.Radiobutton(parent, text="3", variable=var_watch_tv, value=3).grid(row=9, column=3)
    tk.Radiobutton(parent, text="4", variable=var_watch_tv, value=4).grid(row=9, column=4)
    tk.Radiobutton(parent, text="5", variable= var_watch_tv, value=5).grid(row=9, column=5)

    tk.Button(parent, text="Submit", command=submit_survey).grid(row=10, column=1, columnspan=2, pady=10)

# Initialize the content by showing the survey form
show_survey_form()

# Start the main application loop
root.mainloop()
