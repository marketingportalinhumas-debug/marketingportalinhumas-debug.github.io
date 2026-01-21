document.addEventListener('DOMContentLoaded', (event) => {
    fetch('precos.json')
        .then(response => {
            // Garante que a resposta foi OK (código 200)
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json(); // Converte a resposta em um objeto JSON
        })
        .then(data => {
            // Atualiza o texto nos elementos HTML usando seus IDs
            document.getElementById('price-lombo').textContent = `${data['Lombo']}`;
            document.getElementById('price-bisteca').textContent = `${data['Bisteca Lombo']}`;
            
            console.log("Preços atualizados com sucesso!");
        })
        .catch(error => {
            // Lida com erros se o arquivo não for encontrado
            console.error('Houve um problema com a operação de fetch:', error);
            document.getElementById('price-lombo').textContent = "Erro ao carregar";
            document.getElementById('price-bisteca').textContent = "Erro ao carregar";
        });
});

// Recarrega a página automaticamente a cada 5 minutos para garantir que as atualizações apareçam
setTimeout(function(){
   window.location.reload(true);
}, 300000); // 300000 milissegundos = 5 minutos
