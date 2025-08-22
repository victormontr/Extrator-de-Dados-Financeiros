import tkinter as tk
from tkinter import ttk, messagebox
from typing import Tuple, List, Dict

import os
import sys
import subprocess
import threading
import platform
from datetime import datetime, timedelta  # Importa timedelta para manipulação de datas

import pandas as pd
import yfinance as yf  # Biblioteca para obter dados financeiros
import requests.exceptions # Adiciona a importação para tratar erros de conexão
from tkcalendar import DateEntry  # Widget de calendário para seleção de datas

# --- Configurações de Ambiente ---
# Ajusta a conscientização de DPI no Windows
if platform.system() == "Windows":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except (AttributeError, OSError):
        pass

# Redireciona a saída padrão se o script estiver congelado (ex. PyInstaller)
if getattr(sys, 'frozen', False):
    sys.stdout = sys.stdout or open(os.devnull, 'w')
    sys.stderr = sys.stderr or open(os.devnull, 'w')

# Define o caminho para a pasta de documentos e a pasta de saída
DOCUMENTS_PATH = os.path.join(os.path.expanduser("~"), "Documents")
OUTPUT_FOLDER_NAME = "Dados financeiros Extraídos"
PASTA_SAIDA = os.path.join(DOCUMENTS_PATH, OUTPUT_FOLDER_NAME)

# Cria a pasta de saída se não existir
os.makedirs(PASTA_SAIDA, exist_ok=True)

# Define estilos de fonte para a interface
FONTE_LABEL = ("Segoe UI", 9)
FONTE_ENTRY = ("Segoe UI", 9)
FONTE_BOTAO = ("Segoe UI", 10, "bold")
FONTE_RODAPE = ("Segoe UI", 8, "italic")

def carregar_tickers() -> Tuple[List[str], Dict[str, str]]:
    # Carrega os tickers de ações a partir de um arquivo CSV
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    try:
        # Define possíveis caminhos para o arquivo CSV
        csv_path_options = [
            os.path.join(base_path, "Mapa", "Mapa Tickers B3.csv"),
            os.path.join(base_path, "Mapa Tickers B3.csv"),
            os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), "Mapa", "Mapa Tickers B3.csv")
        ]
        df = None
        # Tenta carregar o DataFrame a partir de um dos caminhos
        for path_option in csv_path_options:
            if os.path.exists(path_option):
                df = pd.read_csv(path_option, sep=";")
                break

        # Exibe erro se o arquivo não for encontrado
        if df is None:
            messagebox.showerror("Erro Crítico", "Arquivo 'Mapa Tickers B3.csv' não encontrado.")
            sys.exit(1)

        # Cria uma lista e um dicionário de tickers
        lista = [f"{row['Ação']} - {row['Código']}.SA" for _, row in df.iterrows()]
        mapa = {f"{row['Ação']} - {row['Código']}.SA": f"{row['Código']}.SA" for _, row in df.iterrows()}
        return lista, mapa
    except Exception as e:
        # Exibe erro em caso de falha ao carregar os tickers
        messagebox.showerror("Erro ao Carregar Tickers", f"Não foi possível carregar o arquivo de tickers: {e}")
        sys.exit(1)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Carrega os tickers ao inicializar a aplicação
        self.lista_tickers, self.mapa_tickers = carregar_tickers()

        # Configurações da janela principal
        self.title("Extrator de Dados Financeiros")
        self.geometry("500x230")
        self.resizable(False, False)
        self.configure(bg='white')

        # Configura o estilo da interface
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.configurar_estilos()

        # Cria os widgets da interface
        self.criar_widgets()

    def configurar_estilos(self):
        # Define estilos para os componentes da interface
        self.style.configure('TFrame', background='white')
        self.style.configure('TLabel', background='white', foreground='black')
        self.style.configure("Icon.TButton", font=FONTE_BOTAO, padding=(8, 4), background='#E0E0E0', foreground='black', borderwidth=1, relief='flat')
        self.style.map("Icon.TButton", background=[('active', '!disabled', '#C8C8C8'), ('pressed', '!disabled', '#C8C8C8')])
        self.style.map("TCombobox", fieldbackground=[('disabled', '#F0F0F0')], foreground=[('disabled', '#A9A9A9')])

    def criar_widgets(self):
        # Cria a estrutura de widgets da interface
        content_frame = ttk.Frame(self, padding="5 5 5 5", style='TFrame')
        content_frame.pack(expand=True, fill=tk.BOTH)
        form_frame = ttk.Frame(content_frame, style='TFrame')
        form_frame.pack(pady=3, padx=3, fill=tk.X)
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        # Cria o campo para seleção de empresa (ticker)
        ttk.Label(form_frame, text="Empresa:", font=FONTE_LABEL, style='TLabel').grid(row=0, column=0, sticky="e", padx=(0, 3), pady=5)
        self.combo_ticker = ttk.Combobox(form_frame, values=self.lista_tickers, font=FONTE_ENTRY)
        self.combo_ticker.grid(row=0, column=1, columnspan=3, sticky="ew", pady=5)
        self.combo_ticker.bind("<KeyRelease>", self.autocompletar)  # Habilita autocompletar
        if self.lista_tickers:
            self.combo_ticker.current(0)  # Seleciona o primeiro ticker por padrão

        # Cria campos para seleção de datas
        ttk.Label(form_frame, text="Data de Início:", font=FONTE_LABEL, style='TLabel').grid(row=1, column=0, sticky="e", padx=(0, 3), pady=5)
        ttk.Label(form_frame, text="Fim:", font=FONTE_LABEL, style='TLabel').grid(row=1, column=2, sticky="e", padx=(8, 3), pady=5)

        # Cria o campo de data de fim
        self.entry_fim = DateEntry(
            form_frame,
            font=FONTE_ENTRY,
            width=10,
            date_pattern='dd-mm-yyyy',
            locale='pt_BR',
            showweeknumbers=False,
            firstweekday='monday'
        )
        self.entry_fim.grid(row=1, column=3, sticky="ew", pady=5)

        # Define datas padrão para os campos de data
        fim_default = self.entry_fim.get_date()
        inicio_default = fim_default - timedelta(days=1)

        # Cria o campo de data de início
        self.entry_inicio = DateEntry(
            form_frame,
            font=FONTE_ENTRY,
            width=10,
            date_pattern='dd-mm-yyyy',
            locale='pt_BR',
            showweeknumbers=False,
            firstweekday='monday'
        )
        self.entry_inicio.grid(row=1, column=1, sticky="ew", pady=5)
        self.entry_inicio.set_date(inicio_default)

        # Atualiza a data de início quando a data de fim é alterada
        self.entry_fim.bind("<<DateEntrySelected>>", self._atualizar_inicio_por_fim)

        # Cria o campo para seleção de intervalo
        ttk.Label(form_frame, text="Intervalo:", font=FONTE_LABEL, style='TLabel').grid(row=2, column=0, sticky="e", padx=(0, 3), pady=5)
        self.var_intervalo = tk.StringVar(self)
        self.var_intervalo.set("1wk")  # Define valor padrão
        self.combo_intervalo = ttk.Combobox(form_frame, textvariable=self.var_intervalo, values=["1d", "5d", "1wk", "1mo", "3mo"], font=FONTE_ENTRY, state="readonly", width=9)
        self.combo_intervalo.grid(row=2, column=1, sticky="ew", pady=5)

        # Cria o campo para seleção de formato de saída
        ttk.Label(form_frame, text="Formato:", font=FONTE_LABEL, style='TLabel').grid(row=2, column=2, sticky="e", padx=(8, 3), pady=5)
        self.var_formato = tk.StringVar(self)
        self.var_formato.set("CSV")  # Define valor padrão
        self.combo_formato = ttk.Combobox(form_frame, textvariable=self.var_formato, values=["CSV", "XLSX"], font=FONTE_ENTRY, state="readonly", width=9)
        self.combo_formato.grid(row=2, column=3, sticky="ew", pady=5)

        # Cria a área de botões
        button_area_frame = ttk.Frame(content_frame, style='TFrame')
        button_area_frame.pack(pady=(10, 6))
        self.botao_buscar = ttk.Button(button_area_frame, text="🔍 Buscar", command=self.iniciar_busca_thread, style="Icon.TButton")
        self.botao_buscar.pack(side=tk.LEFT, padx=4)
        self.botao_abrir = ttk.Button(button_area_frame, text="📂 Abrir", command=self.abrir_pasta, style="Icon.TButton")
        self.botao_abrir.pack(side=tk.LEFT, padx=4)

        # Cria rodapé com informações do autor
        ttk.Label(content_frame, text="Powered by Victor Monteiro", font=FONTE_RODAPE, foreground="gray", style='TLabel').pack(pady=(6, 2))
        self.status_label = ttk.Label(content_frame, text="Pronto para buscar...", font=FONTE_RODAPE, foreground="#5A5A5A", style='TLabel')
        self.status_label.pack(pady=(0, 2))

    def _atualizar_inicio_por_fim(self, event=None):
        # Atualiza a data de início com base na data de fim selecionada
        try:
            fim = self.entry_fim.get_date()
            novo_inicio = fim - timedelta(days=1)
            self.entry_inicio.set_date(novo_inicio)
        except Exception:
            pass  # Ignora exceções

    def autocompletar(self, event: tk.Event):
        # Implementa a funcionalidade de autocompletar para o campo de ticker
        texto_digitado = self.combo_ticker.get().lower()
        sugestoes = [item for item in self.lista_tickers if texto_digitado in item.lower()]
        self.combo_ticker['values'] = sugestoes if sugestoes else self.lista_tickers

    def buscar(self):
        # Realiza a busca de dados financeiros com base nas entradas do usuário
        empresa = self.combo_ticker.get().strip()
        if empresa not in self.mapa_tickers:
            messagebox.showerror("Erro", "Selecione um ticker válido.")
            return

        ticker = self.mapa_tickers[empresa]
        inicio_date_obj = self.entry_inicio.get_date()
        fim_date_obj = self.entry_fim.get_date()

        # Verifica se as datas foram preenchidas
        if not inicio_date_obj or not fim_date_obj:
            messagebox.showwarning("Campos obrigatórios", "Preencha as datas.")
            return

        # Converte as datas para o formato datetime
        inicio_dt = datetime.combine(inicio_date_obj, datetime.min.time())
        fim_dt = datetime.combine(fim_date_obj, datetime.min.time())
        intervalo, formato = self.var_intervalo.get(), self.var_formato.get()

        try:
            # Valida as datas
            if inicio_dt > fim_dt:
                messagebox.showerror("Erro de Data", "A data inicial não pode ser maior que a final.")
                return
            if max(inicio_dt, fim_dt) > datetime.today():
                messagebox.showerror("Erro de Data", "As datas não podem estar no futuro.")
                return

            # Obtém os dados financeiros usando a biblioteca yfinance
            df = yf.download(ticker, start=inicio_dt, end=fim_dt, interval=intervalo)

            # Verifica se os dados retornados estão vazios
            if df.empty:
                messagebox.showwarning("Aviso", "Nenhum dado encontrado para o período e ticker especificados.")
                return
            
            df.reset_index(inplace=True)  # Reseta o índice do DataFrame
            colunas_desejadas = ["Date", "Open", "High", "Low", "Close", "Volume"]
            colunas_existentes = [col for col in colunas_desejadas if col in df.columns]
            df = df[colunas_existentes]  # Filtra as colunas desejadas

            # Define o formato do arquivo de saída
            extensao = "xlsx" if formato == "XLSX" else "csv"
            nome_arquivo = f"{ticker}_{inicio_date_obj.strftime('%Y-%m-%d')}_{fim_date_obj.strftime('%Y-%m-%d')}_{intervalo}.{extensao}"
            caminho = os.path.join(PASTA_SAIDA, nome_arquivo)

            # Salva os dados no formato escolhido
            if formato == "XLSX":
                df.to_excel(caminho, index=False)
            else:
                df.to_csv(caminho, index=False, sep=';', decimal=',')

            messagebox.showinfo("Sucesso", f"Dados salvos em:\n{caminho}")
            self.status_label.config(text="Dados salvos com sucesso.")

        # Novo bloco de exceção para erros de conexão
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar. Verifique sua conexão com a internet.")
            self.status_label.config(text="Erro de conexão.")
            
        except Exception as e:
            # Exibe erro em caso de falha na busca (erros genéricos)
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")
            self.status_label.config(text="Erro durante a busca.")

    def iniciar_busca_thread(self):
        # Inicia a busca em uma thread separada para não bloquear a interface
        self.botao_buscar.config(state=tk.DISABLED)
        self.status_label.config(text="Buscando dados...")
        
        thread = threading.Thread(target=self.buscar_e_reabilitar_botao)
        thread.daemon = True
        thread.start()

    def buscar_e_reabilitar_botao(self):
        # Executa a busca e reabilita o botão após a conclusão
        try:
            self.buscar()
        finally:
            self.after(0, lambda: self.botao_buscar.config(state=tk.NORMAL))
            if self.status_label['text'] == "Buscando dados...":
                self.after(0, lambda: self.status_label.config(text="Pronto para buscar..."))

    def abrir_pasta(self):
        # Abre a pasta onde os dados foram salvos
        try:
            if sys.platform == "win32":
                os.startfile(PASTA_SAIDA)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", PASTA_SAIDA])
            else:
                subprocess.Popen(["xdg-open", PASTA_SAIDA])
        except Exception as e:
            # Exibe erro se não for possível abrir a pasta
            messagebox.showerror("Erro ao Abrir Pasta", f"Não foi possível abrir a pasta: {e}")

# Executa a aplicação
if __name__ == "__main__":
    app = App()
    app.mainloop()