let api_root = "/api";


export async function loadProducts() {
  try {
    const ret = await fetch(`${api_root}/products`);
    return await ret.json();
  } catch (error) {
    console.log(error);
    throw new Error("Could not load Products.");
  }
}


export async function getProduct(id) {
  try {
    const ret = await fetch(`${api_root}/products/${id}`);
    return (await ret.json()).product;
  } catch (error) {
    console.log(error);
    throw new Error("Could not load Products.");
  }
}


export async function saveProduct(data) {
  try {
    const dataJSON = JSON.stringify(data);
    const result = await fetch(`${api_root}/products/${data.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: dataJSON,
    });
    if (!result.ok) {
      throw `Backend error: <br> ${result.statusText}`;
    }
    const json = await result.json();
    if (json.error) {
      throw `Error when saving product<br>${json.error}`;
    }
    return json;
  } catch (error) {
    console.log(error);
    throw new Error("Could not save Product.");
  }
}

export async function insertProduct(data) {
  try {
    const dataJSON = JSON.stringify(data);
    const result = await fetch(`${api_root}/products`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: dataJSON,
    });
    if (!result.ok) {
      throw `Backend error: <br> ${result.statusText}`;
    }
    const json = await result.json();
    if (json.error) {
      throw `Error when inserting product<br>${json.error}`;
    }
    return json;
  } catch (error) {
    console.log(error);
    throw new Error("Could not save Product.");
  }
}

export async function deleteProduct(product_id) {
  try {
    const dataJSON = JSON.stringify([{ id: product_id }]);
    const result = await fetch(`${api_root}/products/${product_id}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: dataJSON,
    })
      .then((result) => result.json())
      .then((data) => {
        if (data && data.error) {
          throw `Error when deleting product<br>${data[0].error}`;
        } else {
          return data;
        }
      });
    return result;
  } catch (error) {
    console.log(error);
    throw new Error("could not delete product");
  }
}
