<template>
  <section class="section">
    <div class="field">
      <label class="label">Product name</label>
      <div class="control">
        <input class="input" name="product_name" v-model="product.name" type="text" placeholder="e.g. Milk" />
      </div>
    </div>

    <div class="field">
      <label class="label">Amount on stock</label>
      <div class="control">
        <input class="input" name="product_amount" v-model="product.amount" type="number" placeholder="0" />
      </div>
    </div>

    <div class="field">
      <label class="label">Required amount</label>
      <div class="control">
        <input class="input" name="product_required_amount" v-model="product.required_amount" type="number" placeholder="0" />
      </div>
    </div>

    <div class="field is-grouped">
      <div class="control">
        <button class="button is-link action grow" name="save" @click="doSave()">Save</button>
      </div>
      <div class="control">
        <button class="button is-link is-light action grow" name="cancel" @click="doCancel()">Cancel</button>
      </div>
    </div>
  </section>
</template>

<script>
import * as api from "../products_api.js";

export default {
  name: "ProductEdit",
  props: ["product_id", "origin"],
  data: function() {
    return {
      product: {}
    };
  },
  methods: {
    doSave: async function() {
      if (this.product_id) {
        await api.saveProduct(this.product);
      } else {
        await api.insertProduct(this.product);
      }
      this.$router.push(this.origin);
    },
    doCancel: function() {
      this.$router.push(this.origin);
    }
  },
  created: async function() {
    if (this.product_id) {
      this.product = await api.getProduct(this.product_id);
    } else {
      this.product = { name: "", amount: 0, required_amount: 0 };
    }
  }
};
</script>

<style scoped>
.action {
  cursor: pointer;
}
</style>