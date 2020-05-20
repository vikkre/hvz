import * as api from "../frontend/products_api.js";
const URL = "http://localhost:5000";

function newUniqueProductName() {
  return `product ${new Date().toISOString()}`;
}

function makeNewProduct(values = {}) {
  return { ...{ name: newUniqueProductName() }, ...values };
}

describe("api.loadProducts", function () {
  beforeEach(function () {
    api.setRoot(URL);
  });

  it("should return a list of products as an array", async function () {
    const products = await api.loadProducts();
    expect(products).not.toBeNull();
    expect(products).toBeInstanceOf(Array);
  });

  it("should throw an error when the url is not reachable or the wrong url", async function () {
    api.setRoot(`${URL}/does not exist`);

    await expectAsync(api.loadProducts()).toBeRejectedWith(
      new Error("Could not load Products.")
    );
  });
});

describe("api.insertProduct", function () {
  beforeEach(function () {
    api.setRoot(URL);
  });

  it("should add a single product", async function () {
    const oldProducts = await api.loadProducts();
    const newProduct = makeNewProduct({ amount: 0 });
    const newSavedProduct = await api.insertProduct(newProduct);
    expect(newSavedProduct).not.toBeNull();
    const newProducts = await api.loadProducts();
    expect(newProducts.length - oldProducts.length).toBe(1);
    expect(
      newProducts.find((p) => p.name === newProduct.name).length
    ).not.toBeNull();
  });

  it("should throw an error if the amount is not set", async function () {
    const newProduct = makeNewProduct();
    await expectAsync(api.insertProduct(newProduct)).toBeRejectedWith(
      new Error("Could not save Product.")
    );
  });

  it("should throw an error if a product by the same name exists", async function () {
    const newProduct = makeNewProduct({ amount: 0 });
    await api.insertProduct(newProduct);
    await expectAsync(api.insertProduct(newProduct)).toBeRejectedWith(
      new Error("Could not save Product.")
    );
  });
});

describe("api.saveProduct", function () {
  beforeEach(function () {
    api.setRoot(URL);
  });

  it("should update the amount of a product", async function () {
    const newProduct = makeNewProduct({ amount: 0 });
    await api.insertProduct(newProduct);
    const newProducts = await api.loadProducts();

    const productToUpdate = newProducts.find((p) => p.name === newProduct.name);
    productToUpdate.amount = 1;
    await api.saveProduct(productToUpdate);

    const updatedProduct = await api
      .loadProducts()
      .then((prods) => prods.find((p) => p.id === productToUpdate.id));
    expect(updatedProduct).not.toBeNull();
    expect(updatedProduct.amount).toBe(1);
  });

  it("should update the name of a product", async function () {
    const newProduct = makeNewProduct({ amount: 0 });
    await api.insertProduct(newProduct);
    const newProducts = await api.loadProducts();

    const productToUpdate = newProducts.find((p) => p.name === newProduct.name);
    productToUpdate.amount = 1;
    await api.saveProduct(productToUpdate);

    const updatedProduct = await api
      .loadProducts()
      .then((prods) => prods.find((p) => p.id === productToUpdate.id));
    expect(updatedProduct).not.toBeNull();
    expect(updatedProduct.amount).toBe(1);
  });

  it("should throw an error if a product by the same name exists", async function () {
    const newProduct = makeNewProduct({ amount: 0 });
    const otherProductWithSameName = makeNewProduct(newProduct);
    await api.insertProduct(newProduct);
    await expectAsync(
      api.insertProduct(otherProductWithSameName)
    ).toBeRejectedWith(new Error("Could not save Product."));
  });
});

describe("api.deleteProduct", function () {
  beforeEach(function () {
    api.setRoot(URL);
  });

  it("should just delete the f**** product", async function(){
    const newProduct = makeNewProduct({ amount: 0 });
    const result = await api.insertProduct(newProduct);
    await api.deleteProduct(result.product.id)

    const remainingProducts = await api.loadProducts()
    expect(remainingProducts.find(p => p.id == result.product.id)).nothing()

  });


});