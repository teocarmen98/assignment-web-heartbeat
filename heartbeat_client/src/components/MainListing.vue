<template>
    <div>
        <h2>Url Listing</h2>
        <hr>
        <div class="header">
            <button
                type = "button"
                class = "btn btn-primary"
                title = "Create New Url"
                @click="openDetailPopup"
            > CREATE </button>
        </div>
        <div class="table-container">
            <table class="table">
                <thead>
                    <tr>
                        <th
                            v-for="(value, key) in schema"
                            :key="key"
                            :style="{width: value.width}"
                        > {{ value.label }}
                        </th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                        v-for="(item, index) in tableData" 
                        :key="index"
                    >
                        <td
                            v-for="(value, key) in schema"
                            :key="key"
                            :style="{ width: value.width}"
                            :class="color[item[key]]"
                        > {{ item[key] }}
                        </td>
                        <td
                            :style="{width: '200px'}">
                            <button
                                type="button"
                                class = "btn btn-primary btn-sm"
                                @click="editItem(item)"
                            >
                                Edit
                            </button>
                            <button
                                type="button"
                                class = "btn btn-danger btn-sm ml-2"
                                @click="deleteItem(item)"
                            >
                                Delete
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="footer">
            <span>Pages  -  <b>{{ currentPage }} / {{ totalPage }}</b></span>
            <select v-model="pageSize" @change="updatePageSize">
                <option v-for="(size, key) in pageSizes" :value="size" :key="key">{{ size }}</option>
            </select>
            <div class="button-container">
                <button @click='previosPage()' :disabled="currentPage === 1" class = "btn btn-primary btn-sm">Prvious</button>
                <button @click='nextPage()' :disabled="currentPage === totalPage" class = "btn btn-primary btn-sm">Next</button>
            </div>
        </div>
        <detail-popup
            ref="detailPopUp"
        >
        </detail-popup>
        <confirmation-popup
            ref="confirmationPopup"
            :confirm="confirmDelete"
        ></confirmation-popup>
        <error-popup
            ref="errorPopup"
            :message="errorMessage"
            :clear="clearError"
        ></error-popup>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import { mainListingSchema } from '@/schemas/MainListing';

import DetailPopup from './DetailPopup.vue';
import ErrorPopup from './ErrorPopup.vue'
import ConfirmationPopup from '@/components/ConfirmationPopup.vue';

export default {
    name: 'MainListing',
    components: {
        DetailPopup,
        ErrorPopup,
        ConfirmationPopup
    },
    data() {
        return {
            selectedItem: {},
            color: {
                'ACTIVE': 'text-success',
                'INACTIVE': 'text-danger'
            },
            pageSize: 10,
            pageSizes: [10,30,50]
        }
    },
    watch: {
        /* eslint-disable */
        errorMessage(newVal, oldVal) {
            if (newVal) this.$refs.errorPopup.openModal();
        }
    },
    async created() {
        await this.loadData();
    },
    mounted() {
        setInterval(() => {
            this.loadData();
        }, 2000);
    },
    computed: {
        ...mapState('mainListing', ['tableData', 'currentPage', 'totalPage']),
        ...mapState('detail', ['errorMessage']),
        schema() {
            return mainListingSchema
        }
    },
    methods: {
        ...mapActions('mainListing', ['loadData', 'setPageSize', 'setPage']),
        ...mapActions('detail', ['setId', 'setData','setEditMode', 'setCreateMode', 'deleteData', 'clearError']),
        openDetailPopup(){
            this.setCreateMode(true)
            this.$refs.detailPopUp.openModel();
        },
        editItem(item){
            this.setId(item?.id)
            this.setEditMode(true)
            this.setData()
            this.$refs.detailPopUp.openModel();
        },
        deleteItem(item){
            this.selectedItem = item
            this.$refs.confirmationPopup.openModel();
        },
        confirmDelete(){
            this.deleteData(this.selectedItem.id)
        },
        previosPage() {
            this.setPage({ 'currentPage': this.currentPage - 1})
        },
        nextPage() {
            this.setPage({ 'currentPage': this.currentPage + 1})
        },
        updatePageSize() {
            this.setPageSize({'limit': this.pageSize})
        }
    },
}
</script>

<style scoped>
.table-container {
    height: 750px;
    margin-top: 5px;
    overflow-y: auto;
    padding: 20px;
}
th {
    background-color: #D9D9D9;
}
.header {
    align-items:center;
    display: flex;
}
button {
    border: none;
    margin-left: 20px;
}
.button-container {
    display: flex;
    justify-content: flex-end;
    width: 80%;
}
td, th {
    text-align: left;
}
.footer {
    margin-top: 5px;
    margin-left: 20px;
    display: flex;
}
select {
    margin-left: 20px;
}
</style>