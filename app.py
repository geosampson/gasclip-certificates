#!/usr/bin/env python3
"""
GasClip Certificates Generator - v4.0 Clean Templates Version
Desktop application for generating calibration test certificates for GasClip gas detectors.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import shutil
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black
import io
from product_coordinates import get_coordinates


class DateEntry(ttk.Entry):
    """Custom Entry widget with automatic date formatting (DD/MM/YYYY) - Fixed cursor jumping"""
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._last_value = ""
        self.bind('<KeyRelease>', self.format_date)
        
    def format_date(self, event):
        """Auto-format date as DD/MM/YYYY without cursor jumping"""
        # Ignore navigation keys
        if event.keysym in ('BackSpace', 'Delete', 'Left', 'Right', 'Up', 'Down', 'Tab', 'Shift_L', 'Shift_R'):
            return
        
        # Get current value and cursor position
        current = self.get()
        cursor_pos = self.index(tk.INSERT)
        
        # Remove all non-digits
        digits_only = ''.join(c for c in current if c.isdigit())
        
        # Limit to 8 digits
        if len(digits_only) > 8:
            digits_only = digits_only[:8]
        
        # Format with slashes
        if len(digits_only) <= 2:
            formatted = digits_only
        elif len(digits_only) <= 4:
            formatted = digits_only[:2] + '/' + digits_only[2:]
        else:
            formatted = digits_only[:2] + '/' + digits_only[2:4] + '/' + digits_only[4:]
        
        # Only update if changed
        if formatted != current:
            # Calculate new cursor position
            # Count slashes before cursor in old and new strings
            slashes_before_old = current[:cursor_pos].count('/')
            slashes_before_new = formatted[:cursor_pos + (formatted.count('/') - current.count('/'))].count('/')
            
            # Adjust cursor position
            new_cursor_pos = cursor_pos + (slashes_before_new - slashes_before_old)
            
            # Update entry
            self.delete(0, tk.END)
            self.insert(0, formatted)
            
            # Restore cursor position
            self.icursor(min(new_cursor_pos, len(formatted)))
        
        self._last_value = formatted
    
    def get_raw_date(self):
        """Get date without slashes (DDMMYYYY)"""
        return self.get().replace('/', '')
    
    def validate_date(self):
        """Validate if the entered date is valid"""
        date_str = self.get_raw_date()
        if len(date_str) != 8:
            return False, "Date must be 8 digits (DD/MM/YYYY)"
        
        try:
            day = int(date_str[:2])
            month = int(date_str[2:4])
            year = int(date_str[4:])
            
            if month < 1 or month > 12:
                return False, "Month must be between 01 and 12"
            if day < 1 or day > 31:
                return False, "Day must be between 01 and 31"
            if year < 2000 or year > 2100:
                return False, "Year must be between 2000 and 2100"
            
            datetime(year, month, day)
            return True, ""
        except ValueError:
            return False, "Invalid date (e.g., 31/02/2025 doesn't exist)"


class GasClipCertificateGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("GasClip Certificates Generator v4.0")
        self.root.geometry("750x750")
        self.root.resizable(False, False)
        
        # Product configurations - using clean templates
        self.products = {
            "MGC-S+ (MGC-SIMPLEPLUS)": {
                "prefix": "D4PQ",
                "template": "D4PQ236599_clean.pdf",
                "detector_life": 36,
                "calibration_days": 1095,
            },
            "SGC-O (Single Gas Clip O2)": {
                "prefix": "SOSP",
                "template": "SOSP215459_clean.pdf",
                "detector_life": 24,
                "calibration_days": 730,
            },
            "SGC-C (Single Gas Clip CO)": {
                "prefix": "SCSQ",
                "template": "SCSQ175392_clean.pdf",
                "detector_life": 24,
                "calibration_days": 730,
            },
            "MGC-S (MGC-SIMPLE)": {
                "prefix": "D4SQ",
                "template": "D4SQ106733_clean.pdf",
                "detector_life": 24,
                "calibration_days": 730,
            },
            "SGC-H (Single Gas Clip H2S)": {
                "prefix": "SHSP",
                "template": "SHSP085112_clean.pdf",
                "detector_life": 24,
                "calibration_days": 730,
            }
        }
        
        self.generated_certificates = []
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.entry_widgets = []
        
        self.setup_ui()
        self.setup_keyboard_navigation()
    
    def setup_ui(self):
        """Setup the user interface"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        title_label = ttk.Label(main_frame, text="GasClip Certificate Generator v4.0", 
                                font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        ttk.Label(main_frame, text="Select Product:", font=("Arial", 11, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.product_var = tk.StringVar()
        product_combo = ttk.Combobox(main_frame, textvariable=self.product_var, 
                                     values=list(self.products.keys()), 
                                     state="readonly", width=45)
        product_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        product_combo.bind("<<ComboboxSelected>>", self.on_product_select)
        self.entry_widgets.append(product_combo)
        
        ttk.Label(main_frame, text="Serial Number Prefix:", font=("Arial", 11)).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.prefix_label = ttk.Label(main_frame, text="", font=("Arial", 12, "bold"), 
                                      foreground="blue")
        self.prefix_label.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        
        ttk.Label(main_frame, text="Serial Number (digits only):", font=("Arial", 11)).grid(
            row=4, column=0, sticky=tk.W, pady=5)
        self.serial_entry = ttk.Entry(main_frame, width=47, font=("Arial", 10))
        self.serial_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.entry_widgets.append(self.serial_entry)
        ttk.Label(main_frame, text="Example: 175392", 
                  font=("Arial", 9), foreground="gray").grid(
            row=5, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(main_frame, text="Activation Date:", font=("Arial", 11)).grid(
            row=6, column=0, sticky=tk.W, pady=5)
        self.activation_entry = DateEntry(main_frame, width=47, font=("Arial", 10))
        self.activation_entry.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.entry_widgets.append(self.activation_entry)
        ttk.Label(main_frame, text="Type: 26022025 → Auto-formats to: 26/02/2025", 
                  font=("Arial", 9), foreground="gray").grid(
            row=7, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(main_frame, text="Lot Number:", font=("Arial", 11)).grid(
            row=8, column=0, sticky=tk.W, pady=5)
        self.lot_entry = ttk.Entry(main_frame, width=47, font=("Arial", 10))
        self.lot_entry.grid(row=8, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.entry_widgets.append(self.lot_entry)
        ttk.Label(main_frame, text="Example: CO 100ppm", 
                  font=("Arial", 9), foreground="gray").grid(
            row=9, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(main_frame, text="Gas Production Date:", font=("Arial", 11)).grid(
            row=10, column=0, sticky=tk.W, pady=5)
        self.gas_prod_entry = DateEntry(main_frame, width=47, font=("Arial", 10))
        self.gas_prod_entry.grid(row=10, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.entry_widgets.append(self.gas_prod_entry)
        ttk.Label(main_frame, text="Type: 19102023 → Auto-formats to: 19/10/2023", 
                  font=("Arial", 9), foreground="gray").grid(
            row=11, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(main_frame, text="Calibration Date:", font=("Arial", 11)).grid(
            row=12, column=0, sticky=tk.W, pady=5)
        self.calibration_entry = DateEntry(main_frame, width=47, font=("Arial", 10))
        self.calibration_entry.grid(row=12, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.entry_widgets.append(self.calibration_entry)
        ttk.Label(main_frame, text="Type: 26022024 → Auto-formats to: 26/02/2024", 
                  font=("Arial", 9), foreground="gray").grid(
            row=13, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=14, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=15, column=0, columnspan=2, pady=10)
        
        generate_btn = ttk.Button(button_frame, text="✓ Generate Certificate", 
                                  command=self.generate_certificate,
                                  width=25)
        generate_btn.grid(row=0, column=0, padx=5)
        
        clear_btn = ttk.Button(button_frame, text="Clear Form", 
                              command=self.clear_form,
                              width=15)
        clear_btn.grid(row=0, column=1, padx=5)
        
        self.status_label = ttk.Label(main_frame, text="Ready to generate certificates", 
                                      font=("Arial", 10), 
                                      foreground="blue")
        self.status_label.grid(row=16, column=0, columnspan=2, pady=5)
        
        self.counter_label = ttk.Label(main_frame, 
                                       text="Certificates Generated: 0", 
                                       font=("Arial", 11, "bold"),
                                       foreground="darkgreen")
        self.counter_label.grid(row=17, column=0, columnspan=2, pady=10)
        
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=18, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        finish_btn = ttk.Button(main_frame, text="📁 Finish All Forms & Create Invoice Folder", 
                               command=self.finish_all_forms,
                               width=50)
        finish_btn.grid(row=19, column=0, columnspan=2, pady=10)
        
        info_label = ttk.Label(main_frame, 
                              text="💡 Tip: Press Enter to move to next field, ↑↓ arrows to navigate", 
                              font=("Arial", 9), 
                              foreground="gray")
        info_label.grid(row=20, column=0, columnspan=2, pady=5)
        
        main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def setup_keyboard_navigation(self):
        """Setup Enter and Arrow key navigation"""
        for i, widget in enumerate(self.entry_widgets):
            widget.bind('<Return>', lambda e, idx=i: self.focus_next(idx))
            widget.bind('<Down>', lambda e, idx=i: self.focus_next(idx))
            widget.bind('<Up>', lambda e, idx=i: self.focus_previous(idx))
    
    def focus_next(self, current_idx):
        """Move focus to next entry widget"""
        next_idx = (current_idx + 1) % len(self.entry_widgets)
        self.entry_widgets[next_idx].focus()
        return 'break'
    
    def focus_previous(self, current_idx):
        """Move focus to previous entry widget"""
        prev_idx = (current_idx - 1) % len(self.entry_widgets)
        self.entry_widgets[prev_idx].focus()
        return 'break'
    
    def on_product_select(self, event=None):
        """Update prefix label when product is selected"""
        product = self.product_var.get()
        if product in self.products:
            prefix = self.products[product]["prefix"]
            self.prefix_label.config(text=f"{prefix}XXXXXX")
    
    def calculate_expiration_date(self, activation_date_str, days):
        """Calculate expiration date from activation date"""
        parts = activation_date_str.split('/')
        day = int(parts[0])
        month = int(parts[1])
        year = int(parts[2])
        
        activation = datetime(year, month, day)
        expiration = activation + timedelta(days=days)
        
        return expiration.strftime("%d/%m/%Y")
    
    def validate_inputs(self):
        """Validate all input fields"""
        if not self.product_var.get():
            messagebox.showerror("Error", "Please select a product")
            return False
        
        if not self.serial_entry.get() or not self.serial_entry.get().isdigit():
            messagebox.showerror("Error", "Serial number must contain only digits")
            self.serial_entry.focus()
            return False
        
        valid, msg = self.activation_entry.validate_date()
        if not valid:
            messagebox.showerror("Error", f"Activation Date: {msg}")
            self.activation_entry.focus()
            return False
        
        if not self.lot_entry.get():
            messagebox.showerror("Error", "Lot number is required")
            self.lot_entry.focus()
            return False
        
        valid, msg = self.gas_prod_entry.validate_date()
        if not valid:
            messagebox.showerror("Error", f"Gas Production Date: {msg}")
            self.gas_prod_entry.focus()
            return False
        
        valid, msg = self.calibration_entry.validate_date()
        if not valid:
            messagebox.showerror("Error", f"Calibration Date: {msg}")
            self.calibration_entry.focus()
            return False
        
        return True
    
    def create_text_overlay(self, data, prefix):
        """Create PDF overlay - NO white rectangles needed with clean templates!"""
        # Get coordinates for this product
        coords = get_coordinates(prefix)
        
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        
        # Page 1 - Cover lot placeholder, then write text
        # Cover the "O2 18%" placeholder in lot area
        can.setFillColor(white)
        can.rect(190, 400, 80, 20, fill=1, stroke=0)
        
        can.setFillColor(black)
        
        # Serial number
        p1_serial = coords["page1"]["serial"]
        can.setFont("Helvetica-Bold", int(p1_serial["size"]))
        can.drawString(p1_serial["x"], p1_serial["y"], data["serial"])
        
        # Activation date
        p1_act = coords["page1"]["activation_date"]
        can.setFont("Helvetica", int(p1_act["size"]))
        can.drawString(p1_act["x"], p1_act["y"], data["activation"])
        
        # Lot number
        p1_lot = coords["page1"]["lot"]
        can.setFont("Helvetica-Bold", int(p1_lot["size"]))
        can.drawString(p1_lot["x"], p1_lot["y"], data["lot"])
        
        # Gas production date
        p1_gas = coords["page1"]["gas_prod"]
        can.setFont("Helvetica", int(p1_gas["size"]))
        can.drawString(p1_gas["x"], p1_gas["y"], data["gas_prod"])
        
        # Calibration date
        p1_cal = coords["page1"]["calibration"]
        can.setFont("Helvetica-Bold", int(p1_cal["size"]))
        can.drawString(p1_cal["x"], p1_cal["y"], data["calibration"])
        
        can.showPage()
        
        # Page 2 - ONLY serial number, NO date boxes
        can.setFillColor(black)
        p2_serial = coords["page2"]["serial"]
        can.setFont('Helvetica-Bold', int(p2_serial["size"]))
        can.drawString(p2_serial["x"], p2_serial["y"], data["serial"])
        
        can.save()
        packet.seek(0)
        return packet
    
    def generate_certificate(self):
        """Generate the PDF certificate"""
        if not self.validate_inputs():
            return
        
        try:
            product_name = self.product_var.get()
            product_info = self.products[product_name]
            
            serial_number = product_info["prefix"] + self.serial_entry.get()
            activation_date = self.activation_entry.get()
            lot_number = self.lot_entry.get()
            gas_prod_date = self.gas_prod_entry.get()
            calibration_date = self.calibration_entry.get()
            
            calibration_exp = self.calculate_expiration_date(
                activation_date, 
                product_info["calibration_days"])
            
            data = {
                "serial": serial_number,
                "activation": activation_date,
                "lot": lot_number,
                "gas_prod": gas_prod_date,
                "calibration": calibration_date,
                "calibration_exp": calibration_exp
            }
            
            output_filename = f"{serial_number}.pdf"
            output_path = self.output_dir / output_filename
            
            # Use absolute path for template
            template_path = Path(__file__).parent / "templates" / product_info["template"]
            if not template_path.exists():
                messagebox.showerror("Error", f"Template not found: {template_path}\n\nPlease ensure the templates folder contains: {product_info['template']}")
                return
            
            # Create overlay and merge
            overlay_pdf = self.create_text_overlay(data, product_info["prefix"])
            
            template_pdf = PdfReader(str(template_path))
            overlay_reader = PdfReader(overlay_pdf)
            writer = PdfWriter()
            
            for i, page in enumerate(template_pdf.pages):
                if i < len(overlay_reader.pages):
                    page.merge_page(overlay_reader.pages[i])
                writer.add_page(page)
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            self.generated_certificates.append({
                "filename": output_filename,
                "path": str(output_path),
                "serial": serial_number,
                "product": product_name,
                "data": data
            })
            
            self.status_label.config(
                text=f"✓ Certificate generated: {output_filename}", 
                foreground="green")
            self.counter_label.config(
                text=f"Certificates Generated: {len(self.generated_certificates)}")
            
            response = messagebox.askyesno(
                "Success", 
                f"Certificate {output_filename} generated successfully!\n\n"
                f"Serial: {serial_number}\n"
                f"Activation: {activation_date}\n"
                f"Calibration Exp: {calibration_exp}\n\n"
                f"Do you want to create another certificate?")
            
            if response:
                self.clear_form()
                self.product_var.set(product_name)
                self.on_product_select()
                self.serial_entry.focus()
            else:
                finish = messagebox.askyesno(
                    "Finish?",
                    "Do you want to finish and create the invoice folder now?")
                if finish:
                    self.finish_all_forms()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate certificate:\n{str(e)}")
            import traceback
            traceback.print_exc()
    
    def clear_form(self):
        """Clear all input fields except product selection"""
        self.serial_entry.delete(0, tk.END)
        self.activation_entry.delete(0, tk.END)
        self.lot_entry.delete(0, tk.END)
        self.gas_prod_entry.delete(0, tk.END)
        self.calibration_entry.delete(0, tk.END)
    
    def finish_all_forms(self):
        """Finish all forms and create invoice folder"""
        if not self.generated_certificates:
            messagebox.showwarning("Warning", "No certificates have been generated yet!")
            return
        
        invoice_dialog = tk.Toplevel(self.root)
        invoice_dialog.title("Enter Invoice Number")
        invoice_dialog.geometry("450x180")
        invoice_dialog.resizable(False, False)
        
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
                invoice_folder = self.output_dir / f"Invoice_{invoice_number}"
                invoice_folder.mkdir(exist_ok=True)
                
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
                
                self.generated_certificates = []
                self.counter_label.config(text="Certificates Generated: 0")
                self.status_label.config(text="Ready for new batch", foreground="blue")
                self.clear_form()
                self.product_var.set("")
                self.prefix_label.config(text="")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create invoice folder:\n{str(e)}")
        
        invoice_entry.bind('<Return>', lambda e: create_invoice_folder())
        
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
    
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    app = GasClipCertificateGenerator(root)
    
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
