import tkinter
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
DARK_BG_COLOR = "#91C2AF"
WORDS_TO_LEARN = []

# Importe et converti le .csv en dict de laquelle on extrait la list des mots français
words_file = pandas.read_csv('./data/french_words.csv')
words_dict = pandas.DataFrame.to_dict(words_file)
french_words = [words_dict["French"][i] for i in words_dict["French"]]
total_words_len = len(french_words)

window = tkinter.Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# -------- : Gestions des boutons : --------- #
def right_answer():
    generate_word()

def wrong_answer():
    global WORDS_TO_LEARN
    WORDS_TO_LEARN.append(generate_word())


def generate_word():
    global WORDS_TO_LEARN, french_words, words_file

    # Réinitialise le text des labels
    title_word.config(text="")
    content_word.config(text="")

    try:
        # Message de fin
        if not french_words:
            print(f"Completed all questions. Mistakes: {len(WORDS_TO_LEARN)}")
            return None

        random_french_word = random.choice(french_words)
        french_word_index = words_file[words_file["French"] == random_french_word].index[0]
        associated_english_word = words_file["English"][french_word_index]

        # Suivi du numéro de la question
        remaining = len(french_words) - 1
        print(f"Questions remaining: {remaining}/{len(words_file)}")

        # Enlève le mot joué de la list
        french_words.remove(random_french_word)
        flip_card(random_french_word, associated_english_word)

        return random_french_word

    except Exception as e:
        print(f"Error generating word: {e}")
        return None


def flip_card(random_french, associated_english):
    # Affiche le côté français de la carte
    title_word.config(text="French", bg="white", fg="black")
    content_word.config(text=random_french, bg="white", fg="black")
    text_frame.config(bg="white")
    card_label.config(image=card_front)

    # Retourne du côté anglais au bout de 3s
    window.after(3000, lambda e=associated_english: flip_to_english(e))


def flip_to_english(english_word):
    # Affiche le côté anglais de la carte
    title_word.config(text="English", bg=DARK_BG_COLOR, fg="white")
    content_word.config(text=english_word, bg=DARK_BG_COLOR, fg="white")
    text_frame.config(bg=DARK_BG_COLOR)
    card_label.config(image=card_back)

# ---------------- : UI : --------------------#
# Images card
card_front = tkinter.PhotoImage(file='./images/card_front.png')
card_back = tkinter.PhotoImage(file='./images/card_back.png')

# Card
card_label = tkinter.Label(window, image=card_front, bg=BACKGROUND_COLOR)
card_label.grid(column=0, row=0, columnspan=2)

# Frame
text_frame = tkinter.Frame(card_label, bg="white",width=800,height=526)
text_frame.place(relx=0.5, rely=0.5, anchor="center")

# Text labels
title_word = tkinter.Label(
    text_frame,
    text="Text",
    font=("Arial", 40, "italic"),
)
title_word.pack()

content_word = tkinter.Label(
    text_frame,
    text="Word",
    font=("Arial", 60, "bold"),
)
content_word.pack()

# Images boutons
right_image = tkinter.PhotoImage(file='./images/right.png')
wrong_image = tkinter.PhotoImage(file='./images/wrong.png')

# Boutons
right_button = tkinter.Button(
    window,
    image=right_image,
    highlightthickness=0,
    bg=BACKGROUND_COLOR,
    borderwidth=0,
    command=right_answer
)
right_button.grid(column=1, row=1)

wrong_button = tkinter.Button(
    window,
    image=wrong_image,
    highlightthickness=0,
    bg=BACKGROUND_COLOR,
    borderwidth=0,
    command=wrong_answer
)
wrong_button.grid(column=0, row=1)


generate_word()
window.mainloop()