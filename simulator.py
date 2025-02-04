import json
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

class RobotSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Robot Simulator")
        self.geometry("1000x800")
        
        # Configurações iniciais
        self.robot_type = tk.StringVar(value="Differential")
        self.time_factor = tk.DoubleVar(value=1.0)
        self.trajectory = []
        self.current_step = 0
        self.simulating = False
        self.robot = None
        
        # Carregar configurações
        self.load_config()
        
        # Criar interface
        self.create_widgets()
        self.create_menu()
        self.update_robot()
        
    def create_widgets(self):
        # Canvas para simulação
        self.canvas = tk.Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame de controle
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        # Controles de simulação
        ttk.Button(control_frame, text="Play", command=self.start_simulation).pack(pady=5)
        ttk.Button(control_frame, text="Pause", command=self.pause_simulation).pack(pady=5)
        ttk.Button(control_frame, text="Reset", command=self.reset_simulation).pack(pady=5)
        
        # Configurações de tempo
        ttk.Label(control_frame, text="Time Factor:").pack(pady=5)
        ttk.Scale(control_frame, from_=0.1, to=10, variable=self.time_factor, 
                 orient=tk.HORIZONTAL).pack(pady=5)
        
    def create_menu(self):
        menu_bar = tk.Menu(self)
        
        # Menu Robot
        robot_menu = tk.Menu(menu_bar, tearoff=0)
        robot_menu.add_radiobutton(label="Differential Robot", variable=self.robot_type,
                                  value="Differential", command=self.update_robot)
        robot_menu.add_radiobutton(label="Robot Like a Car", variable=self.robot_type,
                                  value="Car", command=self.show_car_message)
        menu_bar.add_cascade(label="Robot", menu=robot_menu)
        
        # Menu Trajectory
        trajectory_menu = tk.Menu(menu_bar, tearoff=0)
        trajectory_menu.add_command(label="Add Straight Line", command=self.add_straight_line)
        trajectory_menu.add_command(label="Add Circular Path", command=self.add_circular_path)
        menu_bar.add_cascade(label="Trajectory", menu=trajectory_menu)
        
        self.config(menu=menu_bar)
    
    def update_robot(self):
        if self.robot_type.get() == "Differential":
            self.robot = DifferentialRobot(wheel_distance=0.5, time_step=0.1)
            self.draw_robot()
    
    def show_car_message(self):
        messagebox.showinfo("Info", "Car-like robot implementation is coming soon!")
    
    def draw_robot(self):
        self.canvas.delete("robot")
        size = 20
        x, y = self.robot.x[-1], self.robot.y[-1]
        theta = self.robot.theta[-1]
        
        # Desenhar triângulo representando o robô
        points = [
            x + size * np.cos(theta),
            y + size * np.sin(theta),
            x + size * np.cos(theta + np.pi*2/3),
            y + size * np.sin(theta + np.pi*2/3),
            x + size * np.cos(theta - np.pi*2/3),
            y + size * np.sin(theta - np.pi*2/3)
        ]
        self.canvas.create_polygon(points, fill="blue", tags="robot")
    
    def add_straight_line(self):
        dialog = tk.Toplevel()
        dialog.title("Add Straight Line")
        
        ttk.Label(dialog, text="Distance (m):").grid(row=0, column=0)
        distance_entry = ttk.Entry(dialog)
        distance_entry.grid(row=0, column=1)
        
        ttk.Label(dialog, text="Speed (m/s):").grid(row=1, column=0)
        speed_entry = ttk.Entry(dialog)
        speed_entry.grid(row=1, column=1)
        
        def add_command():
            distance = float(distance_entry.get())
            speed = float(speed_entry.get())
            self.trajectory.append(('straight', distance, speed))
            dialog.destroy()
        
        ttk.Button(dialog, text="Add", command=add_command).grid(row=2, columnspan=2)
    
    def add_circular_path(self):
        dialog = tk.Toplevel()
        dialog.title("Add Circular Path")
        
        # Adicionar campos para raio, velocidade e direção
        # Implementação similar à add_straight_line
        
    def start_simulation(self):
        if not self.simulating:
            self.simulating = True
            self.run_simulation()
    
    def run_simulation(self):
        if self.current_step < len(self.trajectory) and self.simulating:
            command = self.trajectory[self.current_step]
            self.execute_command(command)
            self.current_step += 1
            delay = int(self.robot.dt * 1000 / self.time_factor.get())
            self.after(delay, self.run_simulation)
        else:
            self.simulating = False
    
    def execute_command(self, command):
        if command[0] == 'straight':
            distance, speed = command[1], command[2]
            time = distance / speed
            steps = int(time / self.robot.dt)
            vr = np.full(steps, speed)
            vl = np.full(steps, speed)
            self.robot.calculate_trajectory(vr, vl)
            self.draw_robot()
    
    def pause_simulation(self):
        self.simulating = False
    
    def reset_simulation(self):
        self.canvas.delete("all")
        self.robot = DifferentialRobot(wheel_distance=0.5, time_step=0.1)
        self.trajectory = []
        self.current_step = 0
        self.draw_robot()
    
    def load_config(self):
        try:
            with open("start.json", "r") as f:
                config = json.load(f)
                self.robot_type.set(config.get("robot_type", "Differential"))
                self.time_factor.set(config.get("time_factor", 1.0))
        except FileNotFoundError:
            pass
    
    def save_config(self):
        config = {
            "robot_type": self.robot_type.get(),
            "time_factor": self.time_factor.get()
        }
        with open("start.json", "w") as f:
            json.dump(config, f)
    
    def on_closing(self):
        self.save_config()
        self.destroy()

if __name__ == "__main__":
    app = RobotSimulator()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()