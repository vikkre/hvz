from base import db


class MenuHasRecipe(db.Model):
	__tablename__ = "menu_has_recipe"
	menu_id = db.Column(db.Integer, db.ForeignKey("menu.id"), primary_key=True)
	recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)
	menu = db.relationship("Menu", back_populates="recipes")
	recipe = db.relationship("Recipe", back_populates="menus")


	def __repr__(self):
		return f"<MenuHasRecipe ({self.recipe_id},{self.menu_id})>"
