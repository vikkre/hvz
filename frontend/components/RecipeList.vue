<template>
  <div class="container">
    <div class="modal" v-bind:class="{ 'is-active': showModal }">
      <div class="modal-background"></div>
      <div class="modal-content">
        <article class="message is-primary">
          <div class="message-header">
            <p>{{ modalHeader }}</p>
          </div>
          <div class="message-body mx-6">
            <p>{{ modalText }}</p>
            <div class="columns">
              <div class="column is-8"></div>
              <div class="column">
                <a class="button" name="modal_ok" @click="modalOk">OK</a>
              </div>
              <div class="column">
                <a class="button" name="modal_cancel" @click="modalCancel"
                  >Cancel</a
                >
              </div>
            </div>
          </div>
        </article>
      </div>
    </div>
    <table class="table is-narrow is-hoverable has-background-light">
      <thead>
        <th colspan="4">
          <div class="field has-addons">
            <div class="control is-expanded">
              <input
                name="search_input"
                class="input"
                type="text"
                placeholder="Type here to search..."
                v-model="search"
              />
            </div>
            <div class="control">
              <a class="button" name="clear_search" @click="search = ''">
                <span class="icon grow action">
                  <i class="fas fa-times"></i>
                </span>
              </a>
            </div>
          </div>
        </th>
        <th>
          <div class="control">
            <a class="button" @click="newRecipe()" name="new_recipe">
              <span class="icon grow action">
                <i class="fas fa-plus"></i>
              </span>
            </a>
          </div>
        </th>
      </thead>
      <thead>
        <th>Recipe</th>
        <th>No. of Ingr.</th>
        <th></th>
        <th></th>
      </thead>
      <tbody>
        <tr v-for="r in this.filteredRecipes" v-bind:key="r.id">
          <td name="recipe_name">{{ r.name }}</td>
          <td name="recipe_no_of_ingredients">
            {{ r.products.length }}
          </td>
          <td>
            <span
              class="icon grow action"
              name="edit_recipe"
              @click="editRecipe(r)"
            >
              <i class="fas fa-pen"></i>
            </span>
          </td>

          <td>
            <span
              class="icon grow action"
              name="delete_recipe"
              @click="deleteRecipe(r)"
            >
              <i class="fas fa-trash"></i>
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import * as api from "../recipe_api.js";
export default {
  name: "RecipeList",
  data: function () {
    return {
      recipes: [],
      isLoading: true,
      search: "",
      showModal: false,
      modalText: "Do your really want to delete the product xyz?",
      modalHeader: "Confirm Deletion",
      modalOkCallback: function () {},
    };
  },
  methods: {
    modalOk: function () {
      this.modalOkCallback();
      this.showModal = false;
    },
    modalCancel: function () {
      this.showModal = false;
    },
    deleteRecipe: async function(r) {
      this.modalText = `Do your really want to delete the recipe "${r.name}"?`;
      this.modalHeader = "Confirm Deletion";
      this.showModal = true;
      this.modalOkCallback = async function() {
        await api.deleteRecipe(r.id);
        this.recipes.splice(this.recipes.indexOf(r), 1);
      };
    }, 
    editRecipe: function(recipe) {
      this.$router.push({
        name: "recipeEdit",
        params: { recipe_id: recipe.id, origin: this.$router.currentRoute.fullPath }
      });
    },
    newRecipe: function() {
      this.$router.push({
        name: "recipeEdit",
        params: { recipe_id: undefined, origin: this.$router.currentRoute.fullPath }
      });
    },
  },
  computed: {
    filteredRecipes: function () {
      return this.recipes.filter(
        (p) => p.name.toUpperCase().indexOf(this.search.toUpperCase()) >= 0
      );
    },
  },
  created: async function () {
    this.isLoading = true;
    const rs = await api.loadRecipes();
    this.isLoading = false;
    this.recipes = rs.sort((a, b) => (a.name < b.name ? -1 : 1));
  },
};
</script>

<style>
</style>