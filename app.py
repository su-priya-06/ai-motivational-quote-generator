import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import random
import pyperclip
import pyttsx3
import os

# Load quotes into categories
def load_quotes(filename):
    categories = {}
    current_category = None
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('---') and line.endswith('---'):
                current_category = line.strip('- ').strip()
                categories[current_category] = []
            elif line:
                categories[current_category].append(line.strip('"'))

    return categories

# Random Quote Generator
def get_random_quote(selected_category):
    if selected_category == "All":
        all_quotes = sum(quotes_by_category.values(), [])
        return random.choice(all_quotes)
    else:
        return random.choice(quotes_by_category.get(selected_category, []))

# Copy Quote
def copy_quote():
    quote = quote_label['text']
    pyperclip.copy(quote)
    messagebox.showinfo("Copied!", "Quote copied to clipboard!")

# Speak Quote
def speak_quote():
    quote = quote_label['text']
    engine.say(quote)
    engine.runAndWait()

# Generate New Quote
def generate_new_quote():
    selected_category = category_var.get()
    new_quote = get_random_quote(selected_category)
    quote_label.config(text=new_quote)

# Change Background Image
def change_background():
    global bg_index
    bg_index = (bg_index + 1) % len(bg_images)
    resize_background()
    root.after(10000, change_background)  # change every 10 seconds

# Resize background to match window size
def resize_background(event=None):
    w, h = root.winfo_width(), root.winfo_height()
    image = Image.open(os.path.join(bg_folder, bg_files[bg_index])).resize((w, h), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    background_label.config(image=photo)
    background_label.image = photo

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if 'female' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# --- Main App ---
root = tk.Tk()
root.title("Motivational Quote Generator")
root.geometry("1200x800")
root.configure(bg="#fef6f5")

# Load Quotes
quotes_by_category = load_quotes("quotes.txt")

# Load Background Images
bg_folder = "assets"
bg_files = ["bg1.jpg", "bg2.jpg", "bg3.jpg", "bg4.jpg"]
bg_images = [os.path.join(bg_folder, f) for f in bg_files]
bg_index = 0

# Initial background
bg_image = Image.open(bg_images[bg_index])
bg_photo = ImageTk.PhotoImage(bg_image)
background_label = tk.Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Transparent frame over background
frame = tk.Frame(root, bg="#ffffff", bd=0)
frame.place(relx=0.5, rely=0.1, anchor="n")

# Title Label
title_label = tk.Label(frame, text="AI Motivational Quote Generator", font=("Georgia", 28, "bold"), bg="#ffffff", fg="#5a5a5a")
title_label.pack(pady=10)

# Category Dropdown
category_var = tk.StringVar()
category_var.set("All")

categories = ["All"] + list(quotes_by_category.keys())
category_dropdown = ttk.Combobox(frame, textvariable=category_var, values=categories, state='readonly', font=("Poppins", 12))
category_dropdown.pack(pady=10)

# Quote Label
quote_label = tk.Label(root, text="Click below to generate a quote!", wraplength=900, justify="center", font=("Segoe UI", 20), bg="#ffffff", fg="#333333")
quote_label.place(relx=0.5, rely=0.4, anchor="n")

# Buttons Frame
button_frame = tk.Frame(root, bg="#ffffff")
button_frame.place(relx=0.5, rely=0.7, anchor="n")

# Generate Button
generate_btn = tk.Button(button_frame, text="Generate Quote", command=generate_new_quote, font=("Poppins", 14), bg="#6c63ff", fg="white", width=18)
generate_btn.grid(row=0, column=0, padx=10)

# Copy Button
copy_btn = tk.Button(button_frame, text="Copy", command=copy_quote, font=("Poppins", 14), bg="#28a745", fg="white", width=12)
copy_btn.grid(row=0, column=1, padx=10)

# Speak Button
speak_btn = tk.Button(button_frame, text="Speak", command=speak_quote, font=("Poppins", 14), bg="#ff6b6b", fg="white", width=12)
speak_btn.grid(row=0, column=2, padx=10)

# Bind window resize
root.bind("<Configure>", resize_background)

# Start background changing
root.after(10000, change_background)

root.mainloop()
