# -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfMerger

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unir PDFs")

        # Variáveis
        self.pdf_files = []
        self.merger = PdfMerger()

        # Widgets
        self.listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=10, width=50)
        self.listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.btn_add = tk.Button(root, text="Adicionar PDF", command=self.adicionar_pdf)
        self.btn_add.grid(row=1, column=0, padx=10, pady=5)

        self.btn_remove = tk.Button(root, text="Remover Selecionado", command=self.remover_pdf_selecionado)
        self.btn_remove.grid(row=1, column=1, padx=10, pady=5)

        self.btn_mover_up = tk.Button(root, text="Mover para Cima", command=self.mover_pdf_para_cima)
        self.btn_mover_up.grid(row=2, column=0, padx=10, pady=5)

        self.btn_mover_down = tk.Button(root, text="Mover para Baixo", command=self.mover_pdf_para_baixo)
        self.btn_mover_down.grid(row=2, column=1, padx=10, pady=5)
        
        self.btn_unir = tk.Button(root, text="Unir PDFs", command=self.unir_pdfs)
        self.btn_unir.grid(row=3, column=0, columnspan=2, pady=10)

    def adicionar_pdf(self):
        pdf_file_paths = filedialog.askopenfilenames(title="Selecionar PDFs para unir", filetypes=[("PDF files", "*.pdf")])
        for pdf_file in pdf_file_paths:
            self.pdf_files.append(pdf_file)
            self.listbox.insert(tk.END, os.path.basename(pdf_file))

    def remover_pdf_selecionado(self):
        selected_indices = self.listbox.curselection()
        for index in reversed(selected_indices):
            del self.pdf_files[index]
            self.listbox.delete(index)

    def mover_pdf_para_cima(self):
        selected_index = self.listbox.curselection()
        if selected_index and selected_index[0] > 0:
            self.pdf_files[selected_index[0]], self.pdf_files[selected_index[0] - 1] = (
                self.pdf_files[selected_index[0] - 1],
                self.pdf_files[selected_index[0]],
            )
            self.atualizar_listbox()
            self.listbox.selection_set(selected_index[0] - 1)

    def mover_pdf_para_baixo(self):
        selected_index = self.listbox.curselection()
        if selected_index and selected_index[0] < len(self.pdf_files) - 1:
            self.pdf_files[selected_index[0]], self.pdf_files[selected_index[0] + 1] = (
                self.pdf_files[selected_index[0] + 1],
                self.pdf_files[selected_index[0]],
            )
            self.atualizar_listbox()
            self.listbox.selection_set(selected_index[0] + 1)

    def atualizar_listbox(self):
        self.listbox.delete(0, tk.END)
        for pdf_file in self.pdf_files:
            self.listbox.insert(tk.END, os.path.basename(pdf_file))

    def unir_pdfs(self):
        self.merger = PdfMerger()  # Reinicializar o PdfMerger

        caminho_destino = filedialog.asksaveasfilename(
            title="Salvar arquivo unido como",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
        )

        if caminho_destino:
            for pdf_file in self.pdf_files:
                self.merger.append(pdf_file)

            with open(caminho_destino, "wb") as output_pdf:
                self.merger.write(output_pdf)
            self.merger.close()
            self.limpar_tela()

    def limpar_tela(self):
        self.pdf_files = []
        self.listbox.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
