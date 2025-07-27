from tkinter import *
from tkinter import font as tkFont
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser

# Constants
API_KEY = '11d06c59eefb43b0a77d59e51d85ce11'
API_URL = 'https://api.spoonacular.com/recipes/complexSearch'

# App window
window = Tk()
window.title("Recipe Finder")
window.geometry("900x600")
window.resizable(False, False)

# Load and set background image
bg_image = Image.open(r"C:\Users\thull\Downloads\recipe-finder.jpeg").resize((900, 600))
bg_photo = ImageTk.PhotoImage(bg_image)

background_label = Label(window, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Fonts
font_title = tkFont.Font(family="Arial", size=26, weight="bold")
font_label = tkFont.Font(family="Arial", size=14)
font_button = tkFont.Font(family="Arial", size=12)

# Title
title_label = Label(
    window,
    text="Explore Tastes,\nCreate Memories",
    font=font_title,
    bg="#f0f0f0",
    fg="#333333",
    justify="center",
    padx=20,
    pady=10
)
title_label.place(relx=0.5, y=60, anchor="center")

# Entry field
entry = Entry(window, font=font_label, width=30, bg="white", fg="black", relief=SOLID, bd=1)
entry.place(relx=0.5, y=140, anchor="center")

# Frame for results
results_frame = Frame(window, bg="#f0f0f0")
results_frame.place(x=100, y=200, width=700, height=350)

canvas = Canvas(results_frame, bg="#f0f0f0", highlightthickness=0)
scrollbar = Scrollbar(results_frame, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas, bg="#f0f0f0")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


def search_recipes():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    query = entry.get()
    if not query:
        return

    params = {
        "query": query,
        "number": 5,
        "apiKey": API_KEY
    }

    try:
        response = requests.get(API_URL, params=params)
        data = response.json()

        for recipe in data.get("results", []):
            card = Frame(scrollable_frame, bg="#ffffff", padx=10, pady=10, relief=RIDGE, bd=1)
            card.pack(pady=10, fill="x", padx=10)

            title = Label(card, text=recipe['title'], font=font_label, bg="#ffffff", fg="#222222", wraplength=500, justify="left")
            title.pack(anchor="w")

            if recipe.get("image"):
                try:
                    image_url = recipe["image"]
                    img_data = requests.get(image_url).content
                    img = Image.open(BytesIO(img_data)).resize((100, 100))
                    photo = ImageTk.PhotoImage(img)

                    img_label = Label(card, image=photo, bg="#ffffff")
                    img_label.image = photo
                    img_label.pack(side="right")
                except:
                    pass

            link = Label(card, text="View on Spoonacular", fg="blue", bg="#ffffff", cursor="hand2", font=("Arial", 10, "underline"))
            link.pack(anchor="w", pady=(5, 0))
            link.bind("<Button-1>", lambda e, id=recipe["id"]: open_recipe(id))

    except Exception as e:
        error_label = Label(scrollable_frame, text=f"Error: {e}", fg="red", bg="#f0f0f0")
        error_label.pack()


def open_recipe(recipe_id):
    url = f"https://spoonacular.com/recipes/{recipe_id}"
    webbrowser.open(url)


# Search button
search_btn = Button(window, text="Find Recipes", font=font_button, command=search_recipes, bg="#00bfff", fg="white", padx=10, pady=5)
search_btn.place(relx=0.5, y=180, anchor="center")

window.mainloop()

