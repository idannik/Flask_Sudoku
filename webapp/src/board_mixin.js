// import Vue from 'vue'


// define a mixin object
export default {
    methods: {
        get_row: function (square, cell) {
            return Math.floor(square / 3) * 3 + Math.floor(cell / 3)
        },
        get_col: function (square, cell) {
            return (square % 3) * 3 + cell % 3;
        }
    }
}
