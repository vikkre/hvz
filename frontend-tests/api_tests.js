import * as api from "../frontend/products_api.js";

describe("api", function () {
  beforeEach(function () {
    api.setRoot("http://localhost/api");
    api.setRoot("http://localhost:5000");
  });

  it("loadProducts should return a list of products as an array", async function () {
    const products = await api.loadProducts();
    expect(products).not.toBeNull();
    expect(products).toBeInstanceOf(Array);
  });

  it("insertProduct should add a single product", async function () {
      const oldProducts = await api.loadProducts();
      const newProduct = {name: `product ${new Date().toISOString()}`, amount: 0}
      const newSavedProduct = await api.insertProduct(newProduct)
      expect(newSavedProduct).not.toBeNull()
  });
});
