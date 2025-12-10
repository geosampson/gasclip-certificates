#!/usr/bin/env python3
"""
GasClip Certificates Generator - Version 2.1 with Corrected Coordinates
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import os
import shutil
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, white
import io


class DateEntry(ttk.Entry):
    """Custom Entry widget with automatic date formatting (DD/MM/YYYY)"""
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<KeyRelease>', self.format_date)
        self.bind('<BackSpace>', self.handle_backspace)
        
    def format_date(self, event):
        """Auto-format date as DD/MM/YYYY"""
        if event.keysym in ('BackSpace', 'Delete', 'Left', 'Right', 'Up', 'Down', 'Tab'):
            return

        raw_text = self.get()
        cursor_pos = self.index(tk.INSERT)

        # Count digits before the cursor to restore caret after formatting
        digits_before_cursor = ''.join(ch for ch in raw_text[:cursor_pos] if ch.isdigit())

        text = ''.join(ch for ch in raw_text if ch.isdigit())

        # Only allow digits
        if text and not text.isdigit():
            self.delete(0, tk.END)
            self.insert(0, ''.join(c for c in self.get() if c.isdigit() or c == '/'))
            return
        
        # Limit to 8 digits
        if len(text) > 8:
            text = text[:8]

        # Format with slashes
        formatted = text
        if len(text) >= 2:
            formatted = text[:2] + '/'
            if len(text) > 2:
                formatted += text[2:4]
                if len(text) > 4:
                    formatted += '/' + text[4:8]
        
        # Update the entry
        self.delete(0, tk.END)
        self.insert(0, formatted)

        # Adjust cursor position after slashes
        new_cursor = len(digits_before_cursor)
        if new_cursor >= 2:
            new_cursor += 1  # account for first slash
        if new_cursor >= 4:
            new_cursor += 1  # account for second slash

        self.icursor(min(new_cursor, len(formatted)))
    
    def handle_backspace(self, event):
        """Handle backspace to remove slashes properly"""
        cursor_pos = self.index(tk.INSERT)
        if cursor_pos > 0 and self.get()[cursor_pos-1:cursor_pos] == '/':
            self.delete(cursor_pos-2, cursor_pos)
            return 'break'
    
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
        self.root.title("GasClip Certificates Generator v2.1")
        self.root.geometry("750x750")
        self.root.resizable(False, False)
        
        # Product configurations with CORRECTED coordinates
        self.products = {
            "MGC-S+ (MGC-SIMPLEPLUS)": {
                "prefix": "D4PQ",
                "template": "D4PQ236599.pdf",
                "detector_life": 36,
                "calibration_days": 1095,
                "positions": self.get_positions_mgc_s_plus()
            },
            "SGC-O (Single Gas Clip O2)": {
                "prefix": "SOSP",
                "template": "SOSP215459.pdf",
                "detector_life": 24,
                "calibration_days": 730,
                "positions": self.get_positions_sgc_o()
            },
            "SGC-C (Single Gas Clip CO)": {
                "prefix": "SCSQ",
                "template": "SCSQ175392.pdf",
                "detector_life": 24,
                "calibration_days": 730,
                "positions": self.get_positions_sgc_c()
            },
            "MGC-S (MGC-SIMPLE)": {
                "prefix": "D4SQ",
                "template": "D4SQ106733.pdf",
                "detector_life": 24,
                "calibration_days": 730,
                "positions": self.get_positions_mgc_s()
            },
            "SGC-H (Single Gas Clip H2S)": {
                "prefix": "SHSP",
                "template": "SHSP085112.pdf",
                "detector_life": 24,
                "calibration_days": 730,
                "positions": self.get_positions_sgc_h()
            }
        }
        
        self.generated_certificates = []
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.entry_widgets = []
        
        self.setup_ui()
        self.setup_keyboard_navigation()
    
    def get_positions_sgc_o(self):
        """Get corrected positions for SGC-O template"""
        return {
            "page1": {
                "serial": (520, 727),
                "activation_before": (520, 712),
                "lot_number": (145, 475),
                "gas_production": (145, 460),
                "calibration_date": (190, 555),
            },
            "page2": {
                "serial": (520, 750),
                "activation_boxes": [
                    (545, 477), (560, 477),  # DD
                    (590, 477), (605, 477),  # MM
                    (650, 477), (665, 477), (680, 477), (695, 477)  # YYYY
                ],
                "expiration_boxes": [
                    (545, 397), (560, 397),  # DD
                    (590, 397), (605, 397),  # MM
                    (650, 397), (665, 397), (680, 397), (695, 397)  # YYYY
                ]
            }
        }
    
    def get_positions_mgc_s_plus(self):
        """Get positions for MGC-S+ template (same layout as SGC-O)"""
        return self.get_positions_sgc_o()
    
    def get_positions_sgc_c(self):
        """Get positions for SGC-C template (same layout as SGC-O)"""
        return self.get_positions_sgc_o()
    
    def get_positions_mgc_s(self):
        """Get positions for MGC-S template (same layout as SGC-O)"""
        return self.get_positions_sgc_o()
    
    def get_positions_sgc_h(self):
        """Get positions for SGC-H template (same layout as SGC-O)"""
        return self.get_positions_sgc_o()
    
    def setup_ui(self):
        """Setup the user interface"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        title_label = ttk.Label(main_frame, text="GasClip Certificate Generator v2.1", 
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
        ttk.Label(main_frame, text="Example: 236599", 
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
        ttk.Label(main_frame, text="Example: RR2310181807 or 25-3348", 
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
    
    def create_text_overlay(self, data, product_info):
        """Create a transparent PDF overlay with text at corrected positions"""
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)

        def cover_and_draw(text, x, y, font_name, font_size, padding=2, height=None):
            """Cover existing text area before drawing updated text."""
            text_width = can.stringWidth(text, font_name, font_size)
            rect_height = height if height is not None else font_size + padding

            can.setFillColor(white)
            can.rect(x - padding, y - padding, text_width + (padding * 2), rect_height, fill=1, stroke=0)
            can.setFillColor(black)
            can.setFont(font_name, int(font_size))
            can.drawString(x, y, text)

        can.setFont("Helvetica", 10)
        can.setFillColor(black)
        
        positions = product_info["positions"]
        
        # Page 1 overlays
        font_name = "Helvetica"
        font_size = 10
        cover_and_draw(data["serial"], positions["page1"]["serial"][0],
                       positions["page1"]["serial"][1], font_name, font_size, padding=3)
        cover_and_draw(data["activation"], positions["page1"]["activation_before"][0],
                       positions["page1"]["activation_before"][1], font_name, font_size, padding=2)
        cover_and_draw(data["lot"], positions["page1"]["lot_number"][0],
                       positions["page1"]["lot_number"][1], font_name, font_size, padding=3)
        cover_and_draw(data["gas_prod"], positions["page1"]["gas_production"][0],
                       positions["page1"]["gas_production"][1], font_name, font_size, padding=3)
        cover_and_draw(data["calibration"], positions["page1"]["calibration_date"][0],
                       positions["page1"]["calibration_date"][1], font_name, font_size, padding=3)
        
        can.showPage()
        
        # Page 2 overlays
        cover_and_draw(data["serial"], positions["page2"]["serial"][0],
                       positions["page2"]["serial"][1], font_name, font_size, padding=3)

        # Activation date in boxes (individual digits)
        activation_digits = data["activation"].replace('/', '')
        act_positions = positions["page2"]["activation_boxes"]
        if act_positions:
            xs = [p[0] for p in act_positions]
            min_x, max_x = min(xs), max(xs)
            y = act_positions[0][1]
            width = (max_x - min_x) + 12
            can.setFillColor(white)
            can.rect(min_x - 4, y - 4, width + 8, 16, fill=1, stroke=0)
            can.setFillColor(black)
        can.setFont("Helvetica-Bold", 12)
        for i, digit in enumerate(activation_digits):
            if i < len(act_positions):
                x, y = act_positions[i]
                can.drawString(x, y, digit)

        # Calibration expiration date in boxes
        expiration_digits = data["calibration_exp"].replace('/', '')
        exp_positions = positions["page2"]["expiration_boxes"]
        if exp_positions:
            xs = [p[0] for p in exp_positions]
            min_x, max_x = min(xs), max(xs)
            y = exp_positions[0][1]
            width = (max_x - min_x) + 12
            can.setFillColor(white)
            can.rect(min_x - 4, y - 4, width + 8, 16, fill=1, stroke=0)
            can.setFillColor(black)
        can.setFont("Helvetica-Bold", 12)
        for i, digit in enumerate(expiration_digits):
            if i < len(exp_positions):
                x, y = exp_positions[i]
                can.drawString(x, y, digit)
        
        can.save()
        packet.seek(0)
        
        return packet
    
    def generate_certificate(self):
        """Generate the PDF certificate with actual data overlay"""
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
            
            template_path = Path("templates") / product_info["template"]
            if not template_path.exists():
                messagebox.showerror("Error", f"Template not found: {template_path}")
                return
            
            overlay_pdf = self.create_text_overlay(data, product_info)
            
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
