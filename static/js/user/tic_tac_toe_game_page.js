let board = {
  0: '', 1: '', 2: '',
  3: '', 4: '', 5: '',
  6: '', 7: '', 8: '',
  }
  
  let myTurn = false
  let playerLetter = ""
  const opponentTxtElm = document.getElementById("opponent-txt")
  const turnElm = document.getElementById("tic_tac_toe_turn")
  const boxes = document.getElementsByClassName("tic_tac_toe_box")
  Array.from(boxes).forEach((elm, i) => {
      elm.addEventListener("click", e => {
          if(myTurn && !elm.innerHTML && !elm.getAttribute("player")){
              board[i] = playerLetter
              ws.send(JSON.stringify({
                  event: 'boardData_send',
                  board: board,
              }))
              addPlayerLetter(elm) 
              myTurn =false
          }
      })            
  })

  function addPlayerLetter(element, player=playerLetter) {
      element.innerHTML = `<p class="player-letter" >${player}</p>`
      element.setAttribute("player", player)
      setTimeout(() => {
          element.children[0].classList.add("active")
      }, 1);
  }
  

  function resetBoard() {
      Array.from(boxes).forEach(elm => {
          elm.innerHTML = ``
          elm.setAttribute("player", "")
     
      })
  }
  function updateBoard(boardData) {
      Array.from(boxes).forEach((elm,i ) => {
          if(boardData[i] != "" && !elm.getAttribute("player")){
              addPlayerLetter(elm, boardData[i])
          }
      })
  }

  // const ws = new WebSocket("ws://127.0.0.1:8000/ws/tic_tac_toe/game/{{room.uid}}/")
  // const ws = new WebSocket("ws://127.0.0.1:8000/user/tic_tac_toe/ws/game/{{room.uid}}/")
  // const ws = new WebSocket("ws://{{current_site}}/ws/tic_tac_toe/game/{{room.uid}}/")


  ws.onopen = e => {
      console.log(e)
  }

  ws.onmessage = e => {
      console.log(e)
      const data = JSON.parse(e.data)
      if(data.event == "show_error"){
          Swal.fire({
              icon: 'error',
              title: data.error,
              
          }).then(e => window.location = '/')
      }
      else if(data.event == "game_start"){
          board = data.board
          myTurn = data.myTurn
          playerLetter = data.myTurn? "X": "O"
          resetBoard()
          turnElm.innerHTML = data.myTurn? "Your Turn": "Opponent's Turn"
          opponentTxtElm.innerHTML = "Opponent Joined"
          setTimeout(() => {
              Swal.close()
          }, 500);
      }
      else if(data.event == "boardData_send"){
          board = data.board
          myTurn = data.myTurn
          updateBoard(board)
          turnElm.innerHTML = data.myTurn? "Your Turn": "Opponent's Turn"
      }
      else if(data.event == "won"){
          board = data.board
          myTurn = data.myTurn
          updateBoard(board)
          turnElm.innerHTML = data.winner == playerLetter? "You Won": "You Lost"
          setTimeout(() => {
              
              Swal.fire({
                  icon:  data.winner == playerLetter ?'success': "error",
                  title:  data.winner == playerLetter ?'You Won': "You Lost",
                  confirmButtonText: "Restart"
              }).then(e =>  ws.send(JSON.stringify({event: 'restart',})))
          }, 400);

      }

      else if(data.event == "draw"){
          board = data.board
          myTurn = data.myTurn
          updateBoard(board)
          turnElm.innerHTML = "Draw"
          setTimeout(() => {
              Swal.fire({
                  icon:  "info",
                  title:  "Draw",
                  confirmButtonText: "Restart"
              }).then(e =>  ws.send(JSON.stringify({event: 'restart',})))
          }, 400);

      }
      else if(data.event == "opponent_left"){
          board = data.board
          myTurn = data.myTurn
          resetBoard()
          turnElm.innerHTML = "Opponent Left"
          opponentTxtElm.innerHTML = "waiting to join... (Opponent)"

          setTimeout(() => {
              Swal.fire({
                  icon:  "info",
                  title:  "Opponent Left",
                  confirmButtonText: "Ok"
              })
          }, 400);

      }
  
    }