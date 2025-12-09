#!/usr/bin/env python3
"""
GasClip Certificates Generator
A desktop application for generating calibration test certificates for GasClip gas detectors.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os
import shutil
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
import io


class GasClipCertificateGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("GasClip Certificates Generator")
        self.root.geometry("750x700")
        self.root.resizable(False, False)
        
        # Product configurations with coordinate positions for text overlay
        self.products = {
            "MGC-S+ (MGC-SIMPLEPLUS)": {
                "prefix": "D4PQ",
                "template": "D4PQ236599.pdf",
                "detector_life": 36,
                "calibration_days": 1095,
                "full_name": "MGC-S+",
                "description": "MGC-SIMPLEPLUS",
                "positions": {
                    "serial_page1": (520, 685),
                    "activation_date_page1": (520, 670),
                    "lot_number": (130, 430),
                    "gas_production": (130, 415),
                    "calibration_date": (180, 350),
                    "serial_page2": (520, 750),
                    "activation_date_page2_boxes": [(545, 470), (565, 470), (595, 470), (615, 470), (655, 470), (675, 470), (695, 470), (715, 470)],
                    "calibration_exp_boxes": [(545, 390), (565, 390), (595, 390), (615, 390), (655, 390), (675, 390), (695, 390), (715, 390)]
                }
            },
            "SGC-O (Single Gas Clip O2)": {
                "prefix": "SOSP",
                "template": "SOSP215459.pdf",
                "detector_life": 24,
                "calibration_days": 730,
                "full_name": "SGC-O",
                "description": "Single Gas Clip O2",
                "positions": {
                    "serial_page1": (520, 685),
                    "activation_date_page1": (520, 670),
                    "lot_number": (130, 430),
                    "gas_production": (130, 415),
                    "calibration_date": (180, 350),
                    "serial_page2": (520, 750),
                    "activation_date_page2_boxes": [(545, 470), (565, 470), (595, 470), (615, 470), (655, 470), (675, 470), (695, 470), (715, 470)],
                    "calibration_exp_boxes": [(545, 390), (565, 390), (595, 390), (615, 390), (655, 390), (675, 390), (695, 390), (715, 390)]
                }
            },
            "SGC-C (Single Gas Clip CO)": {
                "prefix": "SCSQ",
                "template": "SCSQ175392.pdf",
                "detector_life": 24,
                "calibration_days": 730,
                "full_name": "SGC-C",
                "description": "Single Gas Clip CO",
                "positions": {
                    "serial_page1": (520, 685),
                    "activation_date_page1": (520, 670),
                    "lot_number": (130, 430),
                    "gas_production": (130, 415),
                    "calibration_date": (180, 350),
                    "serial_page2": (520, 750),
                    "activation_date_page2_boxes": [(545, 470), (565, 470), (595, 470), (615, 470), (655, 470), (675, 470), (695, 470), (715, 470)],
                    "calibration_exp_boxes": [(545, 390), (565, 390), (595, 390), (615, 390), (655, 390), (675, 390), (695, 390), (715, 390)]
                }
            },
            "MGC-S (MGC-SIMPLE)": {
                "prefix": "D4SQ",
                "template": "D4SQ106733.pdf",
                "detector_life": 24,
                "calibration_days": 730,
                "full_name": "MGC-S",
                "description": "MGC-SIMPLE",
                "positions": {
                    "serial_page1": (520, 685),
                    "activation_date_page1": (520, 670),
                    "lot_number": (130, 430),
                    "gas_production": (130, 415),
                    "calibration_date": (180, 350),
                    "serial_page2": (520, 750),
                    "activation_date_page2_boxes": [(545, 470), (565, 470), (595, 470), (615, 470), (655, 470), (675, 470), (695, 470), (715, 470)],
                    "calibration_exp_boxes": [(545, 390), (565, 390), (595, 390), (615, 390), (655, 390), (675, 390), (695, 390), (715, 390)]
                }
            },
            "SGC-H (Single Gas Clip H2S)": {
                "prefix": "SHSP",
                "template": "SHSP085112.pdf",
                "detector_life": 24,
                "calibration_days": 730,
                "full_name": "SGC-H",
                "description": "Single Gas Clip H₂S",
                "positions": {
                    "serial_page1": (520, 685),
                    "activation_date_page1": (520, 670),
                    "lot_number": (130, 430),
                    "gas_production": (130, 415),
                    "calibration_date": (180, 350),
                    "serial_page2": (520, 750),
                    "activation_date_page2_boxes": [(545, 470), (565, 470), (595, 470), (615, 470), (655, 470), (675, 470), (695, 470), (715, 470)],
                    "calibration_exp_boxes": [(545, 390), (565, 390), (595, 390), (615, 390), (655, 390), (675, 390), (695, 390), (715, 390)]
                }
            }
        }
        
        # Storage for generated certificates
        self.generated_certificates = []
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame with scrollbar
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="GasClip Certificate Generator", 
                                font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Product selection
        ttk.Label(main_frame, text="Select Product:", font=("Arial", 11, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.product_var = tk.StringVar()
        product_combo = ttk.Combobox(main_frame, textvariable=self.product_var, 
                                     values=list(self.products.keys()), 
                                     state="readonly", width=45)
        product_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        product_combo.bind("<<ComboboxSelected>>", self.on_product_select)
        
        # Serial number prefix display
        ttk.Label(main_frame, text="Serial Number Prefix:", font=("Arial", 11)).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.prefix_label = ttk.Label(main_frame, text="", font=("Arial", 12, "bold"), 
                                      foreground="blue")
        self.prefix_label.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        
        # Serial number input
        ttk.Label(main_frame, text="Serial Number (digits only):", font=("Arial", 11)).grid(
            row=4, column=0, sticky=tk.W, pady=5)
        self.serial_entry = ttk.Entry(main_frame, width=47, font=("Arial", 10))
        self.serial_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        ttk.Label(main_frame, text="Example: 236599", 
                  font=("Arial", 9), foreground="gray").grid(
            row=5, column=1, sticky=tk.W, padx=(10, 0))
        
        # Activation date
        ttk.Label(main_frame, text="Activation Date (DDMMYYYY):", font=("Arial", 11)).grid(
            row=6, column=0, sticky=tk.W, pady=5)
        self.activation_entry = ttk.Entry(main_frame, width=47, font=("Arial", 10))
        self.activation_entry.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        ttk.Label(main_frame, text="Example: 26022025 for 26/02/2025", 
                  font=("Arial", 9), foreground="gray").grid(
            row=7, column=1, sticky=tk.W, padx=(10, 0))
        
        # Lot number
        ttk.Label(main_frame, text="Lot Number:", font=("Arial", 11)).grid(
            row=8, column=0, sticky=tk.W, pady=5)
        self.lot_entry = ttk.Entry(main_frame, width=47, font=("Arial", 10))
        self.lot_entry.grid(row=8, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        ttk.Label(main_frame, text="Example: RR2310181807 or 25-3348", 
                  font=("Arial", 9), foreground="gray").grid(
            row=9, column=1, sticky=tk.W, padx=(10, 0))
        
        # Gas production date
        ttk.Label(main_frame, text="Gas Production Date (DDMMYYYY):", font=("Arial", 11)).grid(
            row=10, column=0, sticky=tk.W, pady=5)
        self.gas_prod_entry = ttk.Entry(main_frame, width=47, font=("Arial", 10))
        self.gas_prod_entry.grid(row=10, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        ttk.Label(main_frame, text="Example: 19102023", 
                  font=("Arial", 9), foreground="gray").grid(
            row=11, column=1, sticky=tk.W, padx=(10, 0))
        
        # Calibration date
        ttk.Label(main_frame, text="Calibration Date (DDMMYYYY):", font=("Arial", 11)).grid(
            row=12, column=0, sticky=tk.W, pady=5)
        self.calibration_entry = ttk.Entry(main_frame, width=47, font=("Arial", 10))
        self.calibration_entry.grid(row=12, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        ttk.Label(main_frame, text="Example: 26022024", 
                  font=("Arial", 9), foreground="gray").grid(
            row=13, column=1, sticky=tk.W, padx=(10, 0))
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=14, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=15, column=0, columnspan=2, pady=10)
        
        # Generate button
        generate_btn = ttk.Button(button_frame, text="✓ Generate Certificate", 
                                  command=self.generate_certificate,
                                  width=25)
        generate_btn.grid(row=0, column=0, padx=5)
        
        # Clear button
        clear_btn = ttk.Button(button_frame, text="Clear Form", 
                              command=self.clear_form,
                              width=15)
        clear_btn.grid(row=0, column=1, padx=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to generate certificates", 
                                      font=("Arial", 10), 
                                      foreground="blue")
        self.status_label.grid(row=16, column=0, columnspan=2, pady=5)
        
        # Certificate counter
        self.counter_label = ttk.Label(main_frame, 
                                       text="Certificates Generated: 0", 
                                       font=("Arial", 11, "bold"),
                                       foreground="darkgreen")
        self.counter_label.grid(row=17, column=0, columnspan=2, pady=10)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=18, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Finish button
        finish_btn = ttk.Button(main_frame, text="📁 Finish All Forms & Create Invoice Folder", 
                               command=self.finish_all_forms,
                               width=50)
        finish_btn.grid(row=19, column=0, columnspan=2, pady=10)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def on_product_select(self, event=None):
        """Update prefix label when product is selected"""
        product = self.product_var.get()
        if product in self.products:
            prefix = self.products[product]["prefix"]
            self.prefix_label.config(text=f"{prefix}XXXXXX")
    
    def format_date(self, date_str):
        """Convert DDMMYYYY to DD/MM/YYYY"""
        if len(date_str) != 8:
            raise ValueError("Date must be 8 digits (DDMMYYYY)")
        return f"{date_str[:2]}/{date_str[2:4]}/{date_str[4:]}"
    
    def calculate_expiration_date(self, activation_date_str, days):
        """Calculate expiration date from activation date"""
        # Parse DDMMYYYY
        day = int(activation_date_str[:2])
        month = int(activation_date_str[2:4])
        year = int(activation_date_str[4:])
        
        from datetime import datetime, timedelta
        activation = datetime(year, month, day)
        expiration = activation + timedelta(days=days)
        
        return expiration.strftime("%d%m%Y")
    
    def validate_inputs(self):
        """Validate all input fields"""
        if not self.product_var.get():
            messagebox.showerror("Error", "Please select a product")
            return False
        
        if not self.serial_entry.get() or not self.serial_entry.get().isdigit():
            messagebox.showerror("Error", "Serial number must contain only digits")
            return False
        
        if len(self.activation_entry.get()) != 8 or not self.activation_entry.get().isdigit():
            messagebox.showerror("Error", "Activation date must be 8 digits (DDMMYYYY)")
            return False
        
        if not self.lot_entry.get():
            messagebox.showerror("Error", "Lot number is required")
            return False
        
        if len(self.gas_prod_entry.get()) != 8 or not self.gas_prod_entry.get().isdigit():
            messagebox.showerror("Error", "Gas production date must be 8 digits (DDMMYYYY)")
            return False
        
        if len(self.calibration_entry.get()) != 8 or not self.calibration_entry.get().isdigit():
            messagebox.showerror("Error", "Calibration date must be 8 digits (DDMMYYYY)")
            return False
        
        return True
    
    def generate_certificate(self):
        """Generate the PDF certificate by copying the template"""
        if not self.validate_inputs():
            return
        
        try:
            product_name = self.product_var.get()
            product_info = self.products[product_name]
            
            # Get input values
            serial_number = product_info["prefix"] + self.serial_entry.get()
            activation_date = self.format_date(self.activation_entry.get())
            lot_number = self.lot_entry.get()
            gas_prod_date = self.format_date(self.gas_prod_entry.get())
            calibration_date = self.format_date(self.calibration_entry.get())
            
            # Calculate calibration expiration
            calibration_exp = self.calculate_expiration_date(
                self.activation_entry.get(), 
                product_info["calibration_days"])
            calibration_exp_formatted = self.format_date(calibration_exp)
            
            # Create output filename
            output_filename = f"{serial_number}.pdf"
            output_path = self.output_dir / output_filename
            
            # Copy template to output (simple copy for now)
            template_path = Path("templates") / product_info["template"]
            if not template_path.exists():
                messagebox.showerror("Error", f"Template not found: {template_path}")
                return
            
            shutil.copy(template_path, output_path)
            
            # Store certificate info
            self.generated_certificates.append({
                "filename": output_filename,
                "path": str(output_path),
                "serial": serial_number,
                "product": product_name,
                "data": {
                    "serial": serial_number,
                    "activation": activation_date,
                    "lot": lot_number,
                    "gas_prod": gas_prod_date,
                    "calibration": calibration_date,
                    "calibration_exp": calibration_exp_formatted
                }
            })
            
            # Update UI
            self.status_label.config(
                text=f"✓ Certificate generated: {output_filename}", 
                foreground="green")
            self.counter_label.config(
                text=f"Certificates Generated: {len(self.generated_certificates)}")
            
            # Ask if user wants to continue or view
            response = messagebox.askyesno(
                "Success", 
                f"Certificate {output_filename} generated successfully!\n\n"
                f"Serial: {serial_number}\n"
                f"Activation: {activation_date}\n"
                f"Calibration Exp: {calibration_exp_formatted}\n\n"
                f"Do you want to create another certificate?")
            
            if response:
                self.clear_form()
            else:
                # Ask if they want to finish
                finish = messagebox.askyesno(
                    "Finish?",
                    "Do you want to finish and create the invoice folder now?")
                if finish:
                    self.finish_all_forms()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate certificate:\n{str(e)}")
    
    def clear_form(self):
        """Clear all input fields except product selection"""
        self.serial_entry.delete(0, tk.END)
        self.activation_entry.delete(0, tk.END)
        self.lot_entry.delete(0, tk.END)
        self.gas_prod_entry.delete(0, tk.END)
        self.calibration_entry.delete(0, tk.END)
        self.serial_entry.focus()
    
    def finish_all_forms(self):
        """Finish all forms and create invoice folder"""
        if not self.generated_certificates:
            messagebox.showwarning("Warning", "No certificates have been generated yet!")
            return
        
        # Ask for invoice number
        invoice_dialog = tk.Toplevel(self.root)
        invoice_dialog.title("Enter Invoice Number")
        invoice_dialog.geometry("450x180")
        invoice_dialog.resizable(False, False)
        
        # Center the dialog
        invoice_dialog.transient(self.root)
        invoice_dialog.grab_set()
        
        frame = ttk.Frame(invoice_dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Enter Invoice Number:", 
                  font=("Arial", 12, "bold")).pack(pady=15)
        invoice_entry = ttk.Entry(frame, width=35, font=("Arial", 11))
        invoice_entry.pack(pady=10)
        invoice_entry.focus()
        
        def create_invoice_folder():
            invoice_number = invoice_entry.get().strip()
            if not invoice_number:
                messagebox.showerror("Error", "Invoice number is required!")
                return
            
            try:
                # Create invoice folder
                invoice_folder = self.output_dir / f"Invoice_{invoice_number}"
                invoice_folder.mkdir(exist_ok=True)
                
                # Move all generated certificates to invoice folder
                moved_count = 0
                for cert in self.generated_certificates:
                    src = Path(cert["path"])
                    dst = invoice_folder / cert["filename"]
                    if src.exists():
                        shutil.move(str(src), str(dst))
                        moved_count += 1
                
                invoice_dialog.destroy()
                
                messagebox.showinfo(
                    "Success", 
                    f"✓ All {moved_count} certificates have been organized!\n\n"
                    f"Folder: {invoice_folder.name}\n"
                    f"Location: {invoice_folder.absolute()}\n\n"
                    f"You can now:\n"
                    f"• Close the application\n"
                    f"• Start a new batch of certificates")
                
                # Reset for new batch
                self.generated_certificates = []
                self.counter_label.config(text="Certificates Generated: 0")
                self.status_label.config(text="Ready for new batch", foreground="blue")
                self.clear_form()
                self.product_var.set("")
                self.prefix_label.config(text="")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create invoice folder:\n{str(e)}")
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=15)
        
        ttk.Button(btn_frame, text="Create Folder", 
                  command=create_invoice_folder,
                  width=15).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Cancel", 
                  command=invoice_dialog.destroy,
                  width=15).pack(side=tk.LEFT, padx=5)


def main():
    """Main entry point"""
    root = tk.Tk()
    
    # Set window icon (if available)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    app = GasClipCertificateGenerator(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
