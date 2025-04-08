import os
import shutil
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from functions import Extraction,convert_jpg_to_png,takeoff_Slide_from_name

class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Presenting with Computer Vision")
        self.root.geometry("500x500")
        self.center_window(500, 500)
        self.root.configure(bg="#2C3E50")  # Dark background

        # Set custom window icon (Replace 'icon.ico' with your actual icon file)
        self.root.iconbitmap(r"C:\Users\fftt7\PycharmProjects\PresentationAppComputerVision\icon\projection-screen.ico")  # Make sure you have an 'icon.ico' file in the same directory

        # Apply ttk styles
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 12), padding=6, background="#3498DB", foreground="white")
        style.map("TButton", background=[("active", "#2980B9")])

        self.file_path = ""
        self.output_dir = ""

        # Create a frame for layout
        main_frame = tk.Frame(root, bg="#2C3E50")
        main_frame.pack(expand=True)

        # Welcome label with rainbow effect
        self.welcome_label = tk.Label(
            main_frame, text="🎉 Welcome to File Manager 🎉",
            font=("Arial", 16, "bold"), bg="#2C3E50"
        )
        self.welcome_label.pack(pady=10)
        self.animate_rainbow_text()  # Start the rainbow animation

        # Create buttons
        buttons = [
            ("📂 Upload Data", self.upload_file),
            ("📦 Extract ZIP", self.extract_zip),
            ("🖼️ Convert JPG to PNG", self.convert_images),
            ("✍️ Rename Files", self.rename_images),
            ("🚀 Start App", self.start_app),
            ("❌ Exit", self.cleanup_and_exit),
        ]

        # Create a frame to hold buttons (so they stay centered)
        button_frame = tk.Frame(main_frame, bg="#2C3E50")
        button_frame.pack(pady=10)

        for text, command in buttons:
            btn = ttk.Button(button_frame, text=text, command=command, width=25)
            btn.pack(pady=5)  # Space between buttons

        # Status label
        self.status_label = tk.Label(
            root, text="No file selected", foreground="white", background="#2C3E50", font=("Arial", 10)
        )
        self.status_label.pack(side="bottom", pady=10)

    def upload_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("ZIP Files", "*.zip")])
        if self.file_path:
            self.output_dir = os.path.join(os.path.dirname(self.file_path), "ExtractedImages")
            self.status_label.config(text=f"Selected: {os.path.basename(self.file_path)}")
            messagebox.showinfo("File Selected", f"Selected: {self.file_path}")

    def extract_zip(self):
        if not self.file_path or not self.file_path.endswith(".zip"):
            messagebox.showwarning("Invalid File", "Please select a ZIP file.")
            return

        try:
            Extraction.extract_images(self.file_path, self.output_dir)
            self.status_label.config(text="Extraction Completed!")
            messagebox.showinfo("Extraction Completed", f"Images extracted to {self.output_dir}")
        except Exception as e:
            messagebox.showerror("Error", f"Extraction failed: {e}")

    def convert_images(self):
        if not self.output_dir or not os.path.exists(self.output_dir):
            messagebox.showwarning("No Extracted Files", "Please extract files first!")
            return

        converted_dir = os.path.join(os.path.dirname(self.file_path), "ConvertedImages")

        try:
            converted_files = convert_jpg_to_png.convert(self.output_dir, converted_dir)
            if converted_files:
                self.status_label.config(text="Conversion Completed!")
                messagebox.showinfo("Conversion Completed", f"Converted images saved to {converted_dir}")
            else:
                messagebox.showwarning("No JPG Found", "No JPG images found for conversion.")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {e}")

    def rename_images(self):
        converted_dir = os.path.join(os.path.dirname(self.file_path), "ConvertedImages")
        renamed_dir = os.path.join(os.path.dirname(self.file_path), "Presentation")

        if not os.path.exists(converted_dir):
            messagebox.showwarning("No Converted Files", "Please convert JPG to PNG first!")
            return

        try:
            renamed_files = takeoff_Slide_from_name.rename_images(converted_dir, renamed_dir)
            if renamed_files:
                self.status_label.config(text="Renaming Completed!")
                messagebox.showinfo("Renaming Completed", f"Renamed images saved to {renamed_dir}")
            else:
                messagebox.showwarning("No PNG Found", "No PNG images found for renaming.")
        except Exception as e:
            messagebox.showerror("Error", f"Renaming failed: {e}")

    def cleanup_and_exit(self):
        """Deletes extracted and processed files before exiting."""
        for folder in ["ExtractedImages", "ConvertedImages", "Presentation"]:
            dir_path = os.path.join(os.path.dirname(self.file_path), folder)
            if os.path.exists(dir_path):
                try:
                    shutil.rmtree(dir_path)
                    print(f"Deleted folder: {dir_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete files in {folder}: {e}")

        self.root.quit()

    def start_app(self):
        """Runs the App.py script and hides the interface. Shows it again when the app is closed."""
        try:
            self.root.withdraw()  # Hide the Tkinter window
            python_executable = sys.executable
            process = subprocess.Popen([python_executable, "App.py"])

            threading.Thread(target=self.monitor_app, args=(process,), daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start app: {e}")

    def monitor_app(self, process):
        """Waits for the App.py process to close, then shows the Tkinter window again."""
        process.wait()
        self.root.after(0, self.root.deiconify)

    def center_window(self, width, height):
        """Centers the window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def animate_rainbow_text(self):
        """Animates the welcome text in a rainbow effect."""
        colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#8B00FF"]
        text = "🎉 Welcome to File Manager 🎉"

        def update_color(index=0):
            self.welcome_label.config(fg=colors[index])
            self.root.after(300, update_color, (index + 1) % len(colors))

        update_color()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()
