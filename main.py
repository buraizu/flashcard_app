from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
vocab_data = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    vocab_data = original_data.to_dict(orient="records")
else:
    vocab_data = data.to_dict(orient="records")

# My dictionary solution
# vocab_dict = {row.French: row.English for (index, row) in vocab_data.iterrows()}
# vocab_choice = random.choice(list(vocab_dict.items()))

# Course dictionary solution
# vocab_data = pandas.read_csv("data/words_to_learn.csv")
# vocab_list = vocab_data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(vocab_data)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_image)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_image)


def remove_word():
    vocab_data.remove(current_card)
    updated_vocab_data = pandas.DataFrame(vocab_data)
    updated_vocab_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()
# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Flash-card app")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

card_front_image = PhotoImage(file="./images/card_front.png")
card_background = canvas.create_image(400, 263, image=card_front_image)

card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60))

card_back_image = PhotoImage(file="./images/card_back.png")
right_image = PhotoImage(file="./images/right.png")
wrong_image = PhotoImage(file="./images/wrong.png")




# Labels
# site_label = Label(text="Website:")
# site_label.grid(column=0, row=1)
# email_label = Label(text="Email/Username:")
# email_label.grid(column=0, row=2)
# password_label = Label(text="Password: ")
# password_label.grid(column=0, row=3)

# Entries
# website_entry = Entry(width=21)
# website_entry.grid(column=1, row=1)
# email_entry = Entry(width=35)
# email_entry.grid(column=1, row=2, columnspan=2)
# password_entry = Entry(width=21)
# password_entry.grid(column=1, row=3)

# Buttons
check_button = Button(image=right_image, highlightthickness=0, command=remove_word)
check_button.grid(row=1, column=1)
x_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
x_button.grid(row=1, column=0)
# search_button = Button(text="Search", command=search)
# search_button.grid(column=2, row=1)

next_card()

window.mainloop()
