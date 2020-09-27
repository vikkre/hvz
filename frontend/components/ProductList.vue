<template>
  <div class="container productListContainer">
    <div class="modal" v-bind:class="{'is-active': showModal}">
      <div class="modal-background"></div>
      <div class="modal-content">
        <article class="message is-primary">
          <div class="message-header">
            <p>{{modalHeader}}</p>
          </div>
          <div class="message-body mx-6">
            <p>{{modalText}}</p>
            <div class="columns">
              <div class="column is-8"></div>
              <div class="column">
                <a class="button" name="modal_ok" @click="modalOk">OK</a>
              </div>
              <div class="column">
                <a class="button" name="modal_cancel" @click="modalCancel">Cancel</a>
              </div>
            </div>
          </div>
        </article>
      </div>
    </div>
    <div
      style="display: unset; position: absolute; top: 0; left: 50%; transform: translate(-50%, 50%);"
      v-bind:style="{display: isLoading ? 'unset' : 'none'}"
    >
      <img src="../assets/loading.gif" />
    </div>
    <table v-if="!isLoading" class="table is-narrow is-hoverable has-background-light">
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
            <a class="button" @click="newProduct()" name="new_product">
              <span class="icon grow action">
                <i class="fas fa-plus"></i>
              </span>
            </a>
          </div>
        </th>
      </thead>
      <thead>
        <th>Product</th>
        <th>Amount</th>
        <th>Req.</th>
        <th></th>
        <th></th>
      </thead>
      <tbody>
        <tr v-for="p in this.filteredProducts" v-bind:key="p.id">
          <td name="product_name">{{p.name}}</td>
          <td>
            <input
              class="input"
              name="product_amount"
              type="number"
              v-model="p.amount"
              @change="changeAmount($event, p)"
            />
          </td>
          <td name="required_amount">{{p.required_amount}}</td>
          <td>
            <span class="icon grow action" name="edit_product" @click="editProduct(p)">
              <i class="fas fa-pen"></i>
            </span>
          </td>
          <td>
            <span class="icon grow action" name="delete_product" @click="deleteProduct(p)">
              <i class="fas fa-trash-alt"></i>
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import * as api from "../products_api.js";

export default {
  name: "ProductList",
  data: function() {
    return {
      products: [],
      isLoading: true,
      search: "",
      showModal: false,
      modalText: "Do your really want to delete the product xyz?",
      modalHeader: "Confirm Deletion",
      modalOkCallback: function() {}
    };
  },
  methods: {
    changeAmount: async function(event, product) {
      console.log(event, product);
      const newProduct = await api.saveProduct(product);
    },
    deleteProduct: async function(product) {
      this.modalText = `Do your really want to delete the product "${product.name}"?`;
      this.modalHeader = "Confirm Deletion";
      this.showModal = true;
      this.modalOkCallback = async function() {
        await api.deleteProduct(product.id);
        this.products.splice(this.products.indexOf(product), 1);
      };
    },
    editProduct: function(product) {
      this.$router.push({
        name: "productEdit",
        params: { product_id: product.id, origin: this.$router.currentRoute.fullPath }
      });
    },
    newProduct: function() {
      this.$router.push({
        name: "productEdit",
        params: { product_id: undefined, origin: this.$router.currentRoute.fullPath }
      });
    },
    modalOk: function() {
      this.modalOkCallback();
      this.showModal = false;
    },
    modalCancel: function() {
      this.showModal = false;
    }
  },
  created: async function() {
    this.isLoading = true;
    const ps = await api.loadProducts();
    this.isLoading = false;
    this.products = ps.sort((a, b) => (a.name < b.name ? -1 : 1));
  },
  computed: {
    filteredProducts: function() {
      return this.products.filter(
        p => p.name.toUpperCase().indexOf(this.search.toUpperCase()) >= 0
      );
    }
  }
};
</script>

<style scoped>
.productListContainer {
  padding: 0em 1em 1em 1em;
  margin-bottom: 2em;
}

table {
  table-layout: fixed;
}

th,
td {
  width: 10em;
}

td input {
  width: 4em;
  text-align: right;
}

th:nth-child(1),
td:nth-child(1) {
  width: 20em;
}

th:nth-child(2),
td:nth-child(2) {
  width: 5em;
}

th:nth-child(3),
td:nth-child(3) {
  width: 5em;
  text-align: right;
}

th:nth-child(4),
td:nth-child(4) {
  width: 3em;
  text-align: center;
}

th:nth-child(5),
td:nth-child(5) {
  width: 3em;
  text-align: center;
}

.action {
  cursor: pointer;
}
</style>