def test_get_products(client_products):
	get_response = client_products.get("/products")

	assert get_response.json == client_products.expected


def test_get_single_product(client_products):
	id = client_products.expected[0]["id"]

	get_response = client_products.get("/products/" + str(id))
	assert get_response.json["status"] == "ok"
	assert get_response.json["product"]["name"] == client_products.expected[0]["name"]
	assert get_response.json["product"]["amount"] == client_products.expected[0]["amount"]


def test_get_single_product_not_found(client_products):
	id = 12345

	get_response = client_products.get("/products/" + str(id))
	assert get_response.json["status"] == "failed"
	assert get_response.json["error"] == "product_not_found"


def test_post_products(client_products):
	data = {
		"name": "Kaffee",
		"amount": 2
	}

	post_response = client_products.post("/products", json=data)
	assert post_response.json["status"] == "ok"

	get_response = client_products.get("/products")
	assert len(get_response.json) == len(client_products.expected) + 1


def test_post_products_double_insert(client_products):
	data = {
		"name": "Sahne",
		"amount": 3
	}

	post_response = client_products.post("/products", json=data)
	assert post_response.json["status"] == "ok"

	post_response = client_products.post("/products", json=data)
	assert post_response.json["status"] == "failed"
	assert post_response.json["error"] == "product_alredy_exits"

	get_response = client_products.get("/products")
	assert len(get_response.json) == len(client_products.expected) + 1


def test_update_product(client_products):
	new_milk_name = "Milch Milch"
	id = client_products.expected[0]["id"]

	data = {
		"name": new_milk_name
	}
	
	put_response = client_products.put("/products/" + str(id), json=data)
	assert put_response.json["status"] == "ok"
	assert put_response.json["product"]["name"] == new_milk_name


def test_update_product_no_product_found(client_products):
	id = 12345
	data = {
		"amount": 123
	}

	put_response = client_products.put("/products/" + str(id), json=data)
	assert put_response.json["status"] == "failed"
	assert put_response.json["error"] == "product_not_found"


def test_delete_product(client_products):
	id = client_products.expected[0]["id"]

	delete_response = client_products.delete("/products/" + str(id))
	assert delete_response.json["status"] == "ok"
	assert delete_response.json["product"]["name"] == client_products.expected[0]["name"]
	assert delete_response.json["product"]["amount"] == client_products.expected[0]["amount"]

	get_response = client_products.get("/products")
	assert len(get_response.json) == len(client_products.expected) - 1


def test_delete_product_no_product_found(client_products):
	id = 12345

	delete_response = client_products.delete("/products/" + str(id))
	assert delete_response.json["status"] == "failed"
	assert delete_response.json["error"] == "product_not_found"

	get_response = client_products.get("/products")
	assert len(get_response.json) == len(client_products.expected)
