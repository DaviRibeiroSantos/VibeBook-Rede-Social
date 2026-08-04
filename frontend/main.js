const formulario = document.getElementById('cadastroForm');
    const inputEmail = document.getElementById('emailJs');
    const mensagem = document.getElementById('mensagem');

    formulario.addEventListener('submit', function(evento) {
      
        const padraoEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (!padraoEmail.test(inputEmail.value)) {
            mensagem.style.color = 'red';
            mensagem.textContent = 'Por favor, insira um e-mail válido.';
            
        
            evento.preventDefault(); 
        } else {
            mensagem.style.color = 'green';
            mensagem.textContent = 'E-mail válido! Enviando...';
        }
    });