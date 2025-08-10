# main_gui.py

import tkinter as tk
from tkinter import filedialog, messagebox
from converters.text_to_pdf import txt_to_pdf
from converters.image_to_text import image_to_text
import os

class SmartFileConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart File Converter")
        self.geometry("500x300")

        # Mode choix
        self.mode_var = tk.StringVar(value="txt2pdf")
        tk.Label(self, text="Choisissez le mode de conversion :").pack(pady=10)

        tk.Radiobutton(self, text="Texte → PDF", variable=self.mode_var, value="txt2pdf").pack()
        tk.Radiobutton(self, text="Image → Texte", variable=self.mode_var, value="img2txt").pack()

        # Input file
        tk.Button(self, text="Sélectionner fichier source", command=self.select_input_file).pack(pady=10)
        self.input_label = tk.Label(self, text="Aucun fichier sélectionné")
        self.input_label.pack()

        # Output file (uniquement txt2pdf)
        self.output_frame = tk.Frame(self)
        self.output_frame.pack(pady=10)

        self.output_label = tk.Label(self.output_frame, text="Fichier PDF de sortie :")
        self.output_entry = tk.Entry(self.output_frame, width=40)
        self.output_button = tk.Button(self.output_frame, text="Parcourir", command=self.select_output_file)

        self.output_label.grid(row=0, column=0)
        self.output_entry.grid(row=0, column=1)
        self.output_button.grid(row=0, column=2)

        # Bouton Convertir
        tk.Button(self, text="Convertir", command=self.convert).pack(pady=10)

        # Zone résultat texte (pour img2txt)
        self.result_text = tk.Text(self, height=6)
        self.result_text.pack(pady=10, fill=tk.BOTH, expand=True)
        self.result_text.config(state=tk.DISABLED)

        # Variables fichiers
        self.input_file = None
        self.output_file = None

        # Actualiser affichage selon mode
        self.mode_var.trace("w", self.on_mode_change)
        self.on_mode_change()

    def on_mode_change(self, *args):
        mode = self.mode_var.get()
        if mode == "txt2pdf":
            self.output_frame.pack(pady=10)
            self.result_text.config(state=tk.DISABLED)
        else:
            self.output_frame.pack_forget()
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete("1.0", tk.END)
            self.result_text.config(state=tk.DISABLED)

    def select_input_file(self):
        mode = self.mode_var.get()
        if mode == "txt2pdf":
            filetypes = [("Fichiers texte", "*.txt")]
        else:
            filetypes = [("Images", "*.png *.jpg *.jpeg *.bmp")]

        filename = filedialog.askopenfilename(title="Sélectionner fichier source", filetypes=filetypes)
        if filename:
            self.input_file = filename
            self.input_label.config(text=os.path.basename(filename))

            # Suggérer un nom de sortie par défaut si mode txt2pdf
            if self.mode_var.get() == "txt2pdf":
                default_output = os.path.splitext(filename)[0] + ".pdf"
                self.output_entry.delete(0, tk.END)
                self.output_entry.insert(0, default_output)

    def select_output_file(self):
        filename = filedialog.asksaveasfilename(title="Fichier PDF de sortie", defaultextension=".pdf",
                                                filetypes=[("Fichiers PDF", "*.pdf")])
        if filename:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, filename)
            self.output_file = filename

    def convert(self):
        if not self.input_file:
            messagebox.showwarning("Erreur", "Veuillez sélectionner un fichier source.")
            return

        mode = self.mode_var.get()
        if mode == "txt2pdf":
            output = self.output_entry.get()
            if not output:
                messagebox.showwarning("Erreur", "Veuillez spécifier un fichier PDF de sortie.")
                return
            try:
                txt_to_pdf(self.input_file, output)
                messagebox.showinfo("Succès", f"Conversion réussie : {self.input_file} → {output}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la conversion:\n{e}")

        else:  # img2txt
            try:
                text = image_to_text(self.input_file)
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert(tk.END, text)
                self.result_text.config(state=tk.DISABLED)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la reconnaissance de texte:\n{e}")


if __name__ == "__main__":
    app = SmartFileConverterApp()
    app.mainloop()
