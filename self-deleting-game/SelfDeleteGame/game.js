class SelfDeleteGame {
  constructor() {
    this.score = 0;
    this.gameArea = document.getElementById('gameArea');
    this.scoreValue = document.getElementById('scoreValue');
    this.message = document.getElementById('message');
    this.gameRunning = true;
    this.init();
  }

  init() {
    this.gameArea.addEventListener('click', (e) => this.handleClick(e));
    this.spawnFlag();
    this.gameLoop();
  }

  spawnFlag() {
    if (this.score >= 10 || !this.gameRunning) return;
    
    const flag = document.createElement('div');
    flag.className = 'flag';
    flag.style.left = Math.random() * (350) + 'px';
    flag.style.top = Math.random() * (350) + 'px';
    
    flag.addEventListener('click', (e) => {
      e.stopPropagation();
      this.catchFlag(flag);
    });
    
    this.gameArea.appendChild(flag);
    
    // Remove after 3s
    setTimeout(() => {
      if (flag.parentNode) flag.remove();
    }, 3000);
  }

  catchFlag(flag) {
    flag.remove();
    this.score++;
    this.scoreValue.textContent = this.score;
    
    if (this.score >= 10) {
      this.win();
    } else {
      this.spawnFlag();
    }
  }

  handleClick() {
    // Miss penalty (fun)
    this.message.textContent = 'Missed! Keep trying!';
    setTimeout(() => {
      this.message.textContent = `Score: ${this.score}/10`;
    }, 1000);
  }

  win() {
    this.gameRunning = false;
    this.message.innerHTML = '<span class="won">YOU WON!</span>';
    
    // Rickroll
    window.open('https://youtu.be/dQw4w9WgXcQ', '_blank');
    
    // Self-delete (save files first!)
    setTimeout(() => {
      if (confirm('Delete game files?')) {
        alert('Downloading backup... (save your code!)');
        // Node would rm -rf; browser limited
        document.body.innerHTML = '<h1>Rickrolled & Deleted! 💥</h1>';
      }
    }, 2000);
  }

  gameLoop() {
    if (this.gameRunning) {
      setTimeout(() => this.gameLoop(), 100);
    }
  }
}

// Start
new SelfDeleteGame();

