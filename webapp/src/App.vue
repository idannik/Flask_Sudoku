<template>
  <div id="main_app">
    <div class="container-fluid">
      <div class="row">
        <div class="col-lg-3">
          <div class="row">
            <div>
              soduko
              <input type="number" :value="board_id" @change="e=> board_id = e.target.value"/>
            </div>
          </div>
          <div class="row">
            <button type="button" class="btn btn-secondary btn-lg" id="load-btn"
                    @click="load_board()">Load
            </button>
          </div>
          <div class="row mt-5">
            <div class="col-md-6 bg-info pt-3">
              <div id="suggester  pt-5">
                <button
                    type="button"
                    class="btn btn-light btn-lg mt-1"
                    id="fill-pencil-marks-btn"
                    @click="fill_pencil_marks()"
                >fill pencil marks
                </button>
                <button
                    type="button"
                    class="btn btn-dark btn-lg mt-1"
                    id="suggest-btn"
                    @click="get_next_step()"
                >Suggest next move
                </button>
                <div id="reason">reason
                  <div v-text="reason"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-6">
          <div class="boards">
            <div class="board" id="sudoku0">
              <div class="square" v-for="(n,i) in 9" :key="i">
                <div class="cell" tabindex="0" v-for="(m,j) in 9" :key="j">
                  <SudokuCell :pencil_marks="get_pencil_marks(i, j)" :value="get_value(i, j)"
                              :is_const="get_const(i, j)" :is_selected="is_selected(i, j)"/>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import board_mixin from "./board_mixin";
// import * as _ from 'lodash';
import SudokuCell from "./SudokuCell";

export default {
  name: "MainApp",
  components: {SudokuCell},
  data: function () {
    return {
      board: Array(9).fill(0).map(() => Array(9).fill(0)),
      pencil_marks: Array(9).fill(0).map(() => Array(9).fill([])),
      is_const: Array(9).fill(0).map(() => Array(9).fill(false)),
      board_id: 3400,
      reason: 'no_reason',
      selected_pos: null
    };
  },
  methods: {
    is_selected: function (square, cell) {
      {
        const row = this.get_row(square, cell)
        const col = this.get_col(square, cell)
        return this.selected_pos && this.selected_pos[0]===row && this.selected_pos[1]===col
      }
    },

    get_value: function (square, cell) {
      {
        const row = this.get_row(square, cell)
        const col = this.get_col(square, cell)

        return this.board[row][col]
      }
    },

    get_pencil_marks: function (square, cell) {
      {
        const row = this.get_row(square, cell)
        const col = this.get_col(square, cell)

        return this.pencil_marks[row][col]
      }
    },

    get_const: function (square, cell) {
      {
        const row = this.get_row(square, cell)
        const col = this.get_col(square, cell)

        return this.is_const[row][col]
      }
    },

    load_board: async function () {
      const url = 'http://127.0.0.1:5000' + '/get_board/' + this.board_id
      const res = await fetch(url, {
        mode: 'cors',
        credentials: 'include',
      }).then(res => res.json())
      this.board = res['board']
      let new_is_const = Array(9).fill(0).map(() => Array(9))
      for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
          new_is_const[i][j] = this.board[i][j] > 0
        }
      }
      this.is_const = new_is_const
      this.pencil_marks = Array(9).fill(0).map(() => Array(9).fill([]))

    },

    fill_pencil_marks: async function () {
      const url = 'http://127.0.0.1:5000' + '/get_pencil_marks'
      const res = await fetch(url, {
        method: 'GET',
        mode: 'cors',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(res => res.json())
      this.pencil_marks = res['options']
      console.log(this.pencil_marks)


    },

    get_next_step: async function () {
      const url = 'http://127.0.0.1:5000' + '/get_next_step'
      const res = await fetch(url, {
        method: 'GET',
        credentials: 'include',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(res => res.json())
      const reason = res['reason']
      if (reason === 'lone_single') {

        this.sign_lone_single(res)
      }

    },

    sign_lone_single: function (json) {
      console.log(json)

    }

  },
  mixins: [board_mixin]
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.boards {
  display: grid;
  grid-template-columns: repeat(2, 50%);
  gap: 3px;

}

.board {
  display: grid;
  grid-template-columns: repeat(3, 300px);
  grid-template-rows: repeat(3, 300px);
}

.square {
  display: grid;
  border: black solid;
  grid-template-columns: repeat(3, 33%);
  grid-template-rows: repeat(3, 33%);
}

.cell {
  border: black 1px solid;
  font-family: monospace;
  text-align: center;
  font-size: 60px;
  padding: 0;
  margin: 0;
  background-size: cover;
  max-width: 100%; /* Maximum width */


}
</style>
