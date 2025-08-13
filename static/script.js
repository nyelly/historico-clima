const btnBuscar = document.getElementById('btnBuscar');
const btnHistorico = document.getElementById('btnHistorico');
const resultado = document.getElementById('resultado');

btnBuscar.addEventListener('click', async () => {
  const cidade = document.getElementById('cidade').value.trim();
  if (!cidade) {
    resultado.textContent = 'Por favor, digite uma cidade.';
    return;
  }

  resultado.textContent = 'Carregando...';
  const url = `http://127.0.0.1:5000/clima?cidade=${encodeURIComponent(cidade)}`;

  try {
    const resposta = await fetch(url);
    if (!resposta.ok) throw new Error('Cidade não encontrada ou sem dados.');

    const dados = await resposta.json();
    const dataFormatada = new Date(dados.data_coleta).toLocaleString('pt-BR');

    resultado.innerHTML = `
      <div class="card">
        <strong>${dados.cidade}</strong><br/>
        Temperatura: ${dados.temperatura} °C<br/>
        Umidade: ${dados.umidade}%<br/>
        Data/Hora da solicitação: ${dataFormatada}
      </div>
    `;
  } catch (erro) {
    resultado.textContent = erro.message;
  }
});

btnHistorico.addEventListener('click', async () => {
  const cidade = document.getElementById('cidade').value.trim();
  if (!cidade) {
    resultado.textContent = 'Digite uma cidade para ver o histórico.';
    return;
  }

  resultado.textContent = 'Carregando histórico...';
  const url = `http://127.0.0.1:5000/historico?cidade=${encodeURIComponent(cidade)}`;

  try {
    const resposta = await fetch(url);
    if (!resposta.ok) throw new Error('Erro ao buscar histórico.');

    const dados = await resposta.json();
    if (dados.length === 0) {
      resultado.textContent = 'Nenhum registro encontrado.';
      return;
    }

    let html = `<strong>Histórico de ${cidade}:</strong><table><tr><th>Data/Hora</th><th>Temperatura (°C)</th><th>Umidade (%)</th></tr>`;
    dados.forEach(item => {
      const dataFormatada = new Date(item.data_coleta).toLocaleString('pt-BR');
      html += `<tr><td>${dataFormatada}</td><td>${item.temperatura}</td><td>${item.umidade}</td></tr>`;
    });
    html += '</table>';
    resultado.innerHTML = html;
  } catch (erro) {
    resultado.textContent = erro.message;
  }
});
