import tkinter as tk
from tkinter import ttk, messagebox
import random

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.array = []
        self.original_array = []  # New: Store the original array
        self.canvas_width = 820
        self.canvas_height = 400
        self.bar_width = 0
        self.speed = 50
        self.is_sorting = False
        self.is_paused = False
        self.sorting_task = None
        self.comparisons = 0
        self.swaps = 0
        
        # Setup GUI
        self.setup_gui()
        self.generate_array()

    def setup_gui(self):
        # Control Frame
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)

        # Algorithm Selection
        ttk.Label(control_frame, text="Algorithm:").pack(side=tk.LEFT, padx=5)
        self.algo_var = tk.StringVar(value="Bubble Sort")
        algorithms = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"]
        algo_menu = ttk.Combobox(control_frame, textvariable=self.algo_var, values=algorithms, state="readonly")
        algo_menu.pack(side=tk.LEFT, padx=5)

        # Buttons
        ttk.Button(control_frame, text="Generate New Array", command=self.generate_array).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Start Sorting", command=self.start_sorting).pack(side=tk.LEFT, padx=5)
        self.pause_resume_button = ttk.Button(control_frame, text="Pause", command=self.toggle_pause_resume)
        self.pause_resume_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Stop", command=self.cancel_sorting).pack(side=tk.LEFT, padx=5)

        # Speed Scale
        ttk.Label(control_frame, text="Speed:").pack(side=tk.LEFT, padx=5)
        self.speed_scale = ttk.Scale(control_frame, from_=10, to=200, orient=tk.HORIZONTAL, command=self.update_speed)
        self.speed_scale.set(self.speed)
        self.speed_scale.pack(side=tk.LEFT, padx=5)

        # Custom Array Input
        custom_frame = ttk.Frame(self.root)
        custom_frame.pack(pady=5)
        ttk.Label(custom_frame, text="Custom Array (comma-separated):").pack(side=tk.LEFT, padx=5)
        self.custom_array_entry = ttk.Entry(custom_frame, width=50)
        self.custom_array_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(custom_frame, text="Set Custom Array", command=self.set_custom_array).pack(side=tk.LEFT, padx=5)

        # Canvas for visualization
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(pady=10)

        # Label to display array values
        self.array_label = ttk.Label(self.root, text="", font=("Arial", 10))
        self.array_label.pack(pady=5)

        # New: Label to display original array
        self.original_array_label = ttk.Label(self.root, text="", font=("Arial", 10))
        self.original_array_label.pack(pady=5)

        # Stats Frame
        self.stats_frame = ttk.Frame(self.root)
        self.stats_frame.pack(pady=5)
        self.comparisons_label = ttk.Label(self.stats_frame, text="Comparisons: 0", font=("Arial", 10))
        self.comparisons_label.pack(side=tk.LEFT, padx=10)
        self.swaps_label = ttk.Label(self.stats_frame, text="Swaps: 0", font=("Arial", 10))
        self.swaps_label.pack(side=tk.LEFT, padx=10)

    def update_speed(self, value):
        self.speed = int(float(value))

    def set_custom_array(self):
        if self.is_sorting:
            messagebox.showwarning("Warning", "Cannot set array while sorting is in progress.")
            return
        input_text = self.custom_array_entry.get().strip()
        try:
            # Parse comma-separated input into integers
            custom_array = [int(x.strip()) for x in input_text.split(",") if x.strip()]
            # Validate array size and values
            if len(custom_array) == 0:
                messagebox.showerror("Error", "Array cannot be empty.")
                return
            if len(custom_array) > 20:
                messagebox.showerror("Error", "Array size must not exceed 20 elements.")
                return
            if any(x < 10 or x > 300 for x in custom_array):
                messagebox.showerror("Error", "Array values must be between 10 and 300.")
                return
            self.array = custom_array
            self.original_array = custom_array.copy()  # New: Store copy of original array
            self.draw_bars()
            self.update_array_label()
            self.update_original_array_label()  # New: Update original array label
            self.is_paused = False
            self.pause_resume_button.config(text="Pause")
            self.sorting_task = None
            self.comparisons = 0
            self.swaps = 0
            self.update_stats()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Enter comma-separated integers (e.g., 50, 100, 30).")
            self.generate_array()

    def generate_array(self):
        if not self.is_sorting:
            input_text = self.custom_array_entry.get().strip()
            if input_text:
                self.set_custom_array()
            else:
                self.array = [random.randint(10, 300) for _ in range(20)]
                self.original_array = self.array.copy()  # New: Store copy of original array
                self.draw_bars()
                self.update_array_label()
                self.update_original_array_label()  # New: Update original array label
                self.is_paused = False
                self.pause_resume_button.config(text="Pause")
                self.sorting_task = None
                self.comparisons = 0
                self.swaps = 0
                self.update_stats()

    def update_array_label(self):
        array_str = "Current Arr: " + ", ".join(map(str, self.array))
        self.array_label.config(text=array_str)

    def update_original_array_label(self):  # New: Method to update original array label
        array_str = "Original Arr: " + ", ".join(map(str, self.original_array))
        self.original_array_label.config(text=array_str)

    def update_stats(self):
        self.comparisons_label.config(text=f"Comparisons: {self.comparisons}")
        self.swaps_label.config(text=f"Swaps: {self.swaps}")

    def draw_bars(self, compare=None, swap=None, sorted_indices=None):
        self.canvas.delete("all")
        self.bar_width = self.canvas_width // len(self.array)
        sorted_indices = sorted_indices or []

        for i, height in enumerate(self.array):
            x0 = i * self.bar_width
            y0 = self.canvas_height
            x1 = (i + 1) * self.bar_width
            y1 = self.canvas_height - height

            color = "blue"
            if i in sorted_indices:
                color = "green"
            elif compare and i in compare:
                color = "red"
            elif swap and i in swap:
                color = "yellow"

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        
        self.update_array_label()

    def toggle_pause_resume(self):
        if self.is_sorting:
            self.is_paused = not self.is_paused
            self.pause_resume_button.config(text="Resume" if self.is_paused else "Pause")
            if not self.is_paused and self.sorting_task:
                self.sorting_task()

    def start_sorting(self):
        if not self.is_sorting:
            if not self.array:
                messagebox.showerror("Error", "No array to sort. Generate or set a custom array.")
                return
            self.is_sorting = True
            self.is_paused = False
            self.pause_resume_button.config(text="Pause")
            self.comparisons = 0
            self.swaps = 0
            self.update_stats()
            algo = self.algo_var.get()
            if algo == "Bubble Sort":
                self.bubble_sort()
            elif algo == "Selection Sort":
                self.selection_sort()
            elif algo == "Insertion Sort":
                self.insertion_sort()
            elif algo == "Merge Sort":
                self.merge_sort(0, len(self.array) - 1, self.stop_sorting)
            elif algo == "Quick Sort":
                self.quick_sort(0, len(self.array) - 1, self.stop_sorting)

    def stop_sorting(self):
        self.is_sorting = False
        self.is_paused = False
        self.sorting_task = None
        self.pause_resume_button.config(text="Pause")
        self.draw_bars(sorted_indices=list(range(len(self.array))))
        self.update_stats()

    def cancel_sorting(self):
        if self.is_sorting:
            self.is_sorting = False
            self.is_paused = False
            self.sorting_task = None
            self.pause_resume_button.config(text="Pause")
            self.draw_bars()
            self.update_stats()

    def bubble_sort(self):
        def step(i, j):
            if not self.is_sorting or self.is_paused:
                self.sorting_task = lambda: step(i, j)
                return
            if i < len(self.array) - 1:
                if j < len(self.array) - i - 1:
                    self.comparisons += 1
                    self.update_stats()
                    self.draw_bars(compare=[j, j + 1])
                    if self.array[j] > self.array[j + 1]:
                        self.swaps += 1
                        self.update_stats()
                        self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                        self.draw_bars(swap=[j, j + 1])
                    self.root.after(self.speed, lambda: step(i, j + 1))
                else:
                    self.draw_bars(sorted_indices=[len(self.array) - i - 1])
                    self.root.after(self.speed, lambda: step(i + 1, 0))
            else:
                self.stop_sorting()
        step(0, 0)

    def selection_sort(self):
        def step(i, j, min_idx):
            if not self.is_sorting or self.is_paused:
                self.sorting_task = lambda: step(i, j, min_idx)
                return
            if i < len(self.array) - 1:
                if j < len(self.array):
                    self.comparisons += 1
                    self.update_stats()
                    self.draw_bars(compare=[j, min_idx])
                    if self.array[j] < self.array[min_idx]:
                        min_idx = j
                    self.root.after(self.speed, lambda: step(i, j + 1, min_idx))
                else:
                    if i != min_idx:
                        self.swaps += 1
                        self.update_stats()
                        self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
                        self.draw_bars(swap=[i, min_idx], sorted_indices=[i])
                    else:
                        self.draw_bars(sorted_indices=[i])
                    self.root.after(self.speed, lambda: step(i + 1, i + 2, i + 1))
            else:
                self.stop_sorting()
        step(0, 1, 0)

    def insertion_sort(self):
        def step(i, j, key):
            if not self.is_sorting or self.is_paused:
                self.sorting_task = lambda: step(i, j, key)
                return
            if i < len(self.array):
                if j >= 0 and self.array[j] > key:
                    self.comparisons += 1
                    self.update_stats()
                    self.draw_bars(compare=[j, j + 1])
                    self.swaps += 1
                    self.update_stats()
                    self.array[j + 1] = self.array[j]
                    self.draw_bars(swap=[j, j + 1])
                    self.root.after(self.speed, lambda: step(i, j - 1, key))
                else:
                    if j >= 0:
                        self.comparisons += 1
                        self.update_stats()
                    self.array[j + 1] = key
                    self.draw_bars(sorted_indices=[k for k in range(i + 1)])
                    self.root.after(self.speed, lambda: step(i + 1, i, self.array[i + 1] if i + 1 < len(self.array) else None))
            else:
                self.stop_sorting()
        if len(self.array) > 1:
            step(1, 0, self.array[1])

    def merge_sort(self, left, right, callback=lambda: None):
        def merge(l, m, r, merge_callback):
            left_arr = self.array[l:m + 1]
            right_arr = self.array[m + 1:r + 1]
            i = j = 0
            k = l

            def merge_step():
                nonlocal i, j, k
                if not self.is_sorting or self.is_paused:
                    self.sorting_task = merge_step
                    return
                if i < len(left_arr) and j < len(right_arr):
                    self.comparisons += 1
                    self.update_stats()
                    self.draw_bars(compare=[l + i, m + 1 + j])
                    if left_arr[i] <= right_arr[j]:
                        self.array[k] = left_arr[i]
                        i += 1
                    else:
                        self.array[k] = right_arr[j]
                        j += 1
                    self.swaps += 1
                    self.update_stats()
                    self.draw_bars(swap=[k])
                    k += 1
                    self.root.after(self.speed, merge_step)
                elif i < len(left_arr):
                    self.array[k] = left_arr[i]
                    self.swaps += 1
                    self.update_stats()
                    self.draw_bars(swap=[k])
                    i += 1
                    k += 1
                    self.root.after(self.speed, merge_step)
                elif j < len(right_arr):
                    self.array[k] = right_arr[j]
                    self.swaps += 1
                    self.update_stats()
                    self.draw_bars(swap=[k])
                    j += 1
                    k += 1
                    self.root.after(self.speed, merge_step)
                else:
                    merge_callback()

            merge_step()

        def merge_sort_step(l, r, step_callback):
            if not self.is_sorting or self.is_paused:
                self.sorting_task = lambda: merge_sort_step(l, r, step_callback)
                return
            if l < r:
                mid = (l + r) // 2
                def after_left():
                    self.merge_sort(mid + 1, r, lambda: merge(l, mid, r, step_callback))
                self.merge_sort(l, mid, after_left)
            else:
                step_callback()

        merge_sort_step(left, right, callback)

    def quick_sort(self, low, high, callback=lambda: None):
        def partition(l, h, part_callback):
            pivot = self.array[h]
            i = l - 1

            def partition_step(j):
                nonlocal i
                if not self.is_sorting or self.is_paused:
                    self.sorting_task = lambda: partition_step(j)
                    return
                if j < h:
                    self.comparisons += 1
                    self.update_stats()
                    self.draw_bars(compare=[j, h])
                    if self.array[j] <= pivot:
                        i += 1
                        self.array[i], self.array[j] = self.array[j], self.array[i]
                        self.swaps += 1
                        self.update_stats()
                        self.draw_bars(swap=[i, j])
                    self.root.after(self.speed, lambda: partition_step(j + 1))
                else:
                    self.array[i + 1], self.array[h] = self.array[h], self.array[i + 1]
                    self.swaps += 1
                    self.update_stats()
                    self.draw_bars(swap=[i + 1, h])
                    part_callback(i + 1)

            partition_step(l)

        def quicksort_step(l, h, qs_callback):
            if not self.is_sorting or self.is_paused:
                self.sorting_task = lambda: quicksort_step(l, h, qs_callback)
                return
            if l < h:
                def after_partition(pi):
                    self.draw_bars(sorted_indices=[pi])
                    def after_left():
                        self.quick_sort(pi + 1, h, qs_callback)
                    self.quick_sort(l, pi - 1, after_left)
                partition(l, h, after_partition)
            else:
                qs_callback()

        quicksort_step(low, high, callback)

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()