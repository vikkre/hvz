<template>
  <nav class="navbar is-fixed-bottom" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <router-link class="navbar-item" to="/">
        <img src="../assets/logos/logo.png" />
        &nbsp;HVZ
      </router-link>

      <a
        role="button"
        class="navbar-burger burger"
        aria-label="menu"
        aria-expanded="false"
        data-target="navbarBasicExample"
        v-bind:class="{'is-active': menuOpen}"
        @click="menuOpen = !menuOpen"
      >
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>

    <div id="navbarBasicExample" class="navbar-menu" v-bind:class="{'is-active': menuOpen}">
      <div class="navbar-start">
        <router-link class="navbar-item" to="/ProductList">Product List</router-link>
        <router-link class="navbar-item" to="/ShoppingList">Shopping List</router-link>
        <router-link class="navbar-item" to="/RecipeList">Recipe List</router-link>
      </div>

      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <a class="button is-primary">
              <strong>Register</strong>
            </a>
            <a class="button is-light">Log in</a>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "MainNavigation",
  data: function() {
    return {
      menuOpen: false
    };
  },
  watch: {
    $route(to, from) {
      this.menuOpen = false;
    }
  }
};
</script>

<style>
</style>