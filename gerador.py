import customtkinter as ctk
from tkinter import filedialog, messagebox
from docxtpl import DocxTemplate
from datetime import datetime
import os

# Configuração visual da janela (Estilo Moderno)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerador de Manuais Chiptronic - P&D")
        self.geometry("500x400")

        # --- Campos da Interface ---
        self.label = ctk.CTkLabel(self, text="Dados do Manual", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        self.input_cabo = ctk.CTkEntry(self, placeholder_text="Nome do Chicote/Cabo", width=300)
        self.input_cabo.pack(pady=10)

        self.input_resp = ctk.CTkEntry(self, placeholder_text="Responsável Técnico", width=300)
        self.input_resp.pack(pady=10)

        # --- Botão de Gerar ---
        self.btn_gerar = ctk.CTkButton(self, text="GERAR E SALVAR MANUAL", command=self.gerar_manual)
        self.btn_gerar.pack(pady=30)

    def gerar_manual(self):
        try:
            # 1. Verifica se o modelo existe na pasta
            if not os.path.exists("modelo.docx"):
                messagebox.showerror("Erro", "Arquivo 'modelo.docx' não encontrado na pasta!")
                return

            # 2. Abre a caixa "Salvar Como"
            caminho_destino = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=[("Documento Word", "*.docx")],
                initialfile=f"Manual_{self.input_cabo.get()}.docx"
            )

            if caminho_destino:
                # 3. Processa o Word
                doc = DocxTemplate("modelo.docx")
                dados = {
                    'nome_cabo': self.input_cabo.get(),
                    'responsavel': self.input_resp.get(),
                    'data': datetime.now().strftime("%d/%m/%Y")
                }
                doc.render(dados)
                doc.save(caminho_destino)
                
                messagebox.showinfo("Sucesso", "Manual gerado e salvo com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Erro ao gerar: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()