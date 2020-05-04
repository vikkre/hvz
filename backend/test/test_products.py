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
