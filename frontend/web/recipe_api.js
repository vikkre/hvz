let api_root = "/api";

export function setRoot(root) {
  api_root = root;
}

export async function loadRecipes() {
  try {
    const ret = await fetch(`${api_root}/recipe`);
    return await ret.json();
  } catch (error) {
    console.log(error);
    throw new Error("Could not load Recipes.");
  }
}

export async function getRecipe(id) {
  try {
    const ret = await fetch(`${api_root}/recipe/${id}`);
    const json = await ret.json();
    return json.data;
  } catch (error) {
    console.log(error);
    throw new Error("Could not load Recipes.");
  }
}

export async function saveRecipe(data) {
  try {
    data.products.forEach((rp) => {
      delete rp.name;
    });
    const dataJSON = JSON.stringify(data);
    const result = await fetch(`${api_root}/recipe/${data.id}`, {
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
    const dataJSON = JSON.stringify(data);
    const result = await fetch(`${api_root}/recipe`, {
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

export async function deleteRecipe(recipe_id) {
  try {
    const dataJSON = JSON.stringify([{ id: recipe_id }]);
    const result = await fetch(`${api_root}/recipe/${recipe_id}`, {
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
