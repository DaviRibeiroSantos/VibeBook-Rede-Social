const formulario = document.getElementById('meuFormulario');
    const inputEmail = document.getElementById('emailJs');
    const mensagem = document.getElementById('mensagem');

    formulario.addEventListener('submit', function(evento) {
        // Expressão regular simples para validar e-mail
        const padraoEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (!padraoEmail.test(inputEmail.value)) {
            mensagem.style.color = 'red';
            mensagem.textContent = 'Por favor, insira um e-mail válido.';
            
            // Impede o envio do formulário se o e-mail for inválido
            evento.preventDefault(); 
        } else {
            mensagem.style.color = 'green';
            mensagem.textContent = 'E-mail válido! Enviando...';
        }
    });