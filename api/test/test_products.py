def test_get_products(client_products):
	response = client_products.get("/products")

	assert response.json == client_products.expected


def test_post_products(client_products):
	data = [
		{
			"name": "Kaffee",
			"amount": 2
		},
		{
			"name": "Sahne",
			"amount": 3
		}
	]

	post_response = client_products.post("/products", json=data)
	assert post_response.json[0]["status"] == "ok"
	assert post_response.json[1]["status"] == "ok"

	get_response = client_products.get("/products")
	assert len(get_response.json) == len(client_products.expected) + len(data)


def test_post_products_double_insert(client_products):
	data = [
		{
			"name": "Milch",
			"amount": 2
		},
		{
			"name": "Sahne",
			"amount": 3
		}
	]

	post_response = client_products.post("/products", json=data)
	assert post_response.json[0]["status"] == "failed"
	assert post_response.json[1]["status"] == "ok"
	assert post_response.json[0]["error"] == "product_alredy_exits"

	get_response = client_products.get("/products")
	assert len(get_response.json) == len(client_products.expected) + 1


def test_update_product(client_products):
	new_milk_name = "Milch Milch"
	new_burger_amount = 10

	data = [
		{
			"id": client_products.expected[0]["id"],
			"name": new_milk_name
		},
		{
			"id": client_products.expected[1]["id"],
			"amount": new_burger_amount
		}
	]
	
	put_response = client_products.put("/products", json=data)
	assert len(put_response.json) == len(data)

	assert put_response.json[0]["status"] == "ok"
	assert put_response.json[0]["product"]["name"] == new_milk_name

	assert put_response.json[1]["status"] == "ok"
	assert put_response.json[1]["product"]["amount"] == new_burger_amount


def test_update_product_no_id(client_products):
	data = [
		{
			"amount": 123
		}
	]

	put_response = client_products.put("/products", json=data)
	assert len(put_response.json) == len(data)

	assert put_response.json[0]["status"] == "failed"
	assert put_response.json[0]["error"] == "id_not_provided"


def test_update_product_no_product_found(client_products):
	data = [
		{
			"id": 12345,
			"amount": 123
		}
	]

	put_response = client_products.put("/products", json=data)
	assert len(put_response.json) == len(data)

	assert put_response.json[0]["status"] == "failed"
	assert put_response.json[0]["error"] == "product_not_found"


def test_delete_product(client_products):
	data = [
		{
			"id": client_products.expected[0]["id"]
		}
	]

	delete_response = client_products.delete("/products", json=data)
	assert len(delete_response.json) == len(data)

	assert delete_response.json[0]["status"] == "ok"
	assert delete_response.json[0]["product"]["name"] == client_products.expected[0]["name"]
	assert delete_response.json[0]["product"]["amount"] == client_products.expected[0]["amount"]

	get_response = client_products.get("/products")
	assert len(get_response.json) == len(client_products.expected) - len(data)


def test_delete_product_no_id(client_products):
	data = [
		{
		}
	]

	delete_response = client_products.delete("/products", json=data)
	assert len(delete_response.json) == len(data)

	assert delete_response.json[0]["status"] == "failed"
	assert delete_response.json[0]["error"] == "id_not_provided"

	get_response = client_products.get("/products")
	assert len(get_response.json) == len(client_products.expected)


def test_delete_product_no_product_found(client_products):
	data = [
		{
			"id": 12345
		}
	]

	delete_response = client_products.delete("/products", json=data)
	assert len(delete_response.json) == len(data)

	assert delete_response.json[0]["status"] == "failed"
	assert delete_response.json[0]["error"] == "product_not_found"

	get_response = client_products.get("/products")
	assert len(get_response.json) == len(client_products.expected)
