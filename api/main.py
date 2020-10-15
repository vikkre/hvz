import base
import endpoint_setup


def main():
	base.app.url_map.strict_slashes = False
	base.init_db()
	endpoint_setup.init_endpoints()


main()
app = base.app
