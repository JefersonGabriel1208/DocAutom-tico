import customtkinter as ctk                    # Biblioteca para a interface visual moderna (Dark Mode)
from tkinter import filedialog, messagebox     # Ferramentas nativas para janelas de arquivos e avisos
from docxtpl import DocxTemplate               # O "motor" que manipula o arquivo Word (.docx)
from datetime import datetime                  # Para capturar a data do sistema automaticamente
import os                                      # Para verificar arquivos e caminhos no Linux/Windows

# --- CONFIGURAÇÃO VISUAL (DESIGN) ---
ctk.set_appearance_mode("dark")                # Define o tema escuro (estilo profissional)
ctk.set_default_color_theme("blue")            # Define a cor principal dos botões como azul

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Configurações da Janela Principal
        self.title("Gerador de Manuais Chiptronic - P&D")
        self.geometry("500x400")

        # --- TÍTULO DA INTERFACE ---
        self.label = ctk.CTkLabel(self, text="Dados do Manual", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        # --- CAMPOS DE ENTRADA (INPUTS) ---
        # Campo para o nome do chicote/cabo
        self.input_cabo = ctk.CTkEntry(self, placeholder_text="Nome do Chicote/Cabo", width=300)
        self.input_cabo.pack(pady=10)

        # Campo para o nome do engenheiro/técnico responsável
        self.input_resp = ctk.CTkEntry(self, placeholder_text="Responsável Técnico", width=300)
        self.input_resp.pack(pady=10)

        # --- BOTÃO DE AÇÃO ---
        self.btn_gerar = ctk.CTkButton(self, text="GERAR E SALVAR MANUAL", command=self.gerar_manual)
        self.btn_gerar.pack(pady=30)

    def gerar_manual(self):
        """Função principal que processa o Word e salva o novo arquivo"""
        try:
            # 1. SEGURANÇA: Verifica se o arquivo base 'modelo.docx' existe na pasta
            if not os.path.exists("modelo.docx"):
                messagebox.showerror("Erro", "Arquivo 'modelo.docx' não encontrado na pasta!")
                return

            # 2. INTERFACE: Abre a janela do sistema para o usuário escolher onde salvar
            caminho_destino = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=[("Documento Word", "*.docx")],
                initialfile=f"Manual_{self.input_cabo.get()}.docx"
            )

            # 3. PROCESSAMENTO: Se o usuário não cancelou a janela de salvar...
            if caminho_destino:
                doc = DocxTemplate("modelo.docx") # Carrega o template com as tags {{ }}
                
                # Cria o dicionário que vincula as Tags do Word aos dados da Janela
                dados = {
                    'nome_cabo': self.input_cabo.get(),
                    'responsavel': self.input_resp.get(),
                    'data': datetime.now().strftime("%d/%m/%Y") # Pega a data atual formatada
                }
                
                # Executa a substituição das tags pelo texto real
                doc.render(dados)
                # Salva o novo arquivo no local escolhido
                doc.save(caminho_destino)
                
                # Alerta de sucesso ao finalizar
                messagebox.showinfo("Sucesso", "Manual gerado e salvo com sucesso!")

        except Exception as e:
            # Caso ocorra qualquer erro técnico, ele mostra o motivo aqui
            messagebox.showerror("Erro Crítico", f"Erro ao gerar: {e}")

# --- INICIALIZAÇÃO DO PROGRAMA ---
if __name__ == "__main__":
    app = App()
    app.mainloop() # Mantém a janela aberta e rodando