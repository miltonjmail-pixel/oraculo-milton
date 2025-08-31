function iniciarPatrullaje() {
  fetch("/iniciar-patrullaje", { method: "POST" })
    .then(res => res.json())
    .then(data => {
      document.getElementById("estado").textContent = "Patrullaje en curso ✅";
      console.log("Patrullaje iniciado:", data);
    });
}

fetch("/estado")
  .then(res => res.json())
  .then(data => {
    const estado = data.patrullaje ? "Patrullaje en curso ✅" : "Sin patrullaje activo ⛔";
    document.getElementById("estado").textContent = estado;
  });

const eventSource = new EventSource("/stream");
eventSource.onmessage = function (event) {
  const h = JSON.parse(event.data);
  const li = document.createElement("li");
  li.textContent = `${h.id} | ${h.timestamp} | ${h.zona} | ${h.evento} | ${h.hash}`;
  document.getElementById("hallazgos").prepend(li);
};
