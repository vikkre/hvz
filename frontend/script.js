import { ShowModal, ShowSnack } from "./modal.js";
import * as api from "./products_api.js";

const row_template = document.getElementById("row_template");
const product_list = document.getElementById("product_list");
const product_add = document.getElementById("product_add");

async function findApiUrl() {
  const ralfUrl = new URLSearchParams(window.location.search).get("api");
  if (ralfUrl) {
    return ralfUrl;
  }
  const urls = ["/api", "http://localhost/api", "http://localhost:5000"];
  const requests = urls.map((url) => fetch(url));
  const result = await Promise.race(requests).then((x) => x.url);
  return result;
}

findApiUrl().then((api_root) => {
  api.setRoot(api_root);
  ShowSnack(`Using api at ${api_root}`);
  loadData();
});

product_add.addEventListener("click", (e) => {
  e.preventDefault();
  const newProduct = document.getElementById("newProduct");
  const data = {};
  data.name = newProduct.querySelector('input[name="name"]').value;
  data.amount = newProduct.querySelector('input[name="amount"]').value;

  if (data.name.length < 3 || !Number.isInteger(Number(data.amount))) {
    ShowSnack("Enter a valid product", "darkblue");
    return;
  }

  newProduct.querySelector('input[name="name"]').value = "";
  newProduct.querySelector('input[name="amount"]').value = 0;
  try {
    insertProduct(data);
  } catch (error) {
    ShowSnack(error, "red");
  }
});

product_list.addEventListener("click", (e) => {
  if (e.target.tagName === "A") {
    const product = e
      .composedPath()
      .find((item) => item.dataset && item.dataset.product_id);
    if (product) {
      const data = {};
      data.id = product.dataset.product_id;
      data.name = product.querySelector("input[name='name']").value;
      data.amount = product.querySelector("input[name='amount']").value;
      if (e.target.name === "product_save") {
        saveProduct(data);
      } else if (e.target.name === "product_delete") {
        ShowModal(data.name, () => deleteProduct(data));
      }
    }
  }
});

function fillTable(data) {
  const oldList = [...product_list.children];
  oldList.forEach((e) => product_list.removeChild(e));

  data.forEach((prod) => {
    const new_row = row_template.content.cloneNode(true).children[0];
    new_row.id = `product_${prod.id}`;
    new_row.dataset.product_id = prod.id;
    const cells = new_row.querySelectorAll("input");
    cells[0].value = prod.name;
    cells[1].value = prod.amount;
    product_list.appendChild(new_row);
  });

}

async function insertProduct(data) {
  try {
    await api.insertProduct(data);
    ShowSnack(`Product "${data.name}" added.`);
    loadData();
  } catch (error) {
    ShowSnack(error.message || error, "red");
  }
}

async function saveProduct(data) {
  try {
    await api.saveProduct(data);
    ShowSnack(`Product "${data.name}" saved.`);
    loadData();
  } catch (error) {
    ShowSnack(error.message || error, "red");
  }
}

async function deleteProduct(data) {
  try {
    await api.deleteProduct(data.id);
    ShowSnack(`Product "${data.name}" deleted.`);
    loadData();
  } catch (error) {
    ShowSnack(error.message || error, "red");
  }
}

async function loadData() {
  try {
    const result = await api.loadProducts();
    ShowSnack(`Loaded ${result.length} products.`);
    fillTable(result);
  } catch (e) {
    ShowSnack(e.message || e, "red");
  }
}
