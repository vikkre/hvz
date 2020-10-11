from base import db


class RecipeHasProduct(db.Model):
	__tablename__ = "recipe_has_product"
	product_id = db.Column(db.Integer, db.ForeignKey("product.id"), primary_key=True)
	recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)
	amount = db.Column(db.Integer, nullable=False)
	product = db.relationship("Product", back_populates="recipes")
	recipe = db.relationship("Recipe", back_populates="products")


	def __repr__(self):
		return f"<RecipeHasProduct ({self.product_id},{self.recipe_id}), amount={self.amount}>"
