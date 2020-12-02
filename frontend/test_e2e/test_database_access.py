from .database import Database

# db = Database()


def test_get_procuts_from_empty_table(db: Database):
    db.truncate()
    ps = db.get_products()
    assert len(ps) == 0


def test_insert_products(db: Database):
    db.truncate()
    id = db.insert_product(name="Käse", amount=5, required_amount=6)
    assert id != None
    assert id != 0
    p = db.get_products()[0]
    assert p.name == "Käse"
    assert p.amount == 5
    assert p.required_amount == 6


def test_get_product_by_id(db: Database):
    db.truncate()
    id = db.insert_product(name="Käse", amount=5, required_amount=6)
    id = db.insert_product(name="Käse2", amount=10, required_amount=9)
    p = db.get_product_by_id(id)
    assert p.name == "Käse2"
    assert p.amount == 10
    assert p.required_amount == 9
