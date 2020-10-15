from base import db


class RecipeHasProduct(db.Model):
	__tablename__ = "recipe_has_product"
	recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)
	product_id = db.Column(db.Integer, db.ForeignKey("product.id"), primary_key=True)
	amount = db.Column(db.Integer, nullable=False)
	recipe = db.relationship("Recipe", back_populates="products")
	product = db.relationship("Product", back_populates="recipes")


	def __repr__(self):
		return f"<RecipeHasProduct ({self.recipe_id},{self.product_id}), amount={self.amount}>"
