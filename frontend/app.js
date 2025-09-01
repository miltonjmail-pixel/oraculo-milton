function actualizarEstado(mensaje) {
  document.getElementById("estado").textContent = mensaje;
}

function iniciarPatrullaje() {
  console.log("Iniciando patrullaje...");
  fetch("/iniciar-patrullaje", { method: "POST" })
    .then(res => res.json())
    .then(data => {
      actualizarEstado("Patrullaje en curso ✅");
      console.log("Respuesta:", data);
    })
    .catch(err => {
      actualizarEstado("Error al iniciar patrullaje ⚠️");
      console.error("Error:", err);
    });
}

function detenerPatrullaje() {
  console.log("Deteniendo patrullaje...");
  fetch("/detener-patrullaje", { method: "POST" })
    .then(res => res.json())
    .then(data => {
      actualizarEstado("Sin patrullaje activo ⛔");
      console.log("Respuesta:", data);
    })
    .catch(err => {
      actualizarEstado("Error al detener patrullaje ⚠️");
      console.error("Error:", err);
    });
}

// Estado inicial al cargar
fetch("/estado")
  .then(res => res.json())
  .then(data => {
    const estado = data.patrullaje ? "Patrullaje en curso ✅" : "Sin patrullaje activo ⛔";
    actualizarEstado(estado);
  })
  .catch(err => {
    actualizarEstado("Estado desconocido ⚠️");
    console.error("Error al consultar estado:", err);
  });

// Eventos SSE
const eventSource = new EventSource("/stream");
eventSource.onmessage = function (event) {
  try {
    const h = JSON.parse(event.data);
    const li = document.createElement("li");
    li.textContent = `${h.id} | ${h.timestamp} | ${h.zona} | ${h.evento} | ${h.hash}`;
    document.getElementById("hallazgos").prepend(li);
  } catch (err) {
    console.error("Error al procesar evento SSE:", err);
  }
};
