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
            <a class="button" @click="newMenu()" name="new_menu">
              <span class="icon grow action">
                <i class="fas fa-plus"></i>
              </span>
            </a>
          </div>
        </th>
      </thead>
      <thead>
        <th>Menu</th>
        <th>No. of Rec.</th>
        <th></th>
        <th></th>
      </thead>
      <tbody>
        <tr v-for="m in this.filteredMenus" v-bind:key="m.id">
          <td name="menu_date">{{ m.posix_time | formatDate }}</td>
          <td name="no_of_recipes">
            {{ m.recipes.length }}
          </td>
          <td>
            <span
              class="icon grow action"
              name="edit_menu"
              @click="editMenu(m)"
            >
              <i class="fas fa-pen"></i>
            </span>
          </td>

          <td>
            <span
              class="icon grow action"
              name="delete_menu"
              @click="deleteMenu(m)"
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
import * as api from "../menu_api.js";
import moment from 'moment'
export default {
  name: "MenuList",
  data: function () {
    return {
      menus: [],
      isLoading: true,
      search: "",
      showModal: false,
      modalText: "Do your really want to delete the menu xyz?",
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
    deleteMenu: async function(m) {
      this.modalText = `Do your really want to delete the menu "${m.date}"?`;
      this.modalHeader = "Confirm Deletion";
      this.showModal = true;
      this.modalOkCallback = async function() {
        await api.deleteMenu(m.id);
        this.menus.splice(this.menus.indexOf(m), 1);
      };
    }, 
    editMenu: function(menu) {
      this.$router.push({
        name: "menuEdit",
        params: { menu_id: menu.id, origin: this.$router.currentRoute.fullPath }
      });
    },
    newMenu: function() {
      this.$router.push({
        name: "menuEdit",
        params: { menu_id: undefined, origin: this.$router.currentRoute.fullPath }
      });
    },
  },
  computed: {
    filteredMenus: function () {
      function formatDate(posix_time) {
        return moment.unix(String(posix_time)).format('DD.MM.YYYY HH:mm')
      }
      return this.menus.filter(
        (m) => formatDate(m.posix_time).toUpperCase().indexOf(this.search.toUpperCase()) >= 0
      )
      .sort((a,b)=> -1 * ( a.posix_time - b.posix_time ));
    },
  },
  created: async function () {
    this.isLoading = true;
    const rs = await api.loadMenus();
    this.isLoading = false;
    this.menus = rs.sort((a, b) => (a.date < b.date ? -1 : 1));
  },
};
</script>

<style>
</style>