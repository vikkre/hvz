let api_root = "/api";

export function setRoot(root) {
  api_root = root;
}

export async function loadMenus() {
  try {
    const ret = await fetch(`${api_root}/menu`);
    return await ret.json();
  } catch (error) {
    console.log(error);
    throw new Error("Could not load Menus.");
  }
}

export async function getMenu(id) {
  try {
    const ret = await fetch(`${api_root}/menu/${id}`);
    const json = await ret.json();
    return json.data; 
  } catch (error) {
    console.log(error);
    throw new Error("Could not load Menu.");
  }
}

export async function saveMenu(data) {
  try {
    const dataJSON = JSON.stringify(data);
    const result = await fetch(`${api_root}/menu/${data.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: dataJSON,
    });
    if (!result.ok) {
      throw `Backend error: <br> ${result.statusText}`;
    }
    const json = await result.json();
    if (json.error) {
      throw `Error when saving menu<br>${json.error}`;
    }
    return json;
  } catch (error) {
    console.log(error);
    throw new Error("Could not save Menu.");
  }
}

export async function insertMenu(data) {
  try {
    const dataJSON = JSON.stringify(data);
    const result = await fetch(`${api_root}/menu`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: dataJSON,
    });
    if (!result.ok) {
      throw `Backend error: <br> ${result.statusText}`;
    }
    const json = await result.json();
    if (json.error) {
      throw `Error when inserting menu<br>${json.error}`;
    }
    return json;
  } catch (error) {
    console.log(error);
    throw new Error("Could not save Menu.");
  }
}

export async function deleteMenu(menu_id) {
  try {
    const dataJSON = JSON.stringify([{ id: menu_id }]);
    const result = await fetch(`${api_root}/menu/${menu_id}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: dataJSON,
    })
      .then((result) => result.json())
      .then((data) => {
        if (data && data.error) {
          throw `Error when deleting menu<br>${data[0].error}`;
        } else {
          return data;
        }
      });
    return result;
  } catch (error) {
    console.log(error);
    throw new Error("could not delete Menu");
  }
}
