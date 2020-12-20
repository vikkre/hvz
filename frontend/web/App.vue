<template>
  <div class="has-navbar-fixed-bottom">
    <MainNavigation></MainNavigation>
    <section class="hero">
      <transition name="component-fade" mode="out-in">
        <router-view :apiOnline="apiOnline"></router-view>
      </transition>
      <div v-if="!apiOnline" style="text-align: center; background-color: red; font-size: 32px">API NOT REACHABLE!</div>
    </section>
  </div>
</template>

<script>
import MainNavigation from "./components/MainNavigation.vue";

function checkApiOnline(vm) {
  window.setTimeout(function() {
    fetch("/api")
      .then(result => {
        vm.apiOnline = result.ok;
        checkApiOnline(vm);
      })
      .catch(reason => {
        vm.apiOnline = false;
        checkApiOnline(vm);
      });
  }, 5000);
}

export default {
  components: { MainNavigation },
  data: function() {
    return {
      apiOnline: true,
    };
  },
  name: "App",
  methods: {
    showInfo: function(text) {}
  },
  created: function() {
    checkApiOnline(this);
  }
};
</script>

<style>
.grow {
  transition: all 0.1s ease-in-out;
}

.grow:hover {
  transform: scale(1.2);
}

.component-fade-enter-active,
.component-fade-leave-active {
  transition: opacity 0.3s ease;
}

.component-fade-enter,
.component-fade-leave-to {
  opacity: 0;
}
</style>