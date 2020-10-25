import "core-js/stable";
import "regenerator-runtime/runtime";

import Vue from "vue";
import VueRouter from "vue-router";

import App from "./App.vue";
import ProductList from "./components/ProductList.vue";
import ProductEdit from "./components/ProductEdit.vue";

import ShoppingList from "./components/ShoppingList.vue";
import RecipeList from "./components/RecipeList.vue";
import RecipeEdit from "./components/RecipeEdit.vue";
import SplashScreen from "./components/SplashScreen.vue";
import vSelect from 'vue-select'

Vue.component('v-select', vSelect)

Vue.use(VueRouter);

const routes = [
  { path: "/ProductList", component: ProductList },
  {
    path: "/ProductEdit",
    component: ProductEdit,
    name: "productEdit",
    props: true,
  },
  { path: "/ShoppingList", component: ShoppingList },
  { path: "/RecipeList", component: RecipeList, name: "Recipes" },
  {
    path: "/RecipeEdit",
    component: RecipeEdit,
    name: "recipeEdit",
    props: true,
  },
  { path: "*", component: SplashScreen },
];

const router = new VueRouter({
  routes,
});

Vue.config.productionTip = false;
new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
