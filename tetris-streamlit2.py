import streamlit as st
import streamlit.components.v1 as components

def main():
    st.set_page_config(page_title="2인용 테트리스", layout="wide")
    
    # CSS 스타일
    st.markdown("""
        <style>
        .stApp {
            background-color: #f0f0f0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 게임 타이틀
    st.title("2인용 테트리스 대결")
    
    # HTML/JavaScript 게임 컴포넌트
    game_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .game-container {
                display: flex;
                gap: 20px;
                justify-content: center;
                padding: 20px;
            }
            .player-container {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .player-board {
                border: 2px solid #333;
                background-color: rgba(17, 17, 17, 0.8);
            }
            .next-piece {
                border: 2px solid #333;
                background-color: rgba(17, 17, 17, 0.8);
                margin-top: 10px;
            }
            .info {
                text-align: center;
                color: #333;
            }
            .controls {
                margin-top: 10px;
                font-size: 0.8em;
            }
            #winner {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background-color: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 20px;
                border-radius: 10px;
                font-size: 24px;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="game-container">
            <div class="player-container">
                <h2>플레이어 1</h2>
                <canvas id="board1" class="player-board" width="200" height="400"></canvas>
                <canvas id="next1" class="next-piece" width="80" height="80"></canvas>
                <div class="info">
                    <p>점수: <span id="score1">0</span></p>
                    <div class="controls">
                        A D : 이동, W : 회전, S : 빠른 낙하
                    </div>
                </div>
            </div>
            <div class="player-container">
                <h2>플레이어 2</h2>
                <canvas id="board2" class="player-board" width="200" height="400"></canvas>
                <canvas id="next2" class="next-piece" width="80" height="80"></canvas>
                <div class="info">
                    <p>점수: <span id="score2">0</span></p>
                    <div class="controls">
                        ← → : 이동, ↑ : 회전, ↓ : 빠른 낙하
                    </div>
                </div>
            </div>
        </div>
        <div id="winner"></div>

        <script>
            const COLS = 10;
            const ROWS = 20;
            const BLOCK_SIZE = 20;
            const COLORS = [
                'cyan', 'blue', 'orange', 'yellow', 'green', 'purple', 'red'
            ];
            const SHAPES = [
                [[1,1,1,1]],
                [[1,1,1],[0,1,0]],
                [[1,1,1],[1,0,0]],
                [[1,1],[1,1]],
                [[1,1,0],[0,1,1]],
                [[0,1,1],[1,1,0]],
                [[1,1,1],[0,0,1]]
            ];

            class Tetris {
                constructor(boardCanvas, nextCanvas, opponent) {
                    this.canvas = boardCanvas;
                    this.ctx = this.canvas.getContext('2d');
                    this.nextCanvas = nextCanvas;
                    this.nextCtx = this.nextCanvas.getContext('2d');
                    this.grid = this.getEmptyGrid();
                    this.piece = this.getNewPiece();
                    this.nextPiece = this.getNewPiece();
                    this.score = 0;
                    this.gameOver = false;
                    this.opponent = opponent;
                }

                getEmptyGrid() {
                    return Array.from(
                        {length: ROWS}, () => Array(COLS).fill(0)
                    );
                }

                getNewPiece() {
                    const shapeIndex = Math.floor(Math.random() * SHAPES.length);
                    const color = COLORS[shapeIndex];
                    const shape = SHAPES[shapeIndex];
                    return {
                        x: Math.floor(COLS / 2) - Math.ceil(shape[0].length / 2),
                        y: 0,
                        shape,
                        color
                    };
                }

                draw() {
                    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                    this.drawGrid();
                    this.drawPiece();
                    this.drawGridLines();
                    this.drawNextPiece();
                }

                drawGrid() {
                    this.grid.forEach((row, y) => {
                        row.forEach((value, x) => {
                            if (value) {
                                this.ctx.fillStyle = COLORS[value - 1];
                                this.ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
                            }
                        });
                    });
                }

                drawPiece() {
                    this.piece.shape.forEach((row, y) => {
                        row.forEach((value, x) => {
                            if (value) {
                                this.ctx.fillStyle = this.piece.color;
                                this.ctx.fillRect((this.piece.x + x) * BLOCK_SIZE, (this.piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
                            }
                        });
                    });
                }

                drawGridLines() {
                    this.ctx.strokeStyle = '#333';
                    this.ctx.lineWidth = 0.5;
                    for (let x = 0; x <= COLS; x++) {
                        this.ctx.beginPath();
                        this.ctx.moveTo(x * BLOCK_SIZE, 0);
                        this.ctx.lineTo(x * BLOCK_SIZE, this.canvas.height);
                        this.ctx.stroke();
                    }
                    for (let y = 0; y <= ROWS; y++) {
                        this.ctx.beginPath();
                        this.ctx.moveTo(0, y * BLOCK_SIZE);
                        this.ctx.lineTo(this.canvas.width, y * BLOCK_SIZE);
                        this.ctx.stroke();
                    }
                }

                drawNextPiece() {
                    this.nextCtx.clearRect(0, 0, this.nextCanvas.width, this.nextCanvas.height);
                    this.nextCtx.fillStyle = this.nextPiece.color;
                    this.nextPiece.shape.forEach((row, y) => {
                        row.forEach((value, x) => {
                            if (value) {
                                this.nextCtx.fillRect(x * BLOCK_SIZE + 10, y * BLOCK_SIZE + 10, BLOCK_SIZE, BLOCK_SIZE);
                            }
                        });
                    });
                }

                moveDown() {
                    this.piece.y++;
                    if (this.checkCollision()) {
                        this.piece.y--;
                        this.lockPiece();
                        const linesCleared = this.clearLines();
                        if (linesCleared > 0) {
                            this.opponent.addRandomLine(linesCleared);
                        }
                        this.piece = this.nextPiece;
                        this.nextPiece = this.getNewPiece();
                        if (this.checkCollision()) {
                            this.gameOver = true;
                        }
                    }
                }

                moveLeft() {
                    this.piece.x--;
                    if (this.checkCollision()) {
                        this.piece.x++;
                    }
                }

                moveRight() {
                    this.piece.x++;
                    if (this.checkCollision()) {
                        this.piece.x--;
                    }
                }

                rotate() {
                    const rotated = this.piece.shape[0].map((val, index) =>
                        this.piece.shape.map(row => row[index]).reverse()
                    );
                    const previousShape = this.piece.shape;
                    this.piece.shape = rotated;
                    if (this.checkCollision()) {
                        this.piece.shape = previousShape;
                    }
                }

                checkCollision() {
                    return this.piece.shape.some((row, dy) => {
                        return row.some((value, dx) => {
                            let x = this.piece.x + dx;
                            let y = this.piece.y + dy;
                            return (
                                value &&
                                (y >= ROWS ||
                                x < 0 ||
                                x >= COLS ||
                                (this.grid[y] && this.grid[y][x]))
                            );
                        });
                    });
                }

                lockPiece() {
                    this.piece.shape.forEach((row, y) => {
                        row.forEach((value, x) => {
                            if (value) {
                                this.grid[this.piece.y + y][this.piece.x + x] = COLORS.indexOf(this.piece.color) + 1;
                            }
                        });
                    });
                }

                clearLines() {
                    let linesCleared = 0;
                    this.grid = this.grid.reduce((acc, row) => {
                        if (row.every(cell => cell)) {
                            linesCleared++;
                            acc.unshift(Array(COLS).fill(0));
                        } else {
                            acc.push(row);
                        }
                        return acc;
                    }, []);
                    if (linesCleared > 0) {
                        this.score += linesCleared * 100;
                    }
                    return linesCleared;
                }

                addRandomLine(count) {
                    for (let i = 0; i < count; i++) {
                        const newLine = Array(COLS).fill(0).map(() => Math.random() < 0.7 ? 0 : Math.floor(Math.random() * COLORS.length) + 1);
                        this.grid.shift();
                        this.grid.push(newLine);
                    }
                }

                reset() {
                    this.grid = this.getEmptyGrid();
                    this.piece = this.getNewPiece();
                    this.nextPiece = this.getNewPiece();
                    this.score = 0;
                    this.gameOver = false;
                }
            }

            // 게임 초기화
            let game1, game2;

            function initializeGames() {
                game1 = new Tetris(document.getElementById('board1'), document.getElementById('next1'), null);
                game2 = new Tetris(document.getElementById('board2'), document.getElementById('next2'), null);
                game1.opponent = game2;
                game2.opponent = game1;
            }

            function gameLoop() {
                if (!game1.gameOver) {
                    game1.moveDown();
                    game1.draw();
                    document.getElementById('score1').textContent = game1.score;
                }
                if (!game2.gameOver) {
                    game2.moveDown();
                    game2.draw();
                    document.getElementById('score2').textContent = game2.score;
                }
                if (game1.gameOver || game2.gameOver) {
                    let winner = game1.gameOver ? '플레이어 2' : '플레이어 1';
                    const winnerDisplay = document.getElementById('winner');
                    winnerDisplay.textContent = `${winner} 승리!`;
                    winnerDisplay.style.display = 'block';
                    setTimeout(() => {
                        winnerDisplay.style.display = 'none';
                        game1.reset();
                        game2.reset();
                        game1.draw();
                        game2.draw();
                        document.getElementById('score1').textContent = '0';
                        document.getElementById('score2').textContent = '0';
                        gameLoop();
                    }, 3000);
                } else {
                    setTimeout(gameLoop, 1000);
                }
            }

            // 키보드 이벤트 처리
            document.addEventListener('keydown', event => {
                if (!game1.gameOver) {
                    switch(event.keyCode) {
                        case 65: // A
                            game1.moveLeft();
                            break;
                        case 68: // D
                            game1.moveRight();
                            break;
                        case 83: // S
                            game1.moveDown();
                            break;
                        case 87: // W
                            game1.rotate();
                            break;
                    }
                    game1.draw();
                }
                if (!game2.gameOver) {
                    switch(event.keyCode) {
                        case 37: // Left arrow
                            game2.moveLeft();
                            break;
                        case 39: // Right arrow
                            game2.moveRight();
                            break;
                        case 40: // Down arrow
                            game2.moveDown();
                            break;
                        case 38: // Up arrow
                            game2.rotate();
                            break;
                    }
                    game2.draw();
                }
            });

            // 게임 시작
            window.onload = function() {
                initializeGames();
                game1.draw();
                game2.draw();
                gameLoop();
            };
        </script>
    </body>
    </html>
    """
    
    # HTML 컴포넌트를 Streamlit에 삽입
    components.html(game_html, height=800)
    
    # 게임 설명
    with st.expander("게임 설명"):
        st.markdown("""
        ### 조작 방법
        
        #### 플레이어 1
        - A: 왼쪽으로 이동
        - D: 오른쪽으로 이동
        - W: 블록 회전
        - S: 빠른 낙하
        
        #### 플레이어 2
        - ←: 왼쪽으로 이동
        - →: 오른쪽으로 이동
        - ↑: 블록 회전
        - ↓: 빠른 낙하
        
        ### 게임 규칙
        - 두 플레이어가 각각의 보드에서 테트리스를 플레이합니다.
        - 블록을 정렬하여 점수를 얻고, 한 플레이어가 게임 오버가 되면 다른 플레이어가 승리합니다.
        - 빠르게 떨어지는 블록을 적절히 조작하여 더 많은 점수를 획득하세요!
        """)
        
    # 추가적인 사용자 안내 메시지
    st.sidebar.header("도움말")
    st.sidebar.markdown("""
    - **게임 시작**: 페이지를 새로 고침하거나 앱을 열면 자동으로 시작됩니다.
    - **게임 종료**: 한 플레이어의 게임 오버 시, 승리 메시지가 표시됩니다.
    - **다시 시작**: 승리 메시지가 사라진 후 자동으로 게임이 다시 시작됩니다.
    """)

if __name__ == "__main__":
    main()
