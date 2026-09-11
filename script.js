document.getElementById("clienteForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const nome = document.getElementById("nome").value;
  const telefone = document.getElementById("telefone").value;

  await fetch("/clientes", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({nome, telefone})
  });
  alert("Cliente cadastrado com sucesso!");
});

document.getElementById("veiculoForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const placa = document.getElementById("placa").value;
  const cor = document.getElementById("cor").value;
  const modelo = document.getElementById("modelo").value;
  const marca = document.getElementById("marca").value;
  const ano = document.getElementById("ano").value;
  const tipoPagamento = document.getElementById("tipoPagamento").value;

  await fetch("/veiculos", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({placa, cor, modelo, marca, ano, tipoPagamento})
  });
  alert("Veículo cadastrado com sucesso!");
});
