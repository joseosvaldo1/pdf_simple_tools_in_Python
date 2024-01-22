import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfFileReader, PdfReader, PdfWriter

class PDFSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dividir PDFs")

        # Variáveis
        self.pdf_file = None

        # Widgets
        self.label_file = tk.Label(root, text="Nenhum arquivo selecionado")
        self.label_file.grid(row=0, column=0, padx=10, pady=10)

        self.btn_select = tk.Button(root, text="Selecionar PDF", command=self.selecionar_pdf)
        self.btn_select.grid(row=1, column=0, padx=10, pady=5)

        self.label_option = tk.Label(root, text="Opção de divisão:")
        self.label_option.grid(row=2, column=0, padx=10, pady=5)

        self.options = ["Cada página", "Páginas pares", "Páginas ímpares", "Após página específica", "A cada 'n' páginas"]
        self.option_var = tk.StringVar(root)
        self.option_var.set(self.options[0])
        self.option_menu = tk.OptionMenu(root, self.option_var, *self.options)
        self.option_menu.grid(row=3, column=0, padx=10, pady=5)

        self.label_page = tk.Label(root, text="Número da página / 'n':")
        self.label_page.grid(row=4, column=0, padx=10, pady=5)

        self.entry_page = tk.Entry(root, width=10)
        self.entry_page.grid(row=5, column=0, padx=10, pady=5)

        self.btn_split = tk.Button(root, text="Dividir PDF", command=self.dividir_pdf)
        self.btn_split.grid(row=6, column=0, padx=10, pady=10)

    def selecionar_pdf(self):
        self.pdf_file = filedialog.askopenfilename(title="Selecionar PDF para dividir", filetypes=[("PDF files", "*.pdf")])
        if self.pdf_file:
            self.label_file.config(text=os.path.basename(self.pdf_file))

    def dividir_pdf(self):
        if not self.pdf_file:
            messagebox.showerror("Erro", "Nenhum arquivo PDF selecionado.")
            return

        option = self.option_var.get()
        page_num = self.entry_page.get().strip()

        if option in ["Após página específica", "A cada 'n' páginas"] and not page_num.isdigit():
            messagebox.showerror("Erro", "Número de página inválido.")
            return

        output_dir = filedialog.askdirectory(title="Selecionar diretório para salvar PDFs divididos")
        if not output_dir:
            return

        reader = PdfReader(self.pdf_file)
        total_pages = len(reader.pages)

        if option == "Cada página":
            self.split_every_page(reader, total_pages, output_dir)
        elif option == "Páginas pares":
            self.split_even_pages(reader, total_pages, output_dir)
        elif option == "Páginas ímpares":
            self.split_odd_pages(reader, total_pages, output_dir)
        elif option == "Após página específica":
            self.split_after_page(reader, total_pages, int(page_num), output_dir)
        elif option == "A cada 'n' páginas":
            self.split_every_n_pages(reader, total_pages, int(page_num), output_dir)

        messagebox.showinfo("Sucesso", "PDF dividido com sucesso.")

    def split_every_page(self, reader, total_pages, output_dir):
        for i in range(total_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])
            with open(f"{output_dir}/page_{i+1}.pdf", "wb") as output_pdf:
                writer.write(output_pdf)

    def split_even_pages(self, reader, total_pages, output_dir):
        for i in range(1, total_pages, 2):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])
            with open(f"{output_dir}/page_{i+1}.pdf", "wb") as output_pdf:
                writer.write(output_pdf)

    def split_odd_pages(self, reader, total_pages, output_dir):
        for i in range(0, total_pages, 2):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])
            with open(f"{output_dir}/page_{i+1}.pdf", "wb") as output_pdf:
                writer.write(output_pdf)

    def split_after_page(self, reader, total_pages, page_num, output_dir):
        if page_num > total_pages:
            messagebox.showerror("Erro", "Número de página maior que o total de páginas.")
            return

        writer = PdfWriter()
        for i in range(page_num):
            writer.add_page(reader.pages[i])
        with open(f"{output_dir}/pages_1_to_{page_num}.pdf", "wb") as output_pdf:
            writer.write(output_pdf)

        writer = PdfWriter()
        for i in range(page_num, total_pages):
            writer.add_page(reader.pages[i])
        with open(f"{output_dir}/pages_{page_num+1}_to_{total_pages}.pdf", "wb") as output_pdf:
            writer.write(output_pdf)

    def split_every_n_pages(self, reader, total_pages, n, output_dir):
        for i in range(0, total_pages, n):
            writer = PdfWriter()
            for j in range(i, min(i + n, total_pages)):
                writer.add_page(reader.pages[j])
            with open(f"{output_dir}/pages_{i+1}_to_{min(i+n, total_pages)}.pdf", "wb") as output_pdf:
                writer.write(output_pdf)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFSplitterApp(root)
    root.mainloop()
