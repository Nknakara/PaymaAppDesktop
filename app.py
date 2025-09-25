
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import qrcode
from PIL import Image, ImageTk
import random
import datetime
import json
import os
from receipt_template import ReceiptGenerator

class PaymaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Payma - ระบบจัดการการขาย")
        self.root.geometry("1000x750")
        self.root.configure(bg='#f5f6fa')
        
        # ข้อมูลสินค้า
        self.products = [
            {"id": 1, "name": "น้ำดื่ม", "price": 10, "category": "เครื่องดื่ม", "stock": 100},
            {"id": 2, "name": "ขนมปัง", "price": 15, "category": "อาหาร", "stock": 50},
            {"id": 3, "name": "นม", "price": 20, "category": "เครื่องดื่ม", "stock": 80},
            {"id": 4, "name": "กาแฟ", "price": 25, "category": "เครื่องดื่ม", "stock": 60},
            {"id": 5, "name": "บะหมี่กึ่งสำเร็จรูป", "price": 12, "category": "อาหาร", "stock": 120},
            {"id": 6, "name": "น้ำอัดลม", "price": 18, "category": "เครื่องดื่ม", "stock": 90},
            {"id": 7, "name": "ผลไม้", "price": 30, "category": "อาหาร", "stock": 40},
            {"id": 8, "name": "ช็อคโกแลต", "price": 22, "category": "ขนม", "stock": 70},
            {"id": 9, "name": "ข้าวกล่อง", "price": 45, "category": "อาหาร", "stock": 30},
            {"id": 10, "name": "น้ำผลไม้", "price": 25, "category": "เครื่องดื่ม", "stock": 85}
        ]
        
        # รายการสินค้าในตะกร้า
        self.cart = []
        
        # ประวัติการขาย
        self.sales_history = []
        self.load_sales_history()
        
        # ระบบสร้างใบเสร็จ
        self.receipt_generator = ReceiptGenerator()
        
        # สร้างโฟลเดอร์สำหรับบันทึกไฟล์
        self.create_data_folders()
        
        # สร้าง UI
        self.create_widgets()
        
    def create_data_folders(self):
        """สร้างโฟลเดอร์สำหรับเก็บข้อมูล"""
        folders = ['receipts', 'data', 'reports']
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)
    
    def load_sales_history(self):
        """โหลดประวัติการขายจากไฟล์"""
        try:
            if os.path.exists('data/sales_history.json'):
                with open('data/sales_history.json', 'r', encoding='utf-8') as f:
                    self.sales_history = json.load(f)
        except:
            self.sales_history = []
    
    def save_sales_history(self):
        """บันทึกประวัติการขายลงไฟล์"""
        try:
            with open('data/sales_history.json', 'w', encoding='utf-8') as f:
                json.dump(self.sales_history, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def create_widgets(self):
        # ส่วนหัว
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=90)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        title_label = tk.Label(header_frame, text="🛍️ Payma - ระบบจัดการการขาย", 
                              font=("TH Sarabun New", 26, "bold"), bg='#2c3e50', fg='white')
        title_label.pack(pady=20)
        
        # เมนูหลัก
        menu_frame = tk.Frame(self.root, bg='#34495e', height=40)
        menu_frame.pack(fill=tk.X, padx=0, pady=0)
        
        menu_buttons = [
            ("🏠 หน้าหลัก", self.show_home),
            ("📊 รายงาน", self.show_reports),
            ("⚙️ ตั้งค่า", self.show_settings)
        ]
        
        for text, command in menu_buttons:
            btn = tk.Button(menu_frame, text=text, command=command,
                           bg='#34495e', fg='white', font=("TH Sarabun New", 12),
                           relief=tk.FLAT)
            btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # เฟรมหลัก
        self.main_frame = tk.Frame(self.root, bg='#f5f6fa')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # แสดงหน้าหลัก
        self.show_home()
    
    def show_home(self):
        """แสดงหน้าหลัก"""
        self.clear_main_frame()
        
        # สร้างเฟรมสำหรับหน้าหลัก
        home_frame = tk.Frame(self.main_frame, bg='#f5f6fa')
        home_frame.pack(fill=tk.BOTH, expand=True)
        
        # สถิติรวดเร็ว
        stats_frame = tk.Frame(home_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # สถิติ
        today_sales = sum(sale['total'] for sale in self.sales_history 
                         if sale['date'].startswith(datetime.datetime.now().strftime("%Y-%m-%d")))
        
        stats_data = [
            ("💰 ยอดขายวันนี้", f"{today_sales:,.2f} บาท"),
            ("📦 สินค้าทั้งหมด", f"{len(self.products)} รายการ"),
            ("🛒 การขายวันนี้", f"{len([s for s in self.sales_history if s['date'].startswith(datetime.datetime.now().strftime('%Y-%m-%d'))])} รายการ")
        ]
        
        for i, (title, value) in enumerate(stats_data):
            stat_frame = tk.Frame(stats_frame, bg=['#e8f6f3', '#fdedec', '#f4ecf7'][i])
            stat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=10)
            
            tk.Label(stat_frame, text=title, font=("TH Sarabun New", 12), 
                    bg=stat_frame['bg']).pack(pady=(5, 0))
            tk.Label(stat_frame, text=value, font=("TH Sarabun New", 16, "bold"), 
                    bg=stat_frame['bg']).pack(pady=(0, 5))
        
        # เฟรมเนื้อหาหลัก
        content_frame = tk.Frame(home_frame, bg='#f5f6fa')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # เฟรมซ้าย - รายการสินค้า
        left_frame = tk.Frame(content_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # หัวข้อสินค้า
        product_label = tk.Label(left_frame, text="📦 รายการสินค้า", 
                               font=("TH Sarabun New", 18, "bold"), 
                               bg='#3498db', fg='white', pady=10)
        product_label.pack(fill=tk.X)
        
        # ตัวกรองหมวดหมู่
        category_frame = tk.Frame(left_frame, bg='#ecf0f1')
        category_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(category_frame, text="หมวดหมู่:", font=("TH Sarabun New", 12), 
                bg='#ecf0f1').pack(side=tk.LEFT, padx=(0, 10))
        
        categories = ["ทั้งหมด"] + list(set([p["category"] for p in self.products]))
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(category_frame, textvariable=self.category_var, 
                                         values=categories, state="readonly", 
                                         font=("TH Sarabun New", 12))
        self.category_combo.set("ทั้งหมด")
        self.category_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.category_combo.bind('<<ComboboxSelected>>', self.filter_products)
        
        # พื้นที่แสดงสินค้า
        product_canvas_frame = tk.Frame(left_frame, bg='#ffffff')
        product_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.product_canvas = tk.Canvas(product_canvas_frame, bg='#ffffff')
        self.product_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(product_canvas_frame, orient="vertical", 
                               command=self.product_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.product_frame = tk.Frame(self.product_canvas, bg='#ffffff')
        self.product_canvas.create_window((0, 0), window=self.product_frame, anchor="nw")
        
        self.product_frame.bind("<Configure>", self.on_frame_configure)
        self.product_canvas.configure(yscrollcommand=scrollbar.set)
        
        # สร้างปุ่มสินค้า
        self.create_product_buttons()
        
        # เฟรมขวา - ตะกร้าสินค้า
        right_frame = tk.Frame(content_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # หัวข้อตะกร้า
        cart_label = tk.Label(right_frame, text="🛒 ตะกร้าสินค้า", 
                             font=("TH Sarabun New", 18, "bold"), 
                             bg='#2ecc71', fg='white', pady=10)
        cart_label.pack(fill=tk.X)
        
        # พื้นที่แสดงตะกร้า
        cart_display_frame = tk.Frame(right_frame, bg='#ffffff')
        cart_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # รายการสินค้าในตะกร้า
        cart_list_frame = tk.Frame(cart_display_frame, bg='#ffffff')
        cart_list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.cart_listbox = tk.Listbox(cart_list_frame, font=("TH Sarabun New", 12), height=10)
        self.cart_listbox.pack(fill=tk.BOTH, expand=True)
        
        # ปุ่มจัดการตะกร้า
        button_frame = tk.Frame(cart_display_frame, bg='#ffffff')
        button_frame.pack(fill=tk.X, pady=5)
        
        remove_btn = tk.Button(button_frame, text="ลบรายการที่เลือก", 
                              command=self.remove_from_cart,
                              bg='#e74c3c', fg='white', font=("TH Sarabun New", 11))
        remove_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_btn = tk.Button(button_frame, text="ล้างตะกร้า", 
                             command=self.clear_cart,
                             bg='#f39c12', fg='white', font=("TH Sarabun New", 11))
        clear_btn.pack(side=tk.LEFT)
        
        # แสดงยอดรวม
        self.total_label = tk.Label(cart_display_frame, text="ยอดรวม: 0.00 บาท", 
                                   font=("TH Sarabun New", 16, "bold"), 
                                   bg='#ffffff', fg='#2c3e50')
        self.total_label.pack(pady=5)
        
        # ปุ่มดำเนินการ
        action_frame = tk.Frame(cart_display_frame, bg='#ffffff')
        action_frame.pack(fill=tk.X, pady=10)
        
        qr_btn = tk.Button(action_frame, text="💰 สแกน QR Code", 
                          command=self.show_qr_code, bg='#9b59b6', fg='white', 
                          font=("TH Sarabun New", 12), width=12)
        qr_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        receipt_btn = tk.Button(action_frame, text="🧾 พิมพ์ใบเสร็จ", 
                               command=self.print_receipt, bg='#e67e22', fg='white', 
                               font=("TH Sarabun New", 12), width=12)
        receipt_btn.pack(side=tk.LEFT)
        
        # พื้นที่แสดง QR Code
        self.qr_label = tk.Label(cart_display_frame, 
                                text="QR Code จะแสดงที่นี่หลังกดชำระเงิน", 
                                bg='#ecf0f1', fg='#7f8c8d', font=("TH Sarabun New", 12), 
                                height=8, relief=tk.SUNKEN, bd=1)
        self.qr_label.pack(fill=tk.BOTH, expand=True)
    
    def show_reports(self):
        """แสดงหน้ารายงาน"""
        self.clear_main_frame()
        
        report_frame = tk.Frame(self.main_frame, bg='#f5f6fa')
        report_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(report_frame, text="📊 รายงานการขาย", 
                font=("TH Sarabun New", 24, "bold"), bg='#f5f6fa').pack(pady=20)
        
        # สร้าง Treeview สำหรับแสดงรายงาน
        columns = ("date", "receipt_no", "items", "total")
        tree = ttk.Treeview(report_frame, columns=columns, show="headings", height=15)
        
        tree.heading("date", text="วันที่")
        tree.heading("receipt_no", text="เลขที่ใบเสร็จ")
        tree.heading("items", text="จำนวนรายการ")
        tree.heading("total", text="ยอดรวม (บาท)")
        
        tree.column("date", width=120)
        tree.column("receipt_no", width=100)
        tree.column("items", width=100)
        tree.column("total", width=100)
        
        # เพิ่มข้อมูล
        for sale in self.sales_history[-20:]:  # แสดง 20 รายการล่าสุด
            tree.insert("", "end", values=(
                sale['date'],
                sale['receipt_no'],
                len(sale['items']),
                f"{sale['total']:,.2f}"
            ))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # ปุ่มส่งออกรายงาน
        export_btn = tk.Button(report_frame, text="📤 ส่งออกรายงาน PDF", 
                              command=self.export_report, bg='#27ae60', fg='white',
                              font=("TH Sarabun New", 14))
        export_btn.pack(pady=10)
    
    def show_settings(self):
        """แสดงหน้าตั้งค่า"""
        self.clear_main_frame()
        
        settings_frame = tk.Frame(self.main_frame, bg='#f5f6fa')
        settings_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(settings_frame, text="⚙️ ตั้งค่าระบบ", 
                font=("TH Sarabun New", 24, "bold"), bg='#f5f6fa').pack(pady=20)
        
        # การตั้งค่าต่างๆ
        settings = [
            ("🏪 ชื่อร้าน:", "Payma Store"),
            ("📞 เบอร์โทร:", "02-123-4567"),
            ("📧 อีเมล:", "info@payma.com"),
            ("💳 ภาษี (%):", "7")
        ]
        
        for i, (label, default) in enumerate(settings):
            frame = tk.Frame(settings_frame, bg='#f5f6fa')
            frame.pack(fill=tk.X, padx=50, pady=5)
            
            tk.Label(frame, text=label, font=("TH Sarabun New", 14), 
                    bg='#f5f6fa', width=15, anchor='e').pack(side=tk.LEFT)
            
            entry = tk.Entry(frame, font=("TH Sarabun New", 14), width=30)
            entry.insert(0, default)
            entry.pack(side=tk.LEFT, padx=10)
    
    def clear_main_frame(self):
        """ล้างเฟรมหลัก"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def on_frame_configure(self, event):
        self.product_canvas.configure(scrollregion=self.product_canvas.bbox("all"))
    
    def create_product_buttons(self):
        """สร้างปุ่มสินค้า"""
        for widget in self.product_frame.winfo_children():
            widget.destroy()
        
        selected_category = self.category_combo.get()
        if selected_category == "ทั้งหมด":
            products_to_show = self.products
        else:
            products_to_show = [p for p in self.products if p["category"] == selected_category]
        
        row, col = 0, 0
        for product in products_to_show:
            product_frame = tk.Frame(self.product_frame, bg='#ecf0f1', relief=tk.RAISED, bd=1)
            product_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            product_btn = tk.Button(product_frame, 
                                   text=f"{product['name']}\n{product['price']} บาท\nคงเหลือ: {product['stock']}",
                                   command=lambda p=product: self.add_to_cart(p),
                                   bg='#3498db', fg='white', font=("TH Sarabun New", 10),
                                   width=15, height=4)
            product_btn.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
            
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        for i in range(row + 1):
            self.product_frame.rowconfigure(i, weight=1)
        for i in range(3):
            self.product_frame.columnconfigure(i, weight=1)
    
    def filter_products(self, event=None):
        self.create_product_buttons()
    
    def add_to_cart(self, product):
        if product['stock'] > 0:
            self.cart.append(product)
            self.update_cart_display()
            messagebox.showinfo("เพิ่มสินค้า", f"เพิ่ม {product['name']} ลงในตะกร้าเรียบร้อย!")
        else:
            messagebox.showwarning("สินค้าหมด", f"{product['name']} สินค้าหมดสต็อกแล้ว")
    
    def remove_from_cart(self):
        selection = self.cart_listbox.curselection()
        if selection:
            index = selection[0]
            removed_product = self.cart.pop(index)
            self.update_cart_display()
        else:
            messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกรายการที่ต้องการลบ")
    
    def clear_cart(self):
        if self.cart:
            self.cart = []
            self.update_cart_display()
        else:
            messagebox.showwarning("แจ้งเตือน", "ตะกร้าว่างเปล่า")
    
    def update_cart_display(self):
        self.cart_listbox.delete(0, tk.END)
        
        total = 0
        for product in self.cart:
            self.cart_listbox.insert(tk.END, f"{product['name']} - {product['price']:.2f} บาท")
            total += product["price"]
        
        self.total_label.config(text=f"ยอดรวม: {total:,.2f} บาท")
    
    def show_qr_code(self):
        if not self.cart:
            messagebox.showwarning("แจ้งเตือน", "ตะกร้าว่างเปล่า กรุณาเพิ่มสินค้าก่อนชำระเงิน")
            return
        
        total = sum(product["price"] for product in self.cart)
        ref_number = random.randint(100000, 999999)
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        
        payment_data = f"""Payma - การชำระเงิน
ยอดรวม: {total:,.2f} บาท
รหัสอ้างอิง: {ref_number}
วันที่: {timestamp}

ขอบคุณที่ใช้บริการ!"""
        
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=6, border=2)
        qr.add_data(payment_data)
        qr.make(fit=True)
        
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image = qr_image.resize((200, 200), Image.Resampling.LANCZOS)
        
        self.qr_photo = ImageTk.PhotoImage(qr_image)
        self.qr_label.config(image=self.qr_photo, text="")
        
        messagebox.showinfo("ชำระเงิน", f"กรุณาสแกน QR Code เพื่อชำระเงิน\nยอดรวม: {total:,.2f} บาท")
    
    def print_receipt(self):
        if not self.cart:
            messagebox.showwarning("แจ้งเตือน", "ตะกร้าว่างเปล่า ไม่สามารถพิมพ์ใบเสร็จได้")
            return
        
        # สร้างข้อมูลการขาย
        sale_data = {
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'receipt_no': f"PM{datetime.datetime.now().strftime('%Y%m%d')}{random.randint(1000, 9999)}",
            'items': self.cart,
            'total': sum(product["price"] for product in self.cart),
            'tax_rate': 7
        }
        
        # บันทึกการขาย
        self.sales_history.append(sale_data)
        self.save_sales_history()
        
        # สร้างและพิมพ์ใบเสร็จ
        receipt_path = self.receipt_generator.generate_receipt(sale_data)
        
        # ล้างตะกร้าหลังจากพิมพ์ใบเสร็จ
        self.cart = []
        self.update_cart_display()
        self.qr_label.config(image='', text="QR Code จะแสดงที่นี่หลังกดชำระเงิน")
        
        messagebox.showinfo("พิมพ์ใบเสร็จ", f"พิมพ์ใบเสร็จเรียบร้อยแล้ว!\nเลขที่ใบเสร็จ: {sale_data['receipt_no']}")
    
    def export_report(self):
        """ส่งออกรายงานเป็น PDF"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="บันทึกรายงานเป็น PDF"
        )
        
        if filename:
            try:
                from reportlab.lib.pagesizes import A4
                from reportlab.pdfgen import canvas
                from reportlab.lib.utils import ImageReader
                from reportlab.pdfbase import pdfmetrics
                from reportlab.pdfbase.ttfonts import TTFont
                
                # สร้าง PDF
                c = canvas.Canvas(filename, pagesize=A4)
                width, height = A4
                
                # หัวข้อรายงาน
                c.setFont("Helvetica-Bold", 16)
                c.drawString(100, height - 100, "รายงานการขาย - Payma System")
                
                c.setFont("Helvetica", 12)
                c.drawString(100, height - 130, f"วันที่ออกรายงาน: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
                
                # ตารางรายงาน
                y_position = height - 180
                headers = ["วันที่", "เลขที่ใบเสร็จ", "จำนวนรายการ", "ยอดรวม (บาท)"]
                col_widths = [120, 100, 80, 80]
                
                # หัวข้อตาราง
                x_position = 100
                for i, header in enumerate(headers):
                    c.setFont("Helvetica-Bold", 10)
                    c.drawString(x_position, y_position, header)
                    x_position += col_widths[i]
                
                y_position -= 20
                
                # ข้อมูลการขาย
                c.setFont("Helvetica", 9)
                for sale in self.sales_history[-20:]:
                    x_position = 100
                    values = [
                        sale['date'],
                        sale['receipt_no'],
                        str(len(sale['items'])),
                        f"{sale['total']:,.2f}"
                    ]
                    
                    for i, value in enumerate(values):
                        c.drawString(x_position, y_position, value)
                        x_position += col_widths[i]
                    
                    y_position -= 15
                    if y_position < 100:
                        c.showPage()
                        y_position = height - 100
                
                c.save()
                messagebox.showinfo("ส่งออกรายงาน", "ส่งออกรายงานเป็น PDF เรียบร้อยแล้ว!")
                
            except Exception as e:
                messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถส่งออกรายงานได้: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PaymaApp(root)
    root.mainloop()
