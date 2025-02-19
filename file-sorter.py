import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import defaultdict

# Lista obsługiwanych rozszerzeń
roz = ["pdf", "docx", "txt", "jpg", "png", "mp4", "avi", "mp3", "wav"]

# Przechowywanie reguł użytkownika
reg = {}


def dodaj_regule():
    wybrane_rozszerzenia = [ext for ext, var in zmienne_rozszerzen.items() if var.get()]
    sciezka_folderu = filedialog.askdirectory(title="Wybierz folder docelowy")
    if sciezka_folderu and wybrane_rozszerzenia:
        for ext in wybrane_rozszerzenia:
            reg[ext] = sciezka_folderu
        aktualizuj_widok_regul()


def usun_regule(ext):
    if ext in reg:
        del reg[ext]
        aktualizuj_widok_regul()


def aktualizuj_widok_regul():
    for widget in ramka_regul.winfo_children():
        widget.destroy()

    for ext, sciezka in reg.items():
        kontener_reguly = tk.Frame(ramka_regul, bg="#242424", bd=0)
        kontener_reguly.pack(fill=tk.X, pady=5, padx=5)
        kontener_reguly.configure(relief=tk.FLAT)
        kontener_reguly.config(highlightbackground="#242424", highlightthickness=0)

        etykieta = tk.Label(kontener_reguly, text=f"{ext} → {sciezka}", font=("Arial", 10), bg="#242424", fg="white")
        etykieta.pack(side=tk.LEFT, padx=10, pady=5)
        etykieta.configure(relief=tk.FLAT, bd=0)

        przycisk_usun = tk.Button(kontener_reguly, text="❌", command=lambda e=ext: usun_regule(e), bg="#242424",
                                  fg="white", font=("Arial", 10, "bold"), padx=5)
        przycisk_usun.pack(side=tk.RIGHT, padx=10)
        przycisk_usun.configure(relief=tk.FLAT, bd=0)


def sortuj_pliki(katalog):
    if not os.path.exists(katalog):
        messagebox.showerror("Błąd", f"Katalog '{katalog}' nie istnieje.")
        return

    pliki_do_folderow = defaultdict(list)

    for plik in os.listdir(katalog):
        rozszerzenie = os.path.splitext(plik)[1].lstrip('.').lower()
        if not rozszerzenie:
            continue

        if rozszerzenie in reg:
            pliki_do_folderow[reg[rozszerzenie]].append(plik)
        else:
            folder_domyslny = os.path.join(katalog, rozszerzenie)
            pliki_do_folderow[folder_domyslny].append(plik)

    for sciezka_folderu, pliki in pliki_do_folderow.items():
        os.makedirs(sciezka_folderu, exist_ok=True)

        for plik in pliki:
            sciezka_zrodlowa = os.path.join(katalog, plik)
            sciezka_docelowa = os.path.join(sciezka_folderu, plik)
            shutil.move(sciezka_zrodlowa, sciezka_docelowa)

    messagebox.showinfo("Sukces", "Sortowanie zakończone.")


def wybierz_folder():
    global katalog_main
    katalog_main = filedialog.askdirectory(title="Wybierz folder do sortowania")
    etykieta_folderu.config(text=f"Wybrany folder: {katalog_main}")


def uruchom_sortowanie():
    if katalog_main:
        sortuj_pliki(katalog_main)
    else:
        messagebox.showerror("Błąd", "Najpierw wybierz folder do sortowania.")


root = tk.Tk()
root.title("Sortowanie Plików")
root.geometry("600x650")
root.configure(bg="#2E2E2E")
root.option_add('*Font', 'Arial 10')
root.tk_setPalette(background="#2E2E2E", foreground="white")

katalog_main = ""

# Stylowanie interefjsu
# Nagłówek
ramka_tytulu = tk.Frame(root, bg="#1C1C1C")
ramka_tytulu.pack(fill=tk.X)
tk.Label(ramka_tytulu, text="Sortowanie Plików", font=("Arial", 18, "bold"), bg="#1C1C1C", fg="white").pack(pady=10)

# Wybór katalogu
tk.Button(root, text="📂 Wybierz katalog", command=wybierz_folder, font=("Arial", 12, "bold"), bg="#424242", fg="white",
          padx=15, pady=5).pack(pady=5)
etykieta_folderu = tk.Label(root, text="Nie wybrano folderu", bg="#2E2E2E", fg="white", font=("Arial", 10))
etykieta_folderu.pack()

# Wybór reguł
tk.Label(root, text="Wybierz rozszerzenia do grupowania:", font=("Arial", 12, "bold"), bg="#2E2E2E", fg="white").pack(
    pady=5)

ramka_rozszerzen = tk.Frame(root, bg="#3B3B3B")
ramka_rozszerzen.pack(pady=5, padx=10, fill=tk.X)

zmienne_rozszerzen = {}
kolumny = 5
wiersz = 0
kolumna = 0
for ext in roz:
    var = tk.BooleanVar()
    chk = tk.Checkbutton(ramka_rozszerzen, text=ext, variable=var, bg="#3B3B3B", fg="white", font=("Arial", 10),
                         selectcolor="#2E2E2E")
    chk.grid(row=wiersz, column=kolumna, padx=5, pady=2, sticky='w')
    zmienne_rozszerzen[ext] = var
    kolumna += 1
    if kolumna >= kolumny:
        kolumna = 0
        wiersz += 1

# Dodanie reguły
tk.Button(root, text="➕ Dodaj regułę", command=dodaj_regule, font=("Arial", 12, "bold"), bg="#757575", fg="white",
          padx=15, pady=5).pack(pady=5)

# Lista reguł
ramka_regul = tk.Frame(root, bg="#3B3B3B")
ramka_regul.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Sortowanie
tk.Button(root, text="🚀 Rozpocznij sortowanie", command=uruchom_sortowanie, font=("Arial", 12, "bold"), bg="#D32F2F",
          fg="white", padx=15, pady=5).pack(pady=15)

root.mainloop()
