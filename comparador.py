import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

class CSVComparator:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Comparator")
        self.file1_path = ""
        self.file2_path = ""

        # Interface
        tk.Button(root, text="Anexar Carteira de Clientes", command=self.load_file1).pack(pady=5)
        tk.Button(root, text="Anexar Lista de Atividades", command=self.load_file2).pack(pady=5)
        tk.Button(root, text="Analisar", command=self.compare_files).pack(pady=10)

    def load_file1(self):
        self.file1_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.file1_path:
            messagebox.showinfo("Carteira de Clientes", f"Arquivo anexado: {self.file1_path}")

    def load_file2(self):
        self.file2_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.file2_path:
            messagebox.showinfo("Lista de Atividades", f"Arquivo anexado: {self.file2_path}")

    def compare_files(self):
        if not self.file1_path or not self.file2_path:
            messagebox.showwarning("Erro", "Anexe ambos os arquivos antes de analisar.")
            return
        
        try:
            # Ler os arquivos e padronizar nomes das colunas
            clientes_df = pd.read_csv(self.file1_path)
            atividades_df = pd.read_csv(self.file2_path)

            # Remover espaços em branco e padronizar nomes das colunas para minúsculas
            clientes_df.columns = clientes_df.columns.str.strip().str.lower()
            atividades_df.columns = atividades_df.columns.str.strip().str.lower()

            # Verificar se os arquivos têm as colunas corretas
            if 'id' not in clientes_df.columns or 'responsavel' not in clientes_df.columns:
                messagebox.showerror("Erro", "A planilha de clientes precisa ter colunas 'ID' e 'Responsavel'.")
                return
            if 'id' not in atividades_df.columns:
                messagebox.showerror("Erro", "A planilha de atividades precisa ter a coluna 'ID'.")
                return

            # Encontrar clientes sem atividades
            clientes_sem_atividades = clientes_df[~clientes_df['id'].isin(atividades_df['id'])]

            # Salvar o resultado
            clientes_sem_atividades.to_csv("clientes_sem_atividades.csv", index=False)
            messagebox.showinfo("Análise Completa", "Arquivo 'clientes_sem_atividades.csv' gerado com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro durante a análise: {e}")

# Iniciar o programa
root = tk.Tk()
app = CSVComparator(root)
root.mainloop()
