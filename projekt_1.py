import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup

# Funkcja do pobierania opowiadania o SCP
def get_scp_story(scp_number_or_url):
    if scp_number_or_url.startswith("http"):
        url = scp_number_or_url
    else:
        url = f"http://scp-pl.wikidot.com/scp-{scp_number_or_url}"

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        story = soup.find('div', {'id': 'page-content'}).get_text()
        return story
    else:
        return "Nie udało się pobrać opowiadania."

# Funkcja do wyświetlania opowiadania w polu tekstowym
def display_story():
    scp_input = scp_entry.get()
    story = get_scp_story(scp_input)
    text_widget.delete('1.0', tk.END)  # Wyczyść tekst w polu tekstowym
    text_widget.insert(tk.END, story)

# Tworzenie głównego okna
root = tk.Tk()
root.title('Wikipedia SCP')
root.geometry('800x600')

# Ramka z polem do wprowadzania numeru SCP lub linku
input_frame = ttk.Frame(root)
input_frame.pack(pady=20)

label = ttk.Label(input_frame, text="Wybierz numer SCP lub wklej link:")
label.pack(side=tk.LEFT, padx=10)
scp_entry = ttk.Entry(input_frame, width=30)
scp_entry.pack(side=tk.LEFT)

display_button = ttk.Button(input_frame, text="Pokaż Opowiadanie", command=display_story)
display_button.pack(side=tk.LEFT, padx=10)

# Ramka na wyświetlanie opowiadania
text_frame = ttk.Frame(root)
text_frame.pack(fill=tk.BOTH, expand=True)

# Pole tekstowe
text_widget = tk.Text(text_frame)
text_widget.pack(fill=tk.BOTH, expand=True)

root.mainloop()
