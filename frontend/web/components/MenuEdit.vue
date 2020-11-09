<template>
  <section class="section">
    <div class="field">
      <label class="label">Menu date</label>
      <div class="control">
        <input
          class="input"
          name="menu_date"
          v-model="menu.date"
          type="text"
          readonly="true"
          placeholder="set by system on save"
        />
      </div>
    </div>

    <table class="table is-narrow is-hoverable has-background-light">
      <thead>
        <th>Recipe</th>
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
      <tr v-for="r in menu.recipes" v-bind:key="r.id">
        <td>
          <v-select
            :options="recipes"
            v-model="r.recipe"
            taggable
            label="name"
            name="recipe_name"
          ></v-select>
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

import * as api from "../menu_api.js";
import * as recipe_api from "../recipe_api.js";
import "vue-select/dist/vue-select.css";

export default {
  components: {
    Autocomplete,
  },
  name: "MenuEdit",
  props: ["menu_id", "origin"],
  data: function () {
    return {
      menu: {},
      recipes: [],
    };
  },
  methods: {
    doSave: async function () {
      const rs = this.menu.recipes.map((r) => r.recipe);
      this.menu.recipes = rs;
      if (this.menu.id) {
        await api.saveMenu(this.menu);
      } else {
        await api.insertMenu(this.menu);
      }
      this.$router.push(this.origin);
    },
    doCancel: function () {
      this.$router.push(this.origin);
    },
    deleteRecipe: function (r) {
      const index = this.menu.recipes.indexOf(r);
      this.menu.recipes.splice(index, 1);
    },
    newRecipe: function () {
      this.menu.recipes.push({ recipe: { id: null, name: null } });
    },
  },
  created: async function () {
    this.recipes = await recipe_api.loadRecipes();
    if (this.menu_id) {
      const m = await api.getMenu(this.menu_id);
      const rs = m.recipes.map(function (r) {
        return { recipe: r };
      });
      m.recipes = rs;
      this.menu = m;
    } else {
      this.menu = { recipes: [] };
    }
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