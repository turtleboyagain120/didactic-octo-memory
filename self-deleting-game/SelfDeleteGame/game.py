import tkinter as tk
import random
import webbrowser
import shutil
import os
import sys
from pathlib import Path

class SelfDeleteGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Catch Flags - Python Edition")
        self.root.geometry("500x600")
        self.root.configure(bg='#4ecdc4')
        
        self.score = 0
        self.width = 400
        self.height = 400
        self.game_running = True
        
        self.score_label = tk.Label(self.root, text="Score: 0/10", font=("Arial", 20), bg='#4ecdc4', fg='white')
        self.score_label.pack(pady=20)
        
        self.message = tk.Label(self.root, text="Click flags! Catch 10 to win.", font=("Arial", 16), bg='#4ecdc4', fg='white')
        self.message.pack()
        
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg='white', highlightthickness=5, highlightbackground='#ff6b6b')
        self.canvas.pack(pady=20)
        self.canvas.bind("<Button-1>", self.on_click)
        
        self.flags = []
        self.spawn_flag()
        self.move_loop()
        
    def spawn_flag(self):
        if self.score >= 10 or not self.game_running:
            return
            
        x = random.randint(20, self.width-70)
        y = random.randint(20, self.height-70)
        flag_id = self.canvas.create_rectangle(x, y, x+50, y+50, fill='#8b5cf6', outline='white', width=3, tags='flag')
        self.canvas.tag_bind(flag_id, "<Button-1>", lambda e: self.catch_flag(flag_id))
        
        # Auto remove
        self.root.after(3000, lambda: self.remove_flag(flag_id))
        
    def catch_flag(self, flag_id):
        self.canvas.delete(flag_id)
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}/10")
        
        if self.score >= 10:
            self.win()
        else:
            self.spawn_flag()
            
    def remove_flag(self, flag_id):
        if self.canvas.find_withtag(flag_id):
            self.canvas.delete(flag_id)
            
    def on_click(self, event):
        self.message.config(text="Missed! Try again!")
        self.root.after(1000, lambda: self.message.config(text=f"Score: {self.score}/10"))
        
    def win(self):
        self.game_running = False
        self.message.config(text="🎉 YOU WON! 🎉", fg='green', font=("Arial", 24, "bold"))
        
        # Rickroll
        webbrowser.open('https://youtu.be/dQw4w9WgXcQ')
        
        # Self delete
        self.root.after(2000, self.self_destruct)
        
    def self_destruct(self):
        if tk.messagebox.askyesno("Delete Game", "Delete all game files?"):
            try:
                # Backup current dir
                backup = Path(__file__).parent / "backup.zip"
                shutil.make_archive(str(backup), 'zip', Path(__file__).parent)
                tk.messagebox.showinfo("Backup", f"Backup saved: {backup}")
                
                # Delete game dir (Windows)
                import subprocess
                subprocess.Popen(['powershell', '-Command', 'Remove-Item -Recurse -Force "C:\\Users\\turtl\\Desktop\\SelfDeleteGame"'], 
                               creationflags=subprocess.CREATE_NO_WINDOW)
                self.root.destroy()
                sys.exit()
            except:
                tk.messagebox.showerror("Delete Failed", "Manual delete needed.")
                
    def move_loop(self):
        if self.game_running:
            self.root.after(100, self.move_loop)
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = SelfDeleteGame()
    game.run()

