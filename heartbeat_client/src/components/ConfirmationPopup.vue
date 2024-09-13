<template>
    <div v-show="showModel" class="model-container">
        <div class="container">
            <div><h5>Confirmation</h5></div>
            <hr>
            <div> <p>Did you want to delete this information ?</p> </div>
            <div class="model-footer">
                <button
                    class="btn btn-outline-primary"
                    @click="confirmSubmit"
                >Yes</button>
                <button
                    class="btn btn-outline-dark"
                    @click="close"
                >No</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ConfirmationPopup',
    props: {
        confirm: {
            type: Function,
            requried: true
        }
    },
    data(){
        return {
            showModel: false,
        }
    },
    methods: {
        openModel() {
            this.showModel = true
        },
        close() {
            this.showModel = false
        },
        confirmSubmit() {
            this.confirm();
            this.close();
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