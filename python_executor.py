import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.scrolledtext as scrolledtext
import subprocess
import os

def execute_code():
    code = code_input.get("1.0", "end-1c")
    with open("temp_script.py", "w") as f:
        f.write(code)
    try:
        result = subprocess.check_output(["python", "temp_script.py"], stderr=subprocess.STDOUT, text=True)
        output_text.configure(state='normal')
        output_text.delete("1.0", "end")
        output_text.insert("1.0", result)
        output_text.configure(state='disabled')
    except subprocess.CalledProcessError as e:
        output_text.configure(state='normal')
        output_text.delete("1.0", "end")
        output_text.insert("1.0", e.output)
        output_text.configure(state='disabled')

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        with open(file_path, "r") as f:
            code = f.read()
        code_input.delete("1.0", "end")
        code_input.insert("1.0", code)
        update_line_numbers()

def save_file():
    code = code_input.get("1.0", "end-1c")
    file_path = filedialog.asksaveasfilename(filetypes=[("Python Files", "*.py")], defaultextension=".py")
    if file_path:
        with open(file_path, "w") as f:
            f.write(code)

def open_terminal():
    terminal_window = tk.Toplevel(root)
    terminal_window.title("Terminal")
    
    terminal_output = scrolledtext.ScrolledText(terminal_window, wrap=tk.WORD, width=80, height=20)
    terminal_output.grid(row=0, column=0, padx=10, pady=10)
    terminal_output.configure(state='disabled')
    
    terminal_input = ttk.Entry(terminal_window, width=60)
    terminal_input.grid(row=1, column=0, padx=10, pady=10)
    
    def run_command():
        command = terminal_input.get()
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            terminal_output.configure(state='normal')
            terminal_output.insert("end", f"$ {command}\n{result}\n")
            terminal_output.configure(state='disabled')
        except subprocess.CalledProcessError as e:
            terminal_output.configure(state='normal')
            terminal_output.insert("end", f"$ {command}\n{e.output}\n")
            terminal_output.configure(state='disabled')
        
        terminal_input.delete(0, "end")
    
    run_button = ttk.Button(terminal_window, text="Run", command=run_command)
    run_button.grid(row=1, column=1)
    
    def clear_output():
        terminal_output.configure(state='normal')
        terminal_output.delete("1.0", "end")
        terminal_output.configure(state='disabled')
    
    clear_button = ttk.Button(terminal_window, text="Clear Output", command=clear_output)
    clear_button.grid(row=2, column=0)
    
    def close_terminal():
        terminal_window.destroy()
    
    close_button = ttk.Button(terminal_window, text="Close", command=close_terminal)
    close_button.grid(row=2, column=1)

def update_line_numbers(event=None):
    code = code_input.get("1.0", "end-1c")
    lines = code.split("\n")
    line_count = len(lines)
    line_numbers.configure(state='normal')
    line_numbers.delete("1.0", "end")
    line_numbers.insert("1.0", "\n".join(str(i) for i in range(1, line_count + 1)))
    line_numbers.configure(state='disabled')
    # Auto-scroll the line numbers to the same position as code_input
    code_y_offset = code_input.yview()[0]
    line_numbers.yview_moveto(code_y_offset)

# Create the main window
root = tk.Tk()
root.title("Python Executor")

# Create a menu bar
menu = tk.Menu(root)
root.config(menu=menu)

# Create a "File" menu
file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)

# Create a Text widget for code input
code_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=15)
code_input.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
code_input.bind("<KeyRelease>", update_line_numbers)

# Create a button to execute code
execute_button = ttk.Button(root, text="Run", command=execute_code)
execute_button.grid(row=1, column=1)

# Create a Text widget for output
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=15)
output_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
output_text.configure(state='disabled')

# Create a Text widget for line numbers
line_numbers = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=3, height=15)
line_numbers.grid(row=0, column=3, rowspan=3, padx=(0, 10))
line_numbers.configure(state='disabled')

# ... (Previous code)

# Create a button to open the terminal
open_terminal_button = ttk.Button(root, text="Open Terminal", command=open_terminal)
open_terminal_button.grid(row=1, column=2, padx=10)

root.mainloop()
