<template>
    <div v-show="showModel" class="model-container">
        <div class="container">
            <h3>URL Details</h3>
            <div class="form-group">
                <div class="col-md sub-form-group">
                    <label class="form-label"> Please enter URL </label>
                    <input
                        class="form-control"
                        :disabled="!canEdit"
                        type="text"
                        v-model="detailData.url"
                        @input="$emit('update:modelValue', $event.target.value)"
                    />
                </div>
            </div>
            <div class="model-footer">
                <button
                    class="btn btn-primary"
                    :disabled="!detailData.url || error"
                    @click="submit"
                >OK</button>
                <button
                    class="btn btn-outline-primary"
                    @click="close"
                >Close</button>
            </div>
        </div>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
    name: 'DetailPopup',
    props: {

    },
    data() {
        return {
            showModel: false,
            error: false,
        }
    },
    computed: {
        ...mapState('detail', ['detailData', 'editMode', 'createMode', 'newData']),
        canEdit(){
            return this.editMode || this.createMode
        }
    },
    watch: {
        'detailData.url'(newVal, oldVal) {
            if(newVal !== oldVal) this.updateNewValue({'url': newVal})
            this.checkValidation(newVal)
        }
    },
    methods: {
        ...mapActions('detail', ['setId', 'submitData', 'setEditMode', 'setCreateMode', 'updateNewValue',
            'clearData'
        ]),

        openModel() {
            this.showModel = true
        },
        submit() {
            this.submitData();
            this.showModel = false
        },
        close() {
            this.showModel = false
            this.clearData('detailData')
            this.clearData('newData')
            this.setCreateMode(false)
            this.setEditMode(false)
            this.setId('')
        },
        checkValidation(value){
            const regex1 = new RegExp("((http|https)://)"+"[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}"+"\\.[a-z]{2,6}"+"([-a-zA-Z0-9@:%._\\+~#?&//=]*)")
            const regex2 = new RegExp("((http|https)://(www)?)"+"[0-9@:%._\\+~#?&//=]{2,256}"+"([-a-zA-Z0-9@:%._\\+~#?&//=]*)")
            if((regex1.test(value) || regex2.test(value)) && !/\s/.test(value)) this.error = false
                else this.error = true
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