def test_get_root(client_app):
	response = client_app.get("/")
	assert response.data == b"Hello World\n"
