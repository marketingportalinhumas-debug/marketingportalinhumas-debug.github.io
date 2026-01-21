import requests
import base64
import json
import tkinter as tk
from tkinter import messagebox

# --- Configurações (Substitua pelos seus dados reais) ---
GITHUB_TOKEN = "SEU_TOKEN_DE_ACESSO_PESSOAL"
REPO_OWNER = "seu_usuario_ou_organizacao"
REPO_NAME = "nome_do_seu_repositorio"
FILE_PATH = "caminho/do/seu/arquivo.json" # Ex: precos.json
COMMIT_MESSAGE = "Atualização automática de preços via GUI"
# -----------------------------------------------------

def update_github_file(owner, repo, file_path, new_content, token, commit_message):
    """Lógica para atualizar o arquivo no GitHub."""
    api_url = f"https://api.github.com{owner}/{repo}/contents/{file_path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28" 
    }

    # 1. Obter o SHA do arquivo atual
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        current_file_data = response.json()
        current_sha = current_file_data['sha']
    except requests.exceptions.RequestException as e:
        return False, f"Erro ao obter o arquivo atual: {e}"

    # 2. Codificar o novo conteúdo em Base64
    encoded_content = base64.b64encode(new_content.encode('utf-8')).decode('utf-8')

    # 3. Preparar e enviar a requisição PUT
    payload = {
        "message": commit_message,
        "content": encoded_content,
        "sha": current_sha 
    }

    try:
        update_response = requests.put(api_url, headers=headers, data=json.dumps(payload))
        update_response.raise_for_status()
        return True, f"Arquivo '{file_path}' atualizado com sucesso!"
    except requests.exceptions.RequestException as e:
        return False, f"Erro ao atualizar o arquivo: {e}"

def on_update_button_click():
    """Função chamada quando o botão 'Atualizar Preços' é clicado."""
    # Coleta os preços dos campos de entrada (exemplo para 2 itens)
    price_lombo = entry_lombo.get()
    price_bisteca = entry_bisteca.get()
    
    # Formata o novo conteúdo (ajuste o formato para o que seu site espera, ex: JSON)
    novo_conteudo = json.dumps({
        "Lombo": price_lombo,
        "Bisteca Lombo": price_bisteca,
        # Adicione outros campos de entrada e mapeie-os aqui
    }, indent=4)

    success, message = update_github_file(
        REPO_OWNER, REPO_NAME, FILE_PATH, novo_conteudo, GITHUB_TOKEN, COMMIT_MESSAGE
    )

    if success:
        messagebox.showinfo("Sucesso", message)
    else:
        messagebox.showerror("Erro", message)

# --- Configuração da Interface Gráfica ---
root = tk.Tk()
root.title("Atualizador de Preços do Açougue Portal")
root.geometry("350x200") # Define o tamanho da janela

tk.Label(root, text="Novo Preço do Lombo (kg):").pack(pady=5)
entry_lombo = tk.Entry(root)
entry_lombo.pack(pady=5)

tk.Label(root, text="Novo Preço da Bisteca Lombo (kg):").pack(pady=5)
entry_bisteca = tk.Entry(root)
entry_bisteca.pack(pady=5)

update_button = tk.Button(root, text="Atualizar Preços no GitHub", command=on_update_button_click)
update_button.pack(pady=20)

if __name__ == "__main__":
    # Verificação simples se as configurações padrão foram alteradas
    if GITHUB_TOKEN == "SEU_TOKEN_DE_ACESSO_PESSOAL":
        messagebox.showerror("Configuração Necessária", "Por favor, edite o arquivo Python e insira seu GITHUB_TOKEN, REPO_OWNER, etc.")
    else:
        root.mainloop() # Inicia o loop principal da interface gráfica
