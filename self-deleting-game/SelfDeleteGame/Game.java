import java.util.*;
import java.io.*;

public class Game {
    private static int score = 0;
    private static final Random rand = new Random();
    private static Scanner scanner = new Scanner(System.in);
    private static boolean gameRunning = true;
    
    public static void main(String[] args) {
        System.out.println("=== Java Self-Delete Game ===");
        System.out.println("Catch flags by guessing coords! Score 10/10.");
        
        Timer timer = new Timer();
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                if (gameRunning && score < 10) {
                    spawnFlag();
                }
            }
        }, 0, 3000);
        
        while (gameRunning) {
            System.out.print("\nEnter flag coords (x y) or 'q' quit: ");
            if (scanner.hasNext()) {
                String input = scanner.nextLine().trim();
                if (input.equalsIgnoreCase("q")) break;
                
                String[] parts = input.split(" ");
                if (parts.length == 2) {
                    try {
                        int x = Integer.parseInt(parts[0]);
                        int y = Integer.parseInt(parts[1]);
                        checkHit(x, y);
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid coords!");
                    }
                }
            }
        }
        
        scanner.close();
    }
    
    static int flagX, flagY;
    
    static void spawnFlag() {
        flagX = rand.nextInt(10);
        flagY = rand.nextInt(10);
        System.out.printf("New flag at secret (%d,%d)! Width/Height=10.\n", flagX, flagY);
    }
    
    static void checkHit(int guessX, int guessY) {
        if (Math.abs(guessX - flagX) <= 1 && Math.abs(guessY - flagY) <= 1) {
            score++;
            System.out.printf("HIT! Score: %d/10\n", score);
            if (score >= 10) {
                win();
            }
        } else {
            System.out.println("Miss! Try again.");
        }
    }
    
    static void win() {
        gameRunning = false;
        System.out.println("\n🎉 YOU WON! 🎉");
        
        // Rickroll
        try {
            Runtime.getRuntime().exec(new String[]{"cmd", "/c", "start", "https://youtu.be/dQw4w9WgXcQ"});
        } catch (IOException e) {
            System.out.println("Rickroll: https://youtu.be/dQw4w9WgXcQ");
        }
        
        // Self-delete
        System.out.print("Delete game files? (y/n): ");
        String del = scanner.nextLine();
        if (del.equalsIgnoreCase("y")) {
            selfDestruct();
        }
    }
    
    static void selfDestruct() {
        try {
            // Backup
            File backup = new File("SelfDeleteGame_backup.zip");
            // Zip logic simplified
            
            // Windows delete
            ProcessBuilder pb = new ProcessBuilder("cmd", "/c", "rmdir", "/s", "/q", ".");
            pb.directory(new File("C:\\Users\\turtl\\Desktop\\SelfDeleteGame"));
            pb.start();
            System.out.println("Files deleted! 💥");
        } catch (Exception e) {
            System.out.println("Manual delete: rmdir /s SelfDeleteGame");
        }
        System.exit(0);
    }
}

