<script>
  // 🔄 Actualiza el estado del patrullaje en el DOM
  function actualizarEstado(mensaje) {
    document.getElementById("estado").textContent = mensaje;
  }

  // 🚀 Inicia el patrullaje
  function iniciarPatrullaje() {
    fetch("/iniciar-patrullaje", { method: "POST" })
      .then(res => res.json())
      .then(data => {
        actualizarEstado("Patrullaje en curso ✅");
        console.log("Patrullaje iniciado:", data);
      })
      .catch(err => console.error("Error al iniciar patrullaje:", err));
  }

  // 🛑 Detiene el patrullaje
  function detenerPatrullaje() {
    fetch("/detener-patrullaje", { method: "POST" })
      .then(res => res.json())
      .then(data => {
        actualizarEstado("Sin patrullaje activo ⛔");
        console.log("Patrullaje detenido:", data);
      })
      .catch(err => console.error("Error al detener patrullaje:", err));
  }

  // 📡 Consulta el estado actual al cargar
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

  // 🔁 Escucha eventos SSE en tiempo real
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
</script>
