import requests
import base64
import json
import tkinter as tk
from tkinter import messagebox

# --- Configurações (Substitua pelos seus dados reais) ---
GITHUB_TOKEN = ""
REPO_OWNER = "marketingportalinhumas"
REPO_NAME = "marketingportalinhumas-debug.github.io"
FILE_PATH = "precos.json"  # Caminho do arquivo no repositório
COMMIT_MESSAGE = "Atualização automática de preços via GUI"
# -----------------------------------------------------

def update_github_file(owner, repo, file_path, new_content, token, commit_message):
    """Lógica para atualizar o arquivo no GitHub."""
    # 🔴 CORRIGIDO: URL SEM ESPAÇOS!
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # 1. Obter o SHA do arquivo atual
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
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
        update_response = requests.put(api_url, headers=headers, data=json.dumps(payload), timeout=10)
        update_response.raise_for_status()
        return True, f"Arquivo '{file_path}' atualizado com sucesso!"
    except requests.exceptions.RequestException as e:
        return False, f"Erro ao atualizar o arquivo: {e}"

def on_update_button_click():
    """Função chamada quando o botão 'Atualizar Preços' é clicado."""
    price_lombo = entry_lombo.get().strip()
    price_bisteca = entry_bisteca.get().strip()

    if not price_lombo or not price_bisteca:
        messagebox.showwarning("Atenção", "Preencha todos os campos!")
        return

    # Formata o novo conteúdo em JSON
    novo_conteudo = json.dumps({
        "Lombo": price_lombo,
        "Bisteca Lombo": price_bisteca,
    }, indent=4, ensure_ascii=False)

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
root.geometry("350x200")

tk.Label(root, text="Novo Preço do Lombo (kg):").pack(pady=5)
entry_lombo = tk.Entry(root)
entry_lombo.pack(pady=5)

tk.Label(root, text="Novo Preço da Bisteca Lombo (kg):").pack(pady=5)
entry_bisteca = tk.Entry(root)
entry_bisteca.pack(pady=5)

update_button = tk.Button(root, text="Atualizar Preços no GitHub", command=on_update_button_click)
update_button.pack(pady=20)

if __name__ == "__main__":
    # Verificação se o token foi alterado
    if GITHUB_TOKEN == "SE É O MESMO TOKEN":
        messagebox.showerror("Configuração Necessária", 
            "Por favor, edite o arquivo Python e substitua o GITHUB_TOKEN pelo seu token real.")
    else:
        root.mainloop()
