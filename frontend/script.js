const API_BASE = "http://localhost:8081/api";
let puzzle = [];
let solution = [];
let currentGrid = [];
let selectedCell = null;
let fixedCells = new Set();

function init() {
  renderBoard();
  createNumberPad();
  bindEvents();
  newGame();
}

function renderBoard() {
  const board = document.getElementById("board");
  board.innerHTML = "";
  
  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      const cell = document.createElement("div");
      cell.className = "cell";
      cell.dataset.row = r;
      cell.dataset.col = c;
      cell.addEventListener("click", () => selectCell(r, c));
      board.appendChild(cell);
    }
  }
}

function createNumberPad() {
  const pad = document.createElement("div");
  pad.className = "number-pad";
  pad.id = "numberPad";
  
  for (let i = 1; i <= 9; i++) {
    const btn = document.createElement("button");
    btn.textContent = i;
    btn.addEventListener("click", () => inputNumber(i));
    pad.appendChild(btn);
  }
  
  const clearBtn = document.createElement("button");
  clearBtn.className = "clear";
  clearBtn.textContent = "清除";
  clearBtn.addEventListener("click", () => inputNumber(0));
  pad.appendChild(clearBtn);
  
  document.body.appendChild(pad);
}

function bindEvents() {
  document.getElementById("btnNew").addEventListener("click", newGame);
  document.getElementById("btnCheck").addEventListener("click", checkAnswer);
  document.getElementById("btnHint").addEventListener("click", getHint);
  
  document.addEventListener("click", (e) => {
    const pad = document.getElementById("numberPad");
    if (!e.target.closest(".number-pad") && !e.target.closest(".cell")) {
      pad.classList.remove("show");
      selectedCell = null;
      document.querySelectorAll(".cell.selected").forEach(c => c.classList.remove("selected"));
    }
  });
  
  document.addEventListener("keydown", (e) => {
    if (selectedCell !== null) {
      if (e.key >= "1" && e.key <= "9") {
        inputNumber(parseInt(e.key));
      } else if (e.key === "Backspace" || e.key === "Delete") {
        inputNumber(0);
      }
    }
  });
}

function selectCell(row, col) {
  if (fixedCells.has(`${row},${col}`)) {
    return;
  }
  
  document.querySelectorAll(".cell.selected").forEach(c => c.classList.remove("selected"));
  
  const cell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
  cell.classList.add("selected");
  selectedCell = { row, col };
  
  const pad = document.getElementById("numberPad");
  const rect = cell.getBoundingClientRect();
  pad.style.left = `${rect.left}px`;
  pad.style.top = `${rect.bottom + 5}px`;
  pad.classList.add("show");
}

function inputNumber(num) {
  if (selectedCell === null) return;
  
  const { row, col } = selectedCell;
  currentGrid[row][col] = num;
  updateCell(row, col);
  
  const pad = document.getElementById("numberPad");
  pad.classList.remove("show");
  selectedCell = null;
  document.querySelectorAll(".cell.selected").forEach(c => c.classList.remove("selected"));
}

function updateCell(row, col) {
  const cell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
  const value = currentGrid[row][col];
  cell.textContent = value ? value : "";
  cell.classList.remove("hint");
}

function fillBoard(grid) {
  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      const cell = document.querySelector(`.cell[data-row="${r}"][data-col="${c}"]`);
      const value = grid[r][c];
      cell.textContent = value ? value : "";
      
      const isFixed = fixedCells.has(`${r},${c}`);
      cell.classList.toggle("fixed", isFixed);
      cell.classList.remove("selected", "hint");
    }
  }
}

function getCurrentGrid() {
  return currentGrid.map(row => [...row]);
}

function setMsg(text, isError = true) {
  const msg = document.getElementById("msg");
  msg.textContent = text;
  msg.style.color = isError ? "#e94560" : "#4ade80";
}

async function newGame() {
  const difficulty = document.getElementById("difficulty").value;
  
  try {
    const response = await fetch(`${API_BASE}/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ difficulty })
    });
    
    const data = await response.json();
    puzzle = data.puzzle;
    solution = data.solution;
    currentGrid = puzzle.map(row => [...row]);
    
    fixedCells.clear();
    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        if (puzzle[r][c] !== 0) {
          fixedCells.add(`${r},${c}`);
        }
      }
    }
    
    fillBoard(currentGrid);
    setMsg("", false);
  } catch (error) {
    setMsg("加载失败: " + error.message);
  }
}

async function checkAnswer() {
  const grid = getCurrentGrid();
  
  if (grid.some(row => row.some(v => v === 0))) {
    setMsg("请先填满所有空格再检查。");
    return;
  }
  
  try {
    const response = await fetch(`${API_BASE}/validate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ grid })
    });
    
    const data = await response.json();
    
    if (data.valid) {
      setMsg("恭喜，答案正确！", false);
    } else {
      setMsg(data.message || "存在错误，请修改。");
    }
  } catch (error) {
    setMsg("检查失败: " + error.message);
  }
}

async function getHint() {
  const grid = getCurrentGrid();
  
  try {
    const response = await fetch(`${API_BASE}/hint`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ puzzle: grid, solution })
    });
    
    const data = await response.json();
    
    if (data.hint) {
      const { row, col, value } = data.hint;
      currentGrid[row][col] = value;
      
      const cell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
      cell.textContent = value;
      cell.classList.add("hint");
      
      setMsg(`提示：位置 (${row + 1}, ${col + 1}) 应填 ${value}`, false);
    } else {
      setMsg(data.message || "没有可提示的空格。");
    }
  } catch (error) {
    setMsg("获取提示失败: " + error.message);
  }
}

init();
