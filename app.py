#!/usr/bin/env python3
"""
GasClip Certificates Generator - v3.3 Improved Value Positioning
Desktop application for generating calibration test certificates for GasClip gas detectors.
Features: Precise text positioning with two-step overlay (white underlay + text overlay)
to properly cover original template values while preserving labels.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import shutil
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, white
import io
from product_coordinates import get_coordinates


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

        text = self.get().replace('/', '')

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
            formatted = text[:2]
            if len(text) >= 4:
                formatted += '/' + text[2:4]
                if len(text) >= 5:
                    formatted += '/' + text[4:8]
            elif len(text) > 2:
                formatted += '/' + text[2:]

        # Update the entry
        cursor_pos = self.index(tk.INSERT)
        self.delete(0, tk.END)
        self.insert(0, formatted)

        # Adjust cursor position after slashes
        if len(text) == 2 or len(text) == 4:
            cursor_pos += 1
        self.icursor(min(cursor_pos, len(formatted)))

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
        self.root.title("GasClip Certificates Generator v3.3")
        self.root.geometry("750x750")
        self.root.resizable(False, False)

        # Product configurations
        self.products = {
            "MGC-S+ (MGC-SIMPLEPLUS)": {
                "prefix": "D4PQ",
                "template": "D4PQ236599.pdf",
                "detector_life": 36,
                "calibration_days": 1095,
            },
            "SGC-O (Single Gas Clip O2)": {
                "prefix": "SOSP",
                "template": "SOSP215459.pdf",
                "detector_life": 24,
                "calibration_days": 730,
            },
            "SGC-C (Single Gas Clip CO)": {
                "prefix": "SCSQ",
                "template": "SCSQ175392.pdf",
                "detector_life": 24,
                "calibration_days": 730,
            },
            "MGC-S (MGC-SIMPLE)": {
                "prefix": "D4SQ",
                "template": "D4SQ106733.pdf",
                "detector_life": 24,
                "calibration_days": 730,
            },
            "SGC-H (Single Gas Clip H2S)": {
                "prefix": "SHSP",
                "template": "SHSP085112.pdf",
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

        title_label = ttk.Label(main_frame, text="GasClip Certificate Generator v3.3",
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
        ttk.Label(main_frame, text="Type: 26022025 -> Auto-formats to: 26/02/2025",
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
        ttk.Label(main_frame, text="Type: 19102023 -> Auto-formats to: 19/10/2023",
                  font=("Arial", 9), foreground="gray").grid(
            row=11, column=1, sticky=tk.W, padx=(10, 0))

        ttk.Label(main_frame, text="Calibration Date:", font=("Arial", 11)).grid(
            row=12, column=0, sticky=tk.W, pady=5)
        self.calibration_entry = DateEntry(main_frame, width=47, font=("Arial", 10))
        self.calibration_entry.grid(row=12, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.entry_widgets.append(self.calibration_entry)
        ttk.Label(main_frame, text="Type: 26022024 -> Auto-formats to: 26/02/2024",
                  font=("Arial", 9), foreground="gray").grid(
            row=13, column=1, sticky=tk.W, padx=(10, 0))

        ttk.Separator(main_frame, orient='horizontal').grid(
            row=14, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=15, column=0, columnspan=2, pady=10)

        generate_btn = ttk.Button(button_frame, text="Generate Certificate",
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

        finish_btn = ttk.Button(main_frame, text="Finish All Forms & Create Invoice Folder",
                               command=self.finish_all_forms,
                               width=50)
        finish_btn.grid(row=19, column=0, columnspan=2, pady=10)

        info_label = ttk.Label(main_frame,
                              text="Tip: Press Enter to move to next field, Up/Down arrows to navigate",
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

    def format_date_for_boxes(self, date_str):
        """Convert DD/MM/YYYY to DD.MM.YYYY for the digit boxes"""
        return date_str.replace('/', '.')

    def draw_covered_text(self, can, x, y, text, font_size, cover_x, cover_w, cover_h, font_name="Helvetica-Bold"):
        """Draw text with white rectangle coverage underneath"""
        # Draw white rectangle to cover old text (positioned independently)
        can.setFillColor(white)
        can.rect(cover_x, y - 4, cover_w, cover_h, fill=1, stroke=0)

        # Draw new text
        can.setFillColor(black)
        can.setFont(font_name, font_size)
        can.drawString(x, y, text)

    def draw_date_in_boxes(self, can, start_x, y, date_str, spacing, font_size):
        """Draw date characters in individual boxes (DD.MM.YYYY format)"""
        # Convert to DD.MM.YYYY format (10 characters)
        formatted_date = self.format_date_for_boxes(date_str)

        can.setFillColor(black)
        can.setFont("Helvetica-Bold", font_size)

        for i, char in enumerate(formatted_date):
            x = start_x + (i * spacing)
            # Center each character in its box (adjust x slightly for centering)
            char_offset = 3 if char == '.' else 2
            can.drawString(x + char_offset, y, char)

    def create_white_underlay(self, prefix):
        """Create PDF with white rectangles to cover original text values only"""
        coords = get_coordinates(prefix)

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)

        # PAGE 1 - Draw white rectangles to cover variable text values
        p1 = coords["page1"]
        can.setFillColor(white)

        # Cover serial number area
        can.rect(p1["serial"]["cover_x"], p1["serial"]["y"] - 4,
                 p1["serial"]["cover_w"], p1["serial"]["cover_h"], fill=1, stroke=0)

        # Cover activation date area (just the date value)
        can.rect(p1["activation_date"]["cover_x"], p1["activation_date"]["y"] - 3,
                 p1["activation_date"]["cover_w"], p1["activation_date"]["cover_h"], fill=1, stroke=0)

        # Cover lot number area
        can.rect(p1["lot"]["cover_x"], p1["lot"]["y"] - 4,
                 p1["lot"]["cover_w"], p1["lot"]["cover_h"], fill=1, stroke=0)

        # Cover gas production date area (just the date value)
        can.rect(p1["gas_prod"]["cover_x"], p1["gas_prod"]["y"] - 3,
                 p1["gas_prod"]["cover_w"], p1["gas_prod"]["cover_h"], fill=1, stroke=0)

        # Cover calibration date area
        can.rect(p1["calibration"]["cover_x"], p1["calibration"]["y"] - 4,
                 p1["calibration"]["cover_w"], p1["calibration"]["cover_h"], fill=1, stroke=0)

        can.showPage()

        # PAGE 2 - Cover serial number area
        p2 = coords["page2"]
        can.setFillColor(white)
        can.rect(p2["serial"]["cover_x"], p2["serial"]["y"] - 4,
                 p2["serial"]["cover_w"], p2["serial"]["cover_h"], fill=1, stroke=0)

        can.save()
        packet.seek(0)
        return packet

    def create_text_overlay(self, data, prefix):
        """Create PDF overlay with just the new text (no white rectangles)"""
        coords = get_coordinates(prefix)

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)

        # ============ PAGE 1 ============
        p1 = coords["page1"]

        # Serial number
        can.setFillColor(black)
        can.setFont("Helvetica-Bold", p1["serial"]["size"])
        can.drawString(p1["serial"]["x"], p1["serial"]["y"], data["serial"])

        # Activation date
        can.setFont("Helvetica", p1["activation_date"]["size"])
        can.drawString(p1["activation_date"]["x"], p1["activation_date"]["y"], data["activation"])

        # Lot number
        can.setFont("Helvetica-Bold", p1["lot"]["size"])
        can.drawString(p1["lot"]["x"], p1["lot"]["y"], data["lot"])

        # Gas production date
        can.setFont("Helvetica", p1["gas_prod"]["size"])
        can.drawString(p1["gas_prod"]["x"], p1["gas_prod"]["y"], data["gas_prod"])

        # Calibration date
        can.setFont("Helvetica-Bold", p1["calibration"]["size"])
        can.drawString(p1["calibration"]["x"], p1["calibration"]["y"], data["calibration"])

        can.showPage()

        # ============ PAGE 2 ============
        p2 = coords["page2"]

        # Serial number
        can.setFillColor(black)
        can.setFont("Helvetica-Bold", p2["serial"]["size"])
        can.drawString(p2["serial"]["x"], p2["serial"]["y"], data["serial"])

        # Activation date in boxes (DD.MM.YYYY)
        act_boxes = p2["activation_boxes"]
        self.draw_date_in_boxes(
            can, act_boxes["x"], act_boxes["y"],
            data["activation"], act_boxes["spacing"], act_boxes["size"]
        )

        # Expiration date in boxes (DD.MM.YYYY)
        exp_boxes = p2["expiration_boxes"]
        self.draw_date_in_boxes(
            can, exp_boxes["x"], exp_boxes["y"],
            data["calibration_exp"], exp_boxes["spacing"], exp_boxes["size"]
        )

        can.save()
        packet.seek(0)
        return packet

    def generate_certificate(self):
        """Generate the PDF certificate with text overlay"""
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

            # Step 1: Create white underlay to cover original text
            white_underlay = self.create_white_underlay(product_info["prefix"])

            # Step 2: Create text overlay with new values
            text_overlay = self.create_text_overlay(data, product_info["prefix"])

            # Step 3: Merge in order: template -> white underlay -> text
            template_pdf = PdfReader(str(template_path))
            underlay_reader = PdfReader(white_underlay)
            overlay_reader = PdfReader(text_overlay)
            writer = PdfWriter()

            for i, page in enumerate(template_pdf.pages):
                # First merge white rectangles to cover old text
                if i < len(underlay_reader.pages):
                    page.merge_page(underlay_reader.pages[i])
                # Then merge new text on top
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
                text=f"Certificate generated: {output_filename}",
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
                    f"All {moved_count} certificates have been organized!\n\n"
                    f"Folder: {invoice_folder.name}\n"
                    f"Location: {invoice_folder.absolute()}\n\n"
                    f"You can now:\n"
                    f"- Close the application\n"
                    f"- Start a new batch of certificates")

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
