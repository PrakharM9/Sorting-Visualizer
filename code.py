import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

class SortingVisualizer:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("1200x700")
        self.root.configure(bg="#1a1a2e")
        self.array = []
        self.array_size = 50
        self.sorting = False
        self.speed = 50  # milliseconds
        self.algorithm = "Bubble Sort"
        self.colors = {
            'bg': '#1a1a2e',
            'canvas_bg': '#16213e',
            'unsorted': '#3b82f6',
            'comparing': '#fbbf24',
            'swapping': '#ef4444',
            'sorted': '#10b981',
            'text': '#ffffff',
            'button': '#6366f1',
            'button_hover': '#4f46e5'
        }
        
        self.setup_ui()
        self.generate_array()
        
    def setup_ui(self):
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(pady=10)
        
        title_label = tk.Label(
            title_frame, 
            text="🔢 Sorting Algorithm Visualizer",
            font=("Arial", 24, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        title_label.pack()
        control_frame = tk.Frame(self.root, bg=self.colors['bg'])
        control_frame.pack(pady=10, padx=20, fill='x')
        
        algo_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        algo_frame.pack(side='left', padx=10)
        
        tk.Label(algo_frame, text="Algorithm:", bg=self.colors['bg'], 
                fg=self.colors['text'], font=("Arial", 10, "bold")).pack()
        
        self.algo_menu = ttk.Combobox(
            algo_frame,
            values=["Bubble Sort", "Selection Sort", "Insertion Sort", "Quick Sort", "Merge Sort"],
            state="readonly",
            width=15
        )
        self.algo_menu.set("Bubble Sort")
        self.algo_menu.pack()

        speed_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        speed_frame.pack(side='left', padx=10)
        
        tk.Label(speed_frame, text="Speed (ms):", bg=self.colors['bg'],
                fg=self.colors['text'], font=("Arial", 10, "bold")).pack()
        
        self.speed_scale = tk.Scale(
            speed_frame,
            from_=1,
            to=200,
            orient='horizontal',
            bg=self.colors['bg'],
            fg=self.colors['text'],
            highlightthickness=0,
            troughcolor=self.colors['canvas_bg'],
            length=150
        )
        self.speed_scale.set(50)
        self.speed_scale.pack()
        
        size_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        size_frame.pack(side='left', padx=10)
        
        tk.Label(size_frame, text="Array Size:", bg=self.colors['bg'],
                fg=self.colors['text'], font=("Arial", 10, "bold")).pack()
        
        self.size_scale = tk.Scale(
            size_frame,
            from_=10,
            to=100,
            orient='horizontal',
            bg=self.colors['bg'],
            fg=self.colors['text'],
            highlightthickness=0,
            troughcolor=self.colors['canvas_bg'],
            command=self.update_array_size,
            length=150
        )
        self.size_scale.set(50)
        self.size_scale.pack()
        
        button_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        button_frame.pack(side='right', padx=10)
        
        self.start_btn = tk.Button(
            button_frame,
            text="▶ Start Sort",
            command=self.start_sorting,
            bg=self.colors['button'],
            fg=self.colors['text'],
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            relief='flat',
            cursor='hand2'
        )
        self.start_btn.pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="🔄 Random",
            command=self.generate_array,
            bg=self.colors['button'],
            fg=self.colors['text'],
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=5)

        example_frame = tk.Frame(self.root, bg=self.colors['bg'])
        example_frame.pack(pady=5)
        
        tk.Label(example_frame, text="Load Examples:", bg=self.colors['bg'],
                fg=self.colors['text'], font=("Arial", 10, "bold")).pack(side='left', padx=5)
        
        examples = [
            ("Reversed", self.load_reversed),
            ("Nearly Sorted", self.load_nearly_sorted),
            ("Few Unique", self.load_few_unique),
            ("Mountain", self.load_mountain)
        ]
        
        for name, cmd in examples:
            tk.Button(
                example_frame,
                text=name,
                command=cmd,
                bg=self.colors['canvas_bg'],
                fg=self.colors['text'],
                font=("Arial", 9),
                padx=10,
                pady=3,
                relief='flat',
                cursor='hand2'
            ).pack(side='left', padx=3)

        input_frame = tk.Frame(self.root, bg=self.colors['bg'])
        input_frame.pack(pady=5)
        
        tk.Label(input_frame, text="Custom Input (comma-separated):", 
                bg=self.colors['bg'], fg=self.colors['text'], 
                font=("Arial", 10, "bold")).pack(side='left', padx=5)
        
        self.custom_input = tk.Entry(input_frame, width=40, font=("Arial", 10))
        self.custom_input.pack(side='left', padx=5)
        
        tk.Button(
            input_frame,
            text="Load",
            command=self.load_custom_input,
            bg=self.colors['button'],
            fg=self.colors['text'],
            font=("Arial", 9, "bold"),
            padx=10,
            pady=3,
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=5)
        
        # Canvas for visualization
        self.canvas = tk.Canvas(
            self.root,
            bg=self.colors['canvas_bg'],
            highlightthickness=2,
            highlightbackground=self.colors['button']
        )
        self.canvas.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Info Panel
        info_frame = tk.Frame(self.root, bg=self.colors['bg'])
        info_frame.pack(pady=5)
        
        legend_items = [
            ("Unsorted", self.colors['unsorted']),
            ("Comparing", self.colors['comparing']),
            ("Swapping", self.colors['swapping']),
            ("Sorted", self.colors['sorted'])
        ]
        
        for text, color in legend_items:
            legend_frame = tk.Frame(info_frame, bg=self.colors['bg'])
            legend_frame.pack(side='left', padx=15)
            
            canvas = tk.Canvas(legend_frame, width=20, height=20, 
                             bg=self.colors['bg'], highlightthickness=0)
            canvas.create_rectangle(2, 2, 18, 18, fill=color, outline="")
            canvas.pack(side='left', padx=5)
            
            tk.Label(legend_frame, text=text, bg=self.colors['bg'],
                    fg=self.colors['text'], font=("Arial", 9)).pack(side='left')
    
    def generate_array(self):
        if not self.sorting:
            self.array = [random.randint(10, 400) for _ in range(self.array_size)]
            self.draw_array()
    
    def update_array_size(self, val):
        if not self.sorting:
            self.array_size = int(float(val))
            self.generate_array()
    
    def load_reversed(self):
        if not self.sorting:
            self.array = list(range(400, 10, -int(390/self.array_size)))[:self.array_size]
            self.draw_array()
    
    def load_nearly_sorted(self):
        if not self.sorting:
            self.array = list(range(10, 410, int(400/self.array_size)))[:self.array_size]

            for _ in range(3):
                i, j = random.sample(range(len(self.array)), 2)
                self.array[i], self.array[j] = self.array[j], self.array[i]
            self.draw_array()
    
    def load_few_unique(self):
        if not self.sorting:
            values = [100, 200, 300, 400]
            self.array = [random.choice(values) for _ in range(self.array_size)]
            self.draw_array()
    
    def load_mountain(self):
        if not self.sorting:
            mid = self.array_size // 2
            self.array = [10 + abs(mid - i) * (380 / mid) for i in range(self.array_size)]
            self.draw_array()
    
    def load_custom_input(self):
        if not self.sorting:
            try:
                input_text = self.custom_input.get()
                values = [int(x.strip()) for x in input_text.split(',') if x.strip()]
                
                if not values:
                    messagebox.showerror("Error", "Please enter valid numbers!")
                    return
                
                values = [max(10, min(400, v)) for v in values]
                
                self.array = values
                self.array_size = len(values)
                self.size_scale.set(len(values))
                self.draw_array()
                self.custom_input.delete(0, tk.END)
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid comma-separated numbers!")
    
    def draw_array(self, color_array=None):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 1160
        if canvas_height <= 1:
            canvas_height = 400
        
        bar_width = canvas_width / len(self.array)
        
        for i, value in enumerate(self.array):
            x0 = i * bar_width
            y0 = canvas_height
            x1 = (i + 1) * bar_width
            y1 = canvas_height - (value / 420 * canvas_height)
            
            if color_array:
                color = color_array[i]
            else:
                color = self.colors['unsorted']
            
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
    
    def start_sorting(self):
        if not self.sorting and self.array:
            self.sorting = True
            self.start_btn.config(state='disabled', text="⏸ Sorting...")
            self.speed = self.speed_scale.get()
            self.algorithm = self.algo_menu.get()
            
            self.root.after(10, self.sort_array)
    
    def sort_array(self):
        if self.algorithm == "Bubble Sort":
            self.bubble_sort()
        elif self.algorithm == "Selection Sort":
            self.selection_sort()
        elif self.algorithm == "Insertion Sort":
            self.insertion_sort()
        elif self.algorithm == "Quick Sort":
            self.quick_sort(0, len(self.array) - 1)
        elif self.algorithm == "Merge Sort":
            self.merge_sort(0, len(self.array) - 1)
        
        color_array = [self.colors['sorted']] * len(self.array)
        self.draw_array(color_array)
        
        self.sorting = False
        self.start_btn.config(state='normal', text="▶ Start Sort")
    
    def bubble_sort(self):
        n = len(self.array)
        for i in range(n - 1):
            for j in range(n - i - 1):
                color_array = [self.colors['unsorted']] * len(self.array)
                color_array[j] = self.colors['comparing']
                color_array[j + 1] = self.colors['comparing']
                
                for k in range(n - i, n):
                    color_array[k] = self.colors['sorted']
                
                self.draw_array(color_array)
                self.root.update()
                time.sleep(self.speed / 1000)
                
                if self.array[j] > self.array[j + 1]:
                    color_array[j] = self.colors['swapping']
                    color_array[j + 1] = self.colors['swapping']
                    self.draw_array(color_array)
                    self.root.update()
                    time.sleep(self.speed / 1000)
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
    
    def selection_sort(self):
        n = len(self.array)
        for i in range(n):
            min_idx = i
            color_array = [self.colors['unsorted']] * len(self.array)
            
            for k in range(i):
                color_array[k] = self.colors['sorted']
            
            for j in range(i + 1, n):
                color_array[j] = self.colors['comparing']
                color_array[min_idx] = self.colors['comparing']
                
                self.draw_array(color_array)
                self.root.update()
                time.sleep(self.speed / 1000)
                
                if self.array[j] < self.array[min_idx]:
                    color_array[min_idx] = self.colors['unsorted']
                    min_idx = j
                else:
                    color_array[j] = self.colors['unsorted']
            
            if min_idx != i:
                color_array[i] = self.colors['swapping']
                color_array[min_idx] = self.colors['swapping']
                self.draw_array(color_array)
                self.root.update()
                time.sleep(self.speed / 1000)
                
                self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
    
    def insertion_sort(self):
        for i in range(1, len(self.array)):
            key = self.array[i]
            j = i - 1
            
            while j >= 0 and self.array[j] > key:
                color_array = [self.colors['unsorted']] * len(self.array)
                
                for k in range(i):
                    color_array[k] = self.colors['sorted']
                
                color_array[j] = self.colors['comparing']
                color_array[j + 1] = self.colors['swapping']
                
                self.draw_array(color_array)
                self.root.update()
                time.sleep(self.speed / 1000)
                
                self.array[j + 1] = self.array[j]
                j -= 1
            
            self.array[j + 1] = key
    
    def quick_sort(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self.quick_sort(low, pi - 1)
            self.quick_sort(pi + 1, high)
    
    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1
        
        for j in range(low, high):
            color_array = [self.colors['unsorted']] * len(self.array)
            color_array[high] = self.colors['comparing']
            color_array[j] = self.colors['comparing']
            
            self.draw_array(color_array)
            self.root.update()
            time.sleep(self.speed / 1000)
            
            if self.array[j] < pivot:
                i += 1
                color_array[i] = self.colors['swapping']
                color_array[j] = self.colors['swapping']
                self.draw_array(color_array)
                self.root.update()
                time.sleep(self.speed / 1000)
                
                self.array[i], self.array[j] = self.array[j], self.array[i]
        
        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        return i + 1
    
    def merge_sort(self, left, right):
        if left < right:
            mid = (left + right) // 2
            self.merge_sort(left, mid)
            self.merge_sort(mid + 1, right)
            self.merge(left, mid, right)
    
    def merge(self, left, mid, right):
        left_part = self.array[left:mid + 1]
        right_part = self.array[mid + 1:right + 1]
        
        i = j = 0
        k = left
        
        while i < len(left_part) and j < len(right_part):
            color_array = [self.colors['unsorted']] * len(self.array)
            color_array[k] = self.colors['comparing']
            
            self.draw_array(color_array)
            self.root.update()
            time.sleep(self.speed / 1000)
            
            if left_part[i] <= right_part[j]:
                self.array[k] = left_part[i]
                i += 1
            else:
                self.array[k] = right_part[j]
                j += 1
            k += 1
        
        while i < len(left_part):
            self.array[k] = left_part[i]
            i += 1
            k += 1
        
        while j < len(right_part):
            self.array[k] = right_part[j]
            j += 1
            k += 1


if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()