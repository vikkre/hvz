<template>
    <section class="section pt-0 mb-4 has-background-light">
        <div class="control">
            <a class="button" name="finish" @click="finish()" :disabled="!canFinish"> Finish </a>
        </div>
        <div class="columns is-xmobile header pt-2">
            <div class="column">Product</div>
            <div class="column is-4">Needed/ Bought</div>
            <div class="column is-2 is-hidden-mobile has-text-centered">
                Req.
            </div>
        </div>
        <div
            v-for="p in this.neededProducts"
            :key="p.id"
            name="product_row"
            class="columns is-xmobile is-unselectable"
        >
            <div
                class="is-hidden-tablet"
                style="border: 0.5px dotted black"
            ></div>
            <div class="column">
                <div
                    class="icon grow"
                    @click="p.inCart = !p.inCart"
                    name="check"
                >
                    <i class="fas fa-check"></i>
                </div>
                <span
                    name="product"
                    class="grow"
                    v-bind:class="{ inCart: p.inCart }"
                    @click="p.inCart = !p.inCart"
                    >{{ p.name }}</span
                >
            </div>
            <div class="column is-4">
                <div
                    class="icon is-large grow"
                    name="decrease_bought"
                    @click="p.bought = Math.max(0, p.bought - 1)"
                >
                    <i class="fas fa-minus fa-lg"></i>
                </div>
                <input
                    class="is-size-5"
                    type="number"
                    min="0"
                    v-model="p.bought"
                    name="number_bought"
                />
                <div
                    class="icon is-large grow"
                    name="increase_bought"
                    @click="p.bought += 1"
                >
                    <i class="fas fa-plus fa-lg"></i>
                </div>
            </div>
            <div
                class="column is-2 has-text-centered is-hidden-mobile"
                name="required_amount"
            >
                {{ p.required_amount }}
            </div>
        </div>
    </section>
</template>

<script>
import * as api from "../products_api.js";

export default {
    name: "ShoppingList",
    data: function () {
        return {
            neededProducts: [],
        };
    },
    created: async function () {
        let ps = await api.loadProducts();
        ps = ps.filter((p) => p.needed_amount > 0);
        ps = ps.sort((a, b) => (a.name < b.name ? -1 : 1));
        ps = ps.map((p) =>
            Object.assign(p, { bought: p.needed_amount, inCart: false })
        );
        this.neededProducts = ps;
    },
    computed: {
      canFinish : function() {
        return (this.neededProducts.filter(p => p.inCart).length > 0) && this.$attrs.apiOnline
      }
    },
    methods: {
        finish: async function () {
            this.neededProducts
                .filter((editedProduct) => editedProduct.inCart)
                .forEach(async function (editedProduct) {
                    let dbProduct = await api.getProduct(editedProduct.id);
                    dbProduct.amount =
                        Number(dbProduct.amount) + Number(editedProduct.bought);
                    api.saveProduct(dbProduct);
                    editedProduct.bought = 0;
                });
        },
    },
};
</script>

<style>
.header {
    font-weight: bold;
}
.grow {
    cursor: pointer;
}
input {
    width: 2em;
}
.inCart {
    text-decoration: line-through;
}
</style>