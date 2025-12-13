#!/usr/bin/env python3
"""
GasClip Certificate Coordinate Calibrator
This tool helps you visually set the exact coordinates for text placement on PDF templates.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from pdf2image import convert_from_path
import json
from pathlib import Path

class CoordinateCalibrator:
    def __init__(self, root):
        self.root = root
        self.root.title("GasClip Certificate Coordinate Calibrator")
        self.root.geometry("1400x900")
        
        # Product information
        self.products = {
            "D4PQ": {"name": "MGC-S+ (MGC-SIMPLEPLUS)", "template": "D4PQ236599_clean.pdf", "months": 36, "days": 1095},
            "SOSP": {"name": "SGC-O (Single Gas Clip O2)", "template": "SOSP215459_clean.pdf", "months": 24, "days": 730},
            "SCSQ": {"name": "SGC-C (Single Gas Clip CO)", "template": "SCSQ175392_clean.pdf", "months": 24, "days": 730},
            "D4SQ": {"name": "MGC-S (MGC-SIMPLE)", "template": "D4SQ106733_clean.pdf", "months": 24, "days": 730},
            "SHSP": {"name": "SGC-H (Single Gas Clip H2S)", "template": "SHSP085112_clean.pdf", "months": 24, "days": 730}
        }
        
        # Fields to calibrate
        self.fields = [
            "serial_p1",  # Serial number on page 1
            "activation",  # Activation date on page 1
            "lot",  # Lot number on page 1
            "gas_production",  # Gas production date on page 1
            "calibration",  # Calibration date on page 1
            "serial_p2"  # Serial number on page 2
        ]
        
        self.field_descriptions = {
            "serial_p1": "Serial Number (Page 1, top right)",
            "activation": "Activation Date (Page 1, below serial)",
            "lot": "Lot Number (Page 1, middle section)",
            "gas_production": "Gas Production Date (Page 1, middle section)",
            "calibration": "Calibration Date (Page 1, bottom section)",
            "serial_p2": "Serial Number (Page 2, after 'sn:')"
        }
        
        # Current state
        self.current_product = None
        self.current_page = 1
        self.current_field_index = 0
        self.pdf_images = []
        self.coordinates = {}
        self.scale_factor = 1.0
        
        self.setup_ui()
        
    def setup_ui(self):
        # Top control panel
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Product selection
        ttk.Label(control_frame, text="Select Product:").pack(side=tk.LEFT, padx=5)
        self.product_var = tk.StringVar()
        product_combo = ttk.Combobox(control_frame, textvariable=self.product_var, 
                                     values=[f"{k}: {v['name']}" for k, v in self.products.items()],
                                     width=40, state="readonly")
        product_combo.pack(side=tk.LEFT, padx=5)
        product_combo.bind("<<ComboboxSelected>>", self.load_product)
        
        ttk.Button(control_frame, text="Load PDF", command=self.load_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Save Coordinates", command=self.save_coordinates).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Load Saved", command=self.load_saved_coordinates).pack(side=tk.LEFT, padx=5)
        
        # Instructions frame
        inst_frame = ttk.LabelFrame(self.root, text="Instructions", padding="10")
        inst_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        self.instruction_label = ttk.Label(inst_frame, text="Select a product and click 'Load PDF' to begin", 
                                          font=("Arial", 12, "bold"))
        self.instruction_label.pack()
        
        # Current field info
        self.field_label = ttk.Label(inst_frame, text="", font=("Arial", 10))
        self.field_label.pack()
        
        # Main canvas area
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Canvas with scrollbars
        self.canvas = tk.Canvas(canvas_frame, bg="gray", cursor="crosshair")
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Bottom control panel
        bottom_frame = ttk.Frame(self.root, padding="10")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        ttk.Button(bottom_frame, text="◀ Previous Field", command=self.previous_field).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Next Field ▶", command=self.next_field).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Page 1", command=lambda: self.switch_page(1)).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Page 2", command=lambda: self.switch_page(2)).pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(bottom_frame, text="Ready", relief=tk.SUNKEN)
        self.status_label.pack(side=tk.RIGHT, padx=5)
        
    def load_product(self, event=None):
        selection = self.product_var.get()
        if selection:
            self.current_product = selection.split(":")[0]
            self.status_label.config(text=f"Selected: {self.products[self.current_product]['name']}")
            
    def load_pdf(self):
        if not self.current_product:
            messagebox.showwarning("No Product", "Please select a product first!")
            return
            
        template_path = Path(__file__).parent / "templates" / self.products[self.current_product]["template"]
        
        if not template_path.exists():
            messagebox.showerror("File Not Found", f"Template not found: {template_path}")
            return
            
        try:
            # Convert PDF to images
            self.status_label.config(text="Loading PDF...")
            self.root.update()
            
            self.pdf_images = convert_from_path(str(template_path), dpi=150)
            
            # Initialize coordinates dict for this product
            if self.current_product not in self.coordinates:
                self.coordinates[self.current_product] = {}
                
            self.current_page = 1
            self.current_field_index = 0
            self.display_page()
            self.update_instructions()
            
            self.status_label.config(text="PDF loaded successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PDF: {e}")
            self.status_label.config(text="Error loading PDF")
            
    def display_page(self):
        if not self.pdf_images:
            return
            
        # Get the image for current page
        img = self.pdf_images[self.current_page - 1]
        
        # Calculate scale to fit canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:
            scale_x = canvas_width / img.width
            scale_y = canvas_height / img.height
            self.scale_factor = min(scale_x, scale_y, 1.0)  # Don't scale up
        else:
            self.scale_factor = 0.8
            
        # Resize image
        new_width = int(img.width * self.scale_factor)
        new_height = int(img.height * self.scale_factor)
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        self.photo = ImageTk.PhotoImage(img_resized)
        
        # Clear canvas and display image
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.canvas.config(scrollregion=(0, 0, new_width, new_height))
        
        # Draw existing coordinates as markers
        self.draw_markers()
        
    def draw_markers(self):
        if self.current_product not in self.coordinates:
            return
            
        for field, coord in self.coordinates[self.current_product].items():
            page = coord.get("page", 1)
            if page == self.current_page:
                x = coord["x"] * self.scale_factor
                y = coord["y"] * self.scale_factor
                
                # Draw crosshair
                size = 20
                self.canvas.create_line(x - size, y, x + size, y, fill="red", width=2, tags="marker")
                self.canvas.create_line(x, y - size, x, y + size, fill="red", width=2, tags="marker")
                self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="red", width=2, tags="marker")
                
                # Draw label
                self.canvas.create_text(x, y - 30, text=field, fill="red", font=("Arial", 10, "bold"), tags="marker")
                
    def on_canvas_click(self, event):
        if not self.pdf_images or not self.current_product:
            return
            
        # Convert canvas coordinates to PDF coordinates
        x = event.x / self.scale_factor
        y = event.y / self.scale_factor
        
        # Get current field
        current_field = self.fields[self.current_field_index]
        
        # Determine which page this field belongs to
        page = 2 if current_field == "serial_p2" else 1
        
        # Store coordinates
        self.coordinates[self.current_product][current_field] = {
            "x": x,
            "y": y,
            "page": page
        }
        
        # Redraw markers
        self.draw_markers()
        
        # Move to next field
        self.next_field()
        
        self.status_label.config(text=f"Saved {current_field} at ({x:.1f}, {y:.1f})")
        
    def next_field(self):
        if self.current_field_index < len(self.fields) - 1:
            self.current_field_index += 1
            self.update_instructions()
            
            # Auto-switch to page 2 if needed
            current_field = self.fields[self.current_field_index]
            if current_field == "serial_p2":
                self.switch_page(2)
        else:
            messagebox.showinfo("Complete", "All fields calibrated! Click 'Save Coordinates' to save.")
            
    def previous_field(self):
        if self.current_field_index > 0:
            self.current_field_index -= 1
            self.update_instructions()
            
            # Auto-switch to page 1 if needed
            current_field = self.fields[self.current_field_index]
            if current_field != "serial_p2":
                self.switch_page(1)
                
    def switch_page(self, page):
        if not self.pdf_images:
            return
            
        if 1 <= page <= len(self.pdf_images):
            self.current_page = page
            self.display_page()
            self.status_label.config(text=f"Viewing Page {page}")
            
    def update_instructions(self):
        current_field = self.fields[self.current_field_index]
        description = self.field_descriptions[current_field]
        
        self.instruction_label.config(text=f"Click on the PDF where you want to place: {description}")
        self.field_label.config(text=f"Field {self.current_field_index + 1} of {len(self.fields)}: {current_field}")
        
    def save_coordinates(self):
        if not self.coordinates:
            messagebox.showwarning("No Data", "No coordinates to save!")
            return
            
        output_file = Path(__file__).parent / "calibrated_coordinates.json"
        
        try:
            with open(output_file, 'w') as f:
                json.dump(self.coordinates, f, indent=2)
                
            messagebox.showinfo("Success", f"Coordinates saved to:\n{output_file}")
            self.status_label.config(text="Coordinates saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save coordinates: {e}")
            
    def load_saved_coordinates(self):
        coord_file = Path(__file__).parent / "calibrated_coordinates.json"
        
        if not coord_file.exists():
            messagebox.showwarning("No File", "No saved coordinates found!")
            return
            
        try:
            with open(coord_file, 'r') as f:
                self.coordinates = json.load(f)
                
            messagebox.showinfo("Success", "Coordinates loaded successfully!")
            self.display_page()  # Redraw with loaded coordinates
            self.status_label.config(text="Coordinates loaded")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load coordinates: {e}")

def main():
    root = tk.Tk()
    app = CoordinateCalibrator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
