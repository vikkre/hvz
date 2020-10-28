from collections import namedtuple
from warnings import resetwarnings
from sqlalchemy import create_engine, MetaData
import os


class Database():
    def __init__(self) -> None:
        db_server = os.getenv("DB_HOST", "localhost")
        self.eng = create_engine(
            f'postgresql://admin:admin@{db_server}/hvz_production')
        self.meta = MetaData()
        self.meta.reflect(self.eng)
        self.table_names = ['recipe_has_product', 'menu_has_recipe', 'menu',
                            'recipe', 'product', ]
        self.tabs = namedtuple("tables", self.table_names)(
            ** {k: self.meta.tables[k] for k in self.table_names})

    def truncate(self):
        for t in self.table_names:
            dele = self.meta.tables[t].delete()
            self.eng.execute(dele)

    def get_products(self):
        return self.eng.execute(self.tabs.product.select()).fetchall()

    def insert_product(self, **kwargs):
        ins = self.tabs.product.insert().values(**kwargs)
        return self.eng.execute(ins).inserted_primary_key[0]

    def get_product_by_id(self, id):
        sel = self.tabs.product.select().where(self.tabs.product.c.id == id)
        return self.eng.execute(sel).first()

    def insert_2_dummy_products(self):
        ins = self.tabs.product.insert()
        products = [dict(name="Milch", amount=1, required_amount=2),
                    dict(name="Burger", amount=5, required_amount=10)]
        result = self.eng.execute(ins, products)
        return result

    def insert_4_dummy_products_for_shopping_list(self):
        ins = self.tabs.product.insert()
        products = [
            dict(name="Milch", amount=1, required_amount=2),
            dict(name="Burger", amount=5, required_amount=10),
            dict(name="Käse", amount=9, required_amount=10),
            dict(name="Butter", amount=5, required_amount=1),
        ]
        result = self.eng.execute(ins, products)
        return result

    def insert_2_recipes(self):
        insp = self.tabs.product.insert()
        insr = self.tabs.recipe.insert()
        insrp = self.tabs.recipe_has_product.insert()

        products = [
            dict(name="Eier"),
            dict(name="Speck"),
            dict(name="Sahne"),
            dict(name="Knoblauch"),
            dict(name="Parmesan"),
            dict(name="Spaghetti"),
            dict(name="Marsalla"),
        ]
        for p in products:
            p["amount"] = 10
        self.eng.execute(insp, products)
        recipes = [
            dict(name="Carbonara"),
            dict(name="Zabaione")
        ]
        self.eng.execute(insr, recipes)

        products = self.eng.execute(self.tabs.product.select()).fetchall()
        pd = {k: id for (id, k, _, _) in products}
        recipes = self.eng.execute(self.tabs.recipe.select()).fetchall()
        rd = {k: id for (id, k, _) in recipes}

        recipe_has_product = [
            dict(recipe_id=rd["Carbonara"], product_id=pd["Eier"], amount=1),
            dict(recipe_id=rd["Carbonara"], product_id=pd["Speck"], amount=2),
            dict(recipe_id=rd["Carbonara"], product_id=pd["Sahne"], amount=3),
            dict(recipe_id=rd["Carbonara"],
                 product_id=pd["Knoblauch"], amount=4),
            dict(recipe_id=rd["Carbonara"],
                 product_id=pd["Parmesan"], amount=5),
            dict(recipe_id=rd["Carbonara"],
                 product_id=pd["Spaghetti"], amount=6),
            dict(recipe_id=rd["Zabaione"], product_id=pd["Eier"], amount=7),
            dict(recipe_id=rd["Zabaione"],
                 product_id=pd["Marsalla"], amount=8),
        ]
        self.eng.execute(insrp, recipe_has_product)
