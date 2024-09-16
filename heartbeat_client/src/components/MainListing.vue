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
                            :style="{'max-width': value.maxWidth}"
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
                            :style="{ 'max-width': value.maxWidth,'word-wrap': 'break-word', 'text-align': value.textAlign ?? 'center' }"
                            :class="[color[item[key]], value.fontWeight ?? 'normal-text']"
                        > 
                            <div v-if="key !== 'status'">
                                {{ item[key] }}
                            </div>
                            <div v-else-if="key === 'status'">
                                <svg v-if="item[key]" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-circle-fill" viewBox="0 0 16 16">
                                    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                                </svg>
                                <svg v-if="!item[key]" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-circle-fill" viewBox="0 0 16 16">
                                    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4m.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2"/>
                                </svg>
                            </div>
                        </td>
                        <td
                            :style="{width: '200px'}">
                            <div class="d-flex">
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
                            </div>
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
            <div class="footer-button">
                <button @click='previosPage()' :disabled="currentPage === 1" class = "btn btn-primary btn-sm">Previous</button>
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
                true: 'text-success',
                false: 'text-danger'
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
    max-height: 650px;
    height: 650px;
    margin-top: 10px;
    overflow-y: auto;
    padding: 0px 20px;
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
thead {
    position: sticky;
    top: 0;
}
.footer {
    margin-top: 5px;
    margin-left: 20px;
    display: flex;
}
.footer-button {
    margin-left: auto;
    margin-right: 50px;
    display: flex;
}
select {
    margin-left: 20px;
}
</style>