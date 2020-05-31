import { ShowModal, ShowSnack } from "./modal.js";
import * as api from "./products_api.js";

const row_template = document.getElementById("row_template");
const product_list = document.getElementById("product_list");
const product_add = document.getElementById("product_add");
const toggle_shopping_list = document.getElementById("toggle_shopping_list");

toggle_shopping_list.addEventListener("click",async e => {
  e.preventDefault()
  document.getElementById("container").style.display = "none"
  document.getElementById("shopping_list").style.display = "unset"

  document.querySelector("body").style.background = "white"
  let products = await  api.loadProducts()
  products.sort((a,b) => a.name < b.name ? -1 : 1)
  products = products.filter(p=> p.needed_amount > 0)
  const tableRowElement = document.querySelector("#shopping_list tbody")
  products.forEach(p => {
    const newRow = document.createElement("tr")
    newRow.innerHTML = `<td>${p.name}</td><td>${p.needed_amount}</td><td><input type="checkbox"/></td>`
    tableRowElement.appendChild(newRow)
  })
})


async function findApiUrl() {
  const urls = ["/api", "http://localhost/api", "http://localhost:5000"];
  const url = new URLSearchParams(window.location.search).get("api");
  return url || urls[0];
}

findApiUrl().then((api_root) => {
  api.setRoot(api_root);
  ShowSnack(`Using api at ${api_root}`);
  loadData();
});

product_add.addEventListener("click", (e) => {
  e.preventDefault();
  const newProduct = document.getElementById("newProduct");
  const data = getProductData(newProduct);
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
    const product_row_element = e
      .composedPath()
      .find((item) => item.dataset && item.dataset.product_id);
    if (product_row_element) {
      const data = getProductData(product_row_element);
      if (e.target.name === "product_save") {
        saveProduct(data);
      } else if (e.target.name === "product_delete") {
        ShowModal(data.name, () => deleteProduct(data));
      }
    }
  }
});

function getProductData(product_row_element) {
  const data = {};
  if (product_row_element.dataset && product_row_element.dataset.product_id) {
    data.id = product_row_element.dataset.product_id;
  }
  data.name = product_row_element.querySelector("input[name='name']").value;
  data.amount = product_row_element.querySelector("input[name='amount']").value;
  data.required_amount = product_row_element.querySelector(
    "input[name='required_amount']"
  ).value;
  return data;
}

function fillTable(data) {
  const oldList = [...product_list.children];
  oldList.forEach((e) => product_list.removeChild(e));

  data.forEach((prod) => {
    const new_row = newProductRowElement(prod);
    product_list.appendChild(new_row);
  });
}

function newProductRowElement(prod) {
  const new_row = row_template.content.cloneNode(true).children[0];
  new_row.id = `product_${prod.id}`;
  new_row.dataset.product_id = prod.id;
  const cells = new_row.querySelectorAll("input");
  cells[0].value = prod.name;
  cells[1].value = prod.amount;
  cells[2].value = prod.required_amount;
  return new_row;
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
    result.sort((a, b) => a.id - b.id);
    fillTable(result);
  } catch (e) {
    ShowSnack(e.message || e, "red");
  }
}
