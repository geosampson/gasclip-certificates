#!/usr/bin/env python3
"""
Interactive Coordinate Picker Tool
Click on the PDF image to mark where text should appear, and save coordinates automatically.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from pdf2image import convert_from_path
from pathlib import Path
import json

class CoordinatePicker:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Coordinate Picker")
        self.root.geometry("1200x900")
        
        self.pdf_path = Path("templates/SOSP215459.pdf")
        self.coordinates = {}
        self.current_field = None
        self.page_num = 0
        self.images = []
        self.photo_images = []
        
        # Field definitions
        self.fields = [
            # Page 1
            ("Page 1: Serial Number", "serial", 0),
            ("Page 1: Activation Before", "activation_before", 0),
            ("Page 1: Lot Number", "lot_number", 0),
            ("Page 1: Gas Production", "gas_production", 0),
            ("Page 1: Calibration Date", "calibration_date", 0),
            # Page 2
            ("Page 2: Serial Number", "serial_p2", 1),
            ("Page 2: Activation Box 1 (d)", "act_d1", 1),
            ("Page 2: Activation Box 2 (d)", "act_d2", 1),
            ("Page 2: Activation Box 3 (m)", "act_m1", 1),
            ("Page 2: Activation Box 4 (m)", "act_m2", 1),
            ("Page 2: Activation Box 5 (y)", "act_y1", 1),
            ("Page 2: Activation Box 6 (y)", "act_y2", 1),
            ("Page 2: Activation Box 7 (y)", "act_y3", 1),
            ("Page 2: Activation Box 8 (y)", "act_y4", 1),
            ("Page 2: Expiration Box 1 (d)", "exp_d1", 1),
            ("Page 2: Expiration Box 2 (d)", "exp_d2", 1),
            ("Page 2: Expiration Box 3 (m)", "exp_m1", 1),
            ("Page 2: Expiration Box 4 (m)", "exp_m2", 1),
            ("Page 2: Expiration Box 5 (y)", "exp_y1", 1),
            ("Page 2: Expiration Box 6 (y)", "exp_y2", 1),
            ("Page 2: Expiration Box 7 (y)", "exp_y3", 1),
            ("Page 2: Expiration Box 8 (y)", "exp_y4", 1),
        ]
        
        self.field_index = 0
        
        self.setup_ui()
        self.load_pdf()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Top frame for instructions
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.instruction_label = ttk.Label(
            top_frame,
            text="Click on the PDF where the text should appear",
            font=("Arial", 12, "bold"),
            foreground="blue"
        )
        self.instruction_label.pack()
        
        self.field_label = ttk.Label(
            top_frame,
            text="",
            font=("Arial", 11),
            foreground="darkgreen"
        )
        self.field_label.pack()
        
        # Canvas for PDF display
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=v_scroll.set)
        
        h_scroll = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scroll.pack(side=tk.TOP, fill=tk.X, padx=10)
        self.canvas.configure(xscrollcommand=h_scroll.set)
        
        # Bind click event
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Bottom frame for buttons
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        ttk.Button(button_frame, text="Skip This Field", 
                  command=self.skip_field).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Previous Field", 
                  command=self.previous_field).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Save Coordinates", 
                  command=self.save_coordinates).pack(side=tk.RIGHT, padx=5)
        
        self.progress_label = ttk.Label(button_frame, text="", font=("Arial", 10))
        self.progress_label.pack(side=tk.RIGHT, padx=20)
    
    def load_pdf(self):
        """Load PDF and convert to images"""
        if not self.pdf_path.exists():
            messagebox.showerror("Error", f"PDF not found: {self.pdf_path}")
            return
        
        try:
            # Convert PDF to images
            self.images = convert_from_path(str(self.pdf_path), dpi=150)
            messagebox.showinfo("Success", f"Loaded {len(self.images)} pages")
            self.show_next_field()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PDF:\n{e}")
    
    def show_next_field(self):
        """Show the next field to mark"""
        if self.field_index >= len(self.fields):
            messagebox.showinfo("Complete", "All fields marked! Click 'Save Coordinates'")
            return
        
        field_name, field_id, page_num = self.fields[self.field_index]
        self.current_field = field_id
        self.page_num = page_num
        
        self.field_label.config(text=f"Field {self.field_index + 1}/{len(self.fields)}: {field_name}")
        self.progress_label.config(text=f"Progress: {self.field_index}/{len(self.fields)}")
        
        # Display the correct page
        self.display_page(page_num)
    
    def display_page(self, page_num):
        """Display a specific page on the canvas"""
        if page_num >= len(self.images):
            return
        
        img = self.images[page_num]
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(img)
        self.photo_images.append(photo)  # Keep reference
        
        # Clear canvas
        self.canvas.delete("all")
        
        # Display image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        # Draw existing coordinates
        self.draw_existing_coordinates()
    
    def draw_existing_coordinates(self):
        """Draw markers for already-marked coordinates"""
        for field_id, (x, y, page) in self.coordinates.items():
            if page == self.page_num:
                # Convert PDF coordinates (bottom-left) to image coordinates (top-left)
                img_height = self.images[page].height
                img_y = img_height - y
                
                # Draw a red circle
                r = 5
                self.canvas.create_oval(x-r, img_y-r, x+r, img_y+r, 
                                       fill="red", outline="darkred", width=2)
                self.canvas.create_text(x, img_y-15, text=field_id, 
                                       fill="red", font=("Arial", 8, "bold"))
    
    def on_canvas_click(self, event):
        """Handle canvas click to mark coordinate"""
        if not self.current_field:
            return
        
        # Get click position
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        
        # Convert to PDF coordinates (bottom-left origin)
        img_height = self.images[self.page_num].height
        pdf_y = img_height - y
        
        # Convert from image pixels (150 DPI) to PDF points (72 DPI)
        scale = 72 / 150
        pdf_x = x * scale
        pdf_y = pdf_y * scale
        
        # Store coordinate
        self.coordinates[self.current_field] = (int(pdf_x), int(pdf_y), self.page_num)
        
        print(f"Marked {self.current_field}: ({int(pdf_x)}, {int(pdf_y)}) on page {self.page_num + 1}")
        
        # Move to next field
        self.field_index += 1
        self.show_next_field()
    
    def skip_field(self):
        """Skip the current field"""
        self.field_index += 1
        self.show_next_field()
    
    def previous_field(self):
        """Go back to previous field"""
        if self.field_index > 0:
            self.field_index -= 1
            # Remove the coordinate if it exists
            field_name, field_id, page_num = self.fields[self.field_index]
            if field_id in self.coordinates:
                del self.coordinates[field_id]
            self.show_next_field()
    
    def save_coordinates(self):
        """Save coordinates to a JSON file"""
        if not self.coordinates:
            messagebox.showwarning("Warning", "No coordinates to save!")
            return
        
        output_file = Path("pdf_coordinates.json")
        
        # Convert to saveable format
        save_data = {
            field_id: {"x": x, "y": y, "page": page}
            for field_id, (x, y, page) in self.coordinates.items()
        }
        
        with open(output_file, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        messagebox.showinfo("Success", 
                           f"Coordinates saved to: {output_file}\n\n"
                           f"Total fields marked: {len(self.coordinates)}")
        
        print(f"\nSaved coordinates to: {output_file}")
        print(json.dumps(save_data, indent=2))

def main():
    root = tk.Tk()
    app = CoordinatePicker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
