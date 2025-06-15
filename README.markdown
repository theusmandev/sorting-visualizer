# Sorting Algorithm Visualizer

Welcome to the **Sorting Algorithm Visualizer**, a Python-based tool that brings sorting algorithms to life through interactive visualizations. Built with Tkinter, this project lets you see how Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, and Quick Sort work, step by step, with animated bars and real-time statistics. Whether you're a student learning algorithms, a developer revisiting fundamentals, or just curious about how sorting works, this tool makes it engaging and intuitive.

## Features

- **Interactive GUI**: Visualize sorting with a Tkinter-based interface showing bars that represent array elements.
- **Supported Algorithms**:
  - Bubble Sort
  - Selection Sort
  - Insertion Sort
  - Merge Sort
  - Quick Sort
- **Custom Array Input**: Enter your own comma-separated integers to test specific arrays.
- **Original Array Display**: View the original array alongside the current array during sorting.
- **Real-Time Stats**: Track the number of comparisons and swaps for each algorithm.
- **Animation Controls**: Start, pause, resume, or stop sorting, and adjust animation speed with a slider.
- **Random Array Generation**: Create random arrays with a single click for quick testing.

## Demo

![Sorting Visualizer Demo](Demo/Demo.gif)  


## Prerequisites

- **Python 3.x**: Ensure Python is installed on your system.
- **Tkinter**: Comes pre-installed with Python. If not, install it via:
  ```bash
  pip install tk
  ```

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/theusmandev/sorting-visualizer.git
   cd sorting-visualizer
   ```

2. **Run the Application**:
   ```bash
   python sorting_visualizer.py
   ```

   Ensure the `sorting_visualizer.py` file is in the project directory.

## Usage

1. **Launch the Visualizer**:
   Run the script to open the GUI window.

2. **Select an Algorithm**:
   Choose an algorithm (e.g., Bubble Sort) from the dropdown menu.

3. **Generate or Set an Array**:
   - Click "Generate New Array" to create a random array of 20 integers (10–300).
   - Enter a custom array (e.g., `50, 100, 30, 200`) in the text field and click "Set Custom Array". Values must be integers between 10 and 300, with a maximum of 20 elements.

4. **Start Sorting**:
   Click "Start Sorting" to visualize the algorithm. Bars turn:
   - **Red**: Elements being compared.
   - **Yellow**: Elements being swapped.
   - **Green**: Sorted elements.

5. **Control the Animation**:
   - Use the speed slider to adjust animation speed (10–200 ms).
   - Click "Pause" to pause sorting and "Resume" to continue.
   - Click "Stop" to end the sorting process.

6. **View Stats**:
   - The "Original Arr" label shows the initial array.
   - The "Current Arr" label shows the array as it sorts.
   - "Comparisons" and "Swaps" display real-time counts.

## Project Structure

- `sorting_visualizer.py`: Main script containing the `SortingVisualizer` class with GUI and algorithm logic.
- `demo.gif` (optional): Add a demo GIF or screenshot to showcase the visualizer.

## How It Works

- **GUI**: Built with Tkinter, featuring a canvas for bar visualization, control buttons, a speed slider, and labels for arrays and stats.
- **Visualization**: Bars represent array elements, with heights scaled to values (10–300). Colors indicate sorting actions.
- **Algorithms**: Each algorithm (Bubble, Selection, Insertion, Merge, Quick Sort) is implemented with step-by-step animation using `root.after` for smooth updates.
- **Custom Input**: Validates comma-separated integer inputs, ensuring they fit the canvas (≤20 elements, values 10–300).
- **Stats Tracking**: Counts comparisons and swaps to provide insight into algorithm efficiency.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes (e.g., add a new algorithm, improve UI, or optimize performance).
4. Commit your changes (`git commit -m "Add your feature"`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Open a pull request.

Please ensure your code follows PEP 8 style guidelines and includes comments for clarity.

## Future Enhancements

- Add a dual-canvas view to compare two algorithms side by side.
- Include a chart to visualize comparisons and swaps across algorithms.
- Support dynamic canvas sizing for larger or smaller arrays.
- Add sound effects for sorting actions (e.g., swaps).
- Save and load custom arrays for repeated testing.


## Acknowledgments

- Inspired by my love for algorithms and the desire to make learning visual and fun.
- Thanks to the Python and Tkinter communities for their amazing resources.

Feel free to star ⭐ this repository if you find it useful, and share your feedback or ideas in the issues section!

*Created by Muhammad Usman
