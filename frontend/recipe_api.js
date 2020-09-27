let api_root = "";

let data = [
  {
    id: 1,
    name: "Hamburger",
    preparation: `Lorem, ipsum dolor sit amet consectetur adipisicing elit. Fuga eligendi, expedita debitis quis aperiam hic laudantium doloremque doloribus tempore nemo et error ea, inventore iusto! Ut, expedita iusto. Aspernatur, molestiae! `,
    ingredients: [
      { product_id: 1, product_name: "Minced meat", amount: "250g" },
      { product_id: 2, product_name: "Tomato", amount: "1" },
      { product_id: 3, product_name: "Letuce", amount: "1" },
      { product_id: 4, product_name: "Onions", amount: "1" },
      { product_id: 5, product_name: "Ketchup", amount: "1" },
    ],
  },
  {
    id: 2,
    name: "Spaghetti Carbonara",
    preparation: `Lorem, ipsum dolor sit amet consectetur adipisicing elit. Fuga eligendi, expedita debitis quis aperiam hic laudantium doloremque fdoloribus tempore nemo et error ea, inventore iusto! Ut, expedita iusto. Aspernatur, molestiae! `,
    ingredients: [
      { product_id: 1, product_name: "Pasta / Spaghetti", amount: "250g" },
      { product_id: 2, product_name: "Egg", amount: "2" },
      { product_id: 3, product_name: "Cream", amount: "250ml" },
      { product_id: 4, product_name: "Garlic", amount: "1" },
      { product_id: 5, product_name: "Bacon", amount: "80g" },
      { product_id: 6, product_name: "Parmesan Cheese", amount: "80g" },
    ],
  },
];

export function setRoot(root) {
  api_root = root;
}

export async function loadRecipes() {
  try {
    return data;
    const ret = await fetch(`${api_root}/recipes`);
    return await ret.json();
  } catch (error) {
    console.log(error);
    throw new Error("Could not load Recipes.");
  }
}

export async function getProducts() {
  let ingredientArrays = data.map((r) => r.ingredients);
  return [].concat(ingredientArrays);
}

export async function saveRecipe(data) {
  try {
    throw "not implemented yet";
    const dataJSON = JSON.stringify(data);
    const result = await fetch(`${api_root}/recipes/${data.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: dataJSON,
    });
    if (!result.ok) {
      throw `Backend error: <br> ${result.statusText}`;
    }
    const json = await result.json();
    if (json.error) {
      throw `Error when saving recipe<br>${json.error}`;
    }
    return json;
  } catch (error) {
    console.log(error);
    throw new Error("Could not save Recipe.");
  }
}

export async function insertRecipe(data) {
  try {
    throw "not implemented";
    const dataJSON = JSON.stringify(data);
    const result = await fetch(`${api_root}/recipes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: dataJSON,
    });
    if (!result.ok) {
      throw `Backend error: <br> ${result.statusText}`;
    }
    const json = await result.json();
    if (json.error) {
      throw `Error when inserting recipe<br>${json.error}`;
    }
    return json;
  } catch (error) {
    console.log(error);
    throw new Error("Could not save Recipe.");
  }
}

export async function deleteRecipe(product_id) {
  try {
    throw "not implemented";
    const dataJSON = JSON.stringify([{ id: recipe_id }]);
    const result = await fetch(`${api_root}/recipes/${product_id}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: dataJSON,
    })
      .then((result) => result.json())
      .then((data) => {
        if (data && data.error) {
          throw `Error when deleting recipe<br>${data[0].error}`;
        } else {
          return data;
        }
      });
    return result;
  } catch (error) {
    console.log(error);
    throw new Error("could not delete recipe");
  }
}
