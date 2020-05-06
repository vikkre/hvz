const row_template = document.getElementById("row_template");
const product_list = document.getElementById("product_list");
const submit = document.getElementById("submit");
const artikel = document.getElementById("artikel");
const bestand = document.getElementById("bestand");

submit.addEventListener("click", (e) => {
  e.preventDefault();
  data = JSON.stringify([{ name: artikel.value, amount: bestand.value }]);
  artikel.value = null
  bestand.value = null
  fetch("http://localhost/api/products", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: data,
  })
    .then((result) => result.json())
    .then((data) => {
      console.log(data);
      loadData();
    })
    .catch((reason) => console.log(reason));
});

function loadData() {
  fetch("http://localhost/api/products")
    .then((ret) => ret.json())
    .then((data) => {
      table = product_list.parentElement;
      table.removeChild(product_list);
      oldList = [...product_list.children];
      oldList.forEach((e) => product_list.removeChild(e));

      data.forEach((prod) => {
        new_row = row_template.content.cloneNode((deep = true)).children[0];
        new_row.id = `product_${prod.id}`;
        new_row.dataset["product_id"] = prod.id
        cells = new_row.querySelectorAll("td");
        cells[0].innerText = prod.name;
        cells[1].innerText = prod.amount;
        product_list.appendChild(new_row);
      });

      table.appendChild(product_list);
    });
}
loadData();
