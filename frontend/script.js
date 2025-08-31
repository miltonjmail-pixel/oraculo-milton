function iniciar() {
  const resultados = document.getElementById("resultados");
  resultados.innerHTML = "";
  const evento = new EventSource("/oraculo");
  evento.onmessage = function(e) {
    const div = document.createElement("div");
    div.textContent = e.data;
    resultados.appendChild(div);
  };
}
