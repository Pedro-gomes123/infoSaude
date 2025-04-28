// Aguarda o carregamento completo do DOM
document.addEventListener('DOMContentLoaded', function() {
    const buscarBtn = document.getElementById('buscarBtn');
    const voltarDistritosBtn = document.getElementById('voltarDistritosBtn');
    const especialidadeInput = document.getElementById('especialidadeInput');
    
    // Lista de especialidades disponíveis para autocomplete (exemplo)
    const especialidades = [
        "Clínica Médica",
        "Pediatria",
        "Ginecologia",
        "Cardiologia",
        "Ortopedia",
        "Odontologia",
        "Psicologia",
        "Fisioterapia",
        "Nutrição",
        "Dermatologia"
    ];
    
    // Função simples para autocompletar (poderia ser melhorada com uma biblioteca como jQuery UI)
    function setupAutocomplete() {
        especialidadeInput.addEventListener('input', function() {
            const currentValue = this.value.toLowerCase();
            
            // Limpar autocomplete anterior
            const existingAutocomplete = document.getElementById('autocomplete-list');
            if (existingAutocomplete) {
                existingAutocomplete.remove();
            }
            
            // Se o input estiver vazio, não mostrar sugestões
            if (!currentValue) return;
            
            // Filtrar especialidades que correspondem ao input
            const matchingEspecialidades = especialidades.filter(esp => 
                esp.toLowerCase().includes(currentValue)
            );
            
            // Se houver correspondências, criar lista de autocomplete
            if (matchingEspecialidades.length > 0) {
                const autocompleteList = document.createElement('div');
                autocompleteList.id = 'autocomplete-list';
                autocompleteList.style.position = 'absolute';
                autocompleteList.style.width = '100%';
                autocompleteList.style.backgroundColor = '#fff';
                autocompleteList.style.border = '1px solid #ddd';
                autocompleteList.style.borderTop = 'none';
                autocompleteList.style.borderRadius = '0 0 4px 4px';
                autocompleteList.style.zIndex = '1000';
                autocompleteList.style.maxHeight = '200px';
                autocompleteList.style.overflowY = 'auto';
                
                matchingEspecialidades.forEach(esp => {
                    const item = document.createElement('div');
                    item.textContent = esp;
                    item.style.padding = '10px';
                    item.style.cursor = 'pointer';
                    item.style.borderBottom = '1px solid #f0f0f0';
                    
                    item.addEventListener('mouseenter', function() {
                        this.style.backgroundColor = '#f0f0f0';
                    });
                    
                    item.addEventListener('mouseleave', function() {
                        this.style.backgroundColor = '#fff';
                    });
                    
                    item.addEventListener('click', function() {
                        especialidadeInput.value = esp;
                        autocompleteList.remove();
                    });
                    
                    autocompleteList.appendChild(item);
                });
                
                // Adicionar lista de autocomplete abaixo do input
                const searchBox = document.querySelector('.search-box');
                searchBox.appendChild(autocompleteList);
            }
        });
        
        // Fechar autocomplete ao clicar fora
        document.addEventListener('click', function(e) {
            if (e.target !== especialidadeInput) {
                const existingAutocomplete = document.getElementById('autocomplete-list');
                if (existingAutocomplete) {
                    existingAutocomplete.remove();
                }
            }
        });
    }
    
    // Configurar autocomplete
    setupAutocomplete();
    
    // Evento de buscar especialidade
    if (buscarBtn) {
        buscarBtn.addEventListener('click', function() {
            const especialidade = especialidadeInput.value.trim();
            
            if (especialidade === '') {
                alert('Por favor, informe uma especialidade.');
                return;
            }
            
            // Redirecionar para a página de resultados de postos
            window.location.href = 'postos-proximos.html';
        });
    }
    
    // Evento de voltar para distritos
    if (voltarDistritosBtn) {
        voltarDistritosBtn.addEventListener('click', function() {
            window.location.href = 'distritos.html';
        });
    }
    
    // Permitir pressionar Enter para buscar
    especialidadeInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            if (buscarBtn) {
                buscarBtn.click();
            }
        }
    });
});