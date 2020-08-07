<template>
    <div v-text="get_value()" :class="get_cls()"></div>
</template>
<script>
    // import * as _ from 'lodash';
    export default {
        name: 'SudokuCell',
        props: {
            is_const: {default: false},
            value: {} ,
            pencil_marks: {default: () => Array()}
        },
        data: function () {
            return {
            }
        },
        methods: {
            get_value() {
                if (this.value > 0) {
                    return this.value
                }
                if (this.pencil_marks.length > 0) {
                    return this.pencil_marks.join(' ')
                }
                return ''
            },
            get_cls() {
                let str = ''
                if (this.is_const) {
                    str =  'pen'
                } else {
                    str = 'empty'
                }
                if (this.value === 0 && this.pencil_marks) {
                    str += ' pencil'
                }
                return str
            }
        },

    }
</script>
<style>
    .empty {
        color: blue;
        padding: 0;
        margin: 0;
        background-size: cover;
        height: 100%
    }

    .pencil {
        color: black;
        padding: 0;
        margin: 0;
        font-size: 20px;
        background-size: cover;
        height: 100%
    }

    .pen {
        color: red;
        background: darkgrey;
        padding: 0;
        margin: 0;
        background-size: cover;
        max-width: 100%; /* Maximum width */
        height: 100%
    }
</style>
