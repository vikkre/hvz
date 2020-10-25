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
      <tr v-for="i in recipe.required_products" v-bind:key="i.id">
        <td>
          <!-- <input
            class="input"
            name="product_name"
            v-model="i.product.name"
            type="text"
            placeholder="eg. Eggs"
          /> -->
          <v-select
            :options="products"
            v-model="i.product"
            taggable
            label="name"
          ></v-select>
        </td>
        <td>
          <input
            class="input"
            name="amount"
            v-model="i.amount"
            type="number"
            placeholder="eg. 5"
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
    recipe_id: rp.recipe_id,
    product: { name: rp.product_name, id: rp.product_id },
  };
}

function funmap(rp) {
  return {
    amount: rp.amount,
    recipe_id: rp.recipe_id,
    product_name: rp.product.name,
    product_id: rp.product.id,
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
      if (this.recipe_id) {
        const r = this.recipe
        for (const rp of r.required_products) {
          if (!rp.product.id) {
            const result = await product_api.insertProduct({name: rp.product.name, required_amount:0, amount: 0})
            console.log(result)
            rp.product.id = result.product.id
          }
        }
        r.required_products = r.required_products.map(funmap);
        await api.saveRecipe(r);
      } else {
        await api.insertRecipe(r);
      }
      this.$router.push(this.origin);
    },
    doCancel: function () {
      this.$router.push(this.origin);
    },
    deleteIngredient: function (i) {
      const index = this.recipe.required_products.indexOf(i);
      this.recipe.required_products.splice(index, 1);
    },
    newIngredient: function () {
      this.recipe.required_products.push({
        amount: 0,
        recipe_id: this.recipe.id,
        product: { id: null, name: null },
      });
    },
  },
  created: async function () {
    this.products = await product_api.loadProducts();
    if (this.recipe_id) {
      const r = await api.getRecipe(this.recipe_id);
      const rps = r.required_products.map(fmap);
      r.required_products = rps;
      this.recipe = r;
    } else {
      this.recipe = { name: "", text: "", required_products: [] };
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