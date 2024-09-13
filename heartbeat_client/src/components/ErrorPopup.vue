<template>
    <div v-show="showModal" class="model-container">
        <div class="container">
            <div><h5>Error</h5></div>
            <hr>
            <p>{{ message }}</p>
            <div class="model-footer">
                <button
                    class="btn btn-outline-primary"
                    @click="close"
                >OK</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ErrorPopup',
    props: {
        message: {
            type: String,
            required: true,
            default: ''
        },
        clear: {
            type: Function,
            required: true
        }
    },
    data() {
        return {
            showModal: false,
        }
    },
    methods: {
        openModal() {
            this.showModal = true
        },
        close() {
            this.showModal = false
            this.clear();
        }
    }
}
</script>

<style scoped>
.model-container {
    background-color: #f0e6e686;
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    width: 100%;
    height: 100%;
}
.container {
    background-color: #f2e9e9;
    border-radius: 10px;
    padding: 15px 60px;
    display: flex;
    flex-direction: column;
    width: 60%;
}
.model-footer {
    display: flex;
    flex-direction: row;
    gap: 30px;
    justify-content: center;
}
</style>