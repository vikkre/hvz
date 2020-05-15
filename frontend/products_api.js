let api_root = ''

export function setRoot(root) {
  api_root = root
}

export async function loadProducts() {
  const result = await fetch(`${api_root}/products`)
    .then(ret => ret.json())
    .then(data => {
      return data
    })

  return result
}

async function upsertProduct(data, http_method, op_name) {
  const dataJSON = JSON.stringify([data])
  const result = await fetch(`${api_root}/products`, {
    method: http_method,
    headers: { 'Content-Type': 'application/json' },
    body: dataJSON,
  })
    .then(result => {
      if (!result.ok) {
        throw `Backend error: <br> ${result.statusText}`
      }
      return result.json()
    })
    .then(data => {
      if (data[0].error) {
        throw `Error when ${op_name} product<br>${data[0].error}`
      } else {
        return data
      }
    })
  return result
}

export async function saveProduct(data) {
  return await upsertProduct(data, 'PUT', 'saving')
}

export async function insertProduct(data) {
  return await upsertProduct(data, 'POST', 'inserting')
}

export async function deleteProduct(product_id) {
  const dataJSON = JSON.stringify([{ id: product_id }])
  const result = await fetch(`${api_root}/products`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: dataJSON,
  })
    .then(result => result.json())
    .then(data => {
      if (data[0].error) {
        throw `Error when saving product<br>${data[0].error}`
      } else {
        return data
      }
    })
  return result
}
