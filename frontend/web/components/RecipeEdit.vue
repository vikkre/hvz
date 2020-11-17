<template>
  <section class="section">
    <div class="field">
      <label class="label">Recipe name</label>
      <div class="control">
        <input
          class="input"
          name="recipe_name"
          v-model="recipe.name"
          type="text"
          placeholder="e.g. Spaghetti Carbonara"
        />
      </div>
    </div>

    <div class="field">
      <label class="label">Text</label>
      <div class="control">
        <textarea
          class="textarea"
          name="recipe_text"
          v-model="recipe.text"
        ></textarea>
      </div>
    </div>

    <table class="table is-narrow is-hoverable has-background-light">
      <thead>
        <th>Ingredient</th>
        <th>Amount</th>
        <th>
          <div class="control">
            <a class="button" @click="newIngredient()" name="new_ingredient">
              <span class="icon grow action">
                <i class="fas fa-plus"></i>
              </span>
            </a>
          </div>
        </th>
      </thead>
      <tr v-for="i in recipe.products" v-bind:key="i.id">
        <td>
          <v-select
            :options="products"
            v-model="i.product"
            taggable
            label="name"
            name="product_name"
          ></v-select>
        </td>
        <td>
          <input
            class="input"
            v-model="i.amount"
            type="number"
            placeholder="eg. 5"
            name="product_amount"
          />
        </td>
        <td>
          <span
            class="icon grow action"
            name="delete_ingredient"
            @click="deleteIngredient(i)"
          >
            <i class="fas fa-trash"></i>
          </span>
        </td>
      </tr>
    </table>

    <div class="field is-grouped">
      <div class="control">
        <button
          class="button is-link action grow"
          name="save"
          @click="doSave()"
        >
          Save
        </button>
      </div>
      <div class="control">
        <button
          class="button is-link is-light action grow"
          name="cancel"
          @click="doCancel()"
        >
          Cancel
        </button>
      </div>
    </div>
  </section>
</template>

<script>
import Autocomplete from "@trevoreyre/autocomplete-vue";

import * as api from "../recipe_api.js";
import * as product_api from "../products_api.js";
import "vue-select/dist/vue-select.css";

function fmap(rp) {
  return {
    amount: rp.amount,
    product: { name: rp.name, id: rp.id },
  };
}

function funmap(rp) {
  return {
    amount: rp.amount,
    id: rp.product.id,
    name: rp.product.name,
  };
}

export default {
  components: {
    Autocomplete,
  },
  name: "RecipeEdit",
  props: ["recipe_id", "origin"],
  data: function () {
    return {
      recipe: {},
      products: [],
    };
  },
  methods: {
    doSave: async function () {
      const r = JSON.parse(JSON.stringify(this.recipe));
      for (const rp of r.products) {
        if (!rp.product.id) {
          const result = await product_api.insertProduct({
            name: rp.product.name,
            required_amount: 0,
            amount: 0,
          });
          rp.product.id = result.product.id;
        }
      }
      r.products = r.products.map(funmap);
      if (r.id) {
        await api.saveRecipe(r);
      } else {
        await api.insertRecipe(r);
      }
      this.$router.push("/RecipeList");
    },
    doCancel: function () {
      this.$router.push("/RecipeList");
    },
    deleteIngredient: function (i) {
      const index = this.recipe.products.indexOf(i);
      this.recipe.products.splice(index, 1);
    },
    newIngredient: function () {
      this.recipe.products.push({
        amount: 0,
        product: { id: null, name: null },
      });
    },
  },
  created: async function () {
    this.products = await product_api.loadProducts();
    if (this.recipe_id) {
      const r = await api.getRecipe(this.recipe_id);
      const rps = r.products.map(fmap);
      r.products = rps;
      this.recipe = r;
    } else {
      this.recipe = { name: "", text: "", products: [] };
    }
  },
  computed: {
    filteredDataArray(inp) {
      return this.products.filter((option) => {
        return option.name.toLowerCase().indexOf(inp.toLowerCase()) >= 0;
      });
    },
  },
};
</script>

<style scoped>
.action {
  cursor: pointer;
}
</style>

<style> 
.v-select {
  background-color: white;
}
.vs__dropdown-toggle {
    padding: 2px 5px 7px;
}
.vs__open-indicator {
    cursor: pointer;
}
</style>