const row_template = document.getElementById("row_template");
const product_list = document.getElementById("product_list");
const product_add = document.getElementById("product_add");
const new_product_artikel = document.getElementById("new_product_artikel");
const new_product_bestand = document.getElementById("new_product_bestand");

// const api_root = "http://localhost/api";
const api_root = "http://localhost:5000";

function showSnack(text, color = "var(--color") {
  Toastify({
    text: text,
    duration: 3000,
    close: true,
    gravity: "bottom", // `top` or `bottom`
    position: "right", // `left`, `center` or `right`
    backgroundColor: color,
    stopOnFocus: true, // Prevents dismissing of toast on hover
  }).showToast();
}

product_add.addEventListener("click", (e) => {
  e.preventDefault();
  if (
    new_product_artikel.value.length < 3 ||
    !Number.isInteger(new_product_bestand.valueAsNumber)
  ) {
    showSnack("Enter a valid product", "darkblue");
    return;
  }
  data = [
    {
      name: new_product_artikel.value,
      amount: new_product_bestand.valueAsNumber,
    },
  ];
  dataJSON = JSON.stringify(data);
  new_product_artikel.value = "";
  new_product_bestand.value = 0;
  fetch(`${api_root}/products`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: dataJSON,
  })
    .then((result) => result.json())
    .then((data) => {
      console.log(data);
      if (data[0].status !== "ok") {
        showSnack(data[0].error);
      }
      showSnack(`Product "${data[0].product.name}" added.`);
      loadData();
    })
    .catch((reason) => showSnack(reason.message, "red"));
});

product_list.addEventListener("click", (e) => {
  if (e.target.tagName === "A") {
    const product = e
      .composedPath()
      .find((item) => item.dataset && item.dataset["product_id"]);
    if (product) {
      const product_id = product.dataset["product_id"];
      const t = `I would like to ${e.target.innerText} the product with id = ${product_id}`;
      showSnack(t);
    }
  }
});

function loadData() {
  fetch(`${api_root}/products`)
    .then((ret) => ret.json())
    .then((data) => {
      table = product_list.parentElement;
      table.removeChild(product_list);
      oldList = [...product_list.children];
      oldList.forEach((e) => product_list.removeChild(e));

      data.forEach((prod) => {
        new_row = row_template.content.cloneNode((deep = true)).children[0];
        new_row.id = `product_${prod.id}`;
        new_row.dataset["product_id"] = prod.id;
        cells = new_row.querySelectorAll("input");
        cells[0].value = prod.name;
        cells[1].value = prod.amount;
        product_list.appendChild(new_row);
      });

      table.appendChild(product_list);
      showSnack(`Loaded ${data.length} products`);
    })
    .catch((e) => {
      showSnack(e.message, "red");
    });
}

loadData();
