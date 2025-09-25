
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import datetime
import os

class ReceiptGenerator:
    def __init__(self):
        self.receipt_count = 0
    
    def generate_receipt(self, sale_data):
        """สร้างใบเสร็จรับเงิน"""
        # สร้างชื่อไฟล์
        filename = f"receipts/{sale_data['receipt_no']}.pdf"
        
        # สร้าง PDF
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        
        # ข้อมูลบริษัท
        self.draw_header(c, width, height, sale_data)
        
        # รายการสินค้า
        self.draw_items(c, width, height, sale_data)
        
        # ยอดรวม
        self.draw_totals(c, width, height, sale_data)
        
        # ท้ายใบเสร็จ
        self.draw_footer(c, width, height)
        
        c.save()
        return filename
    
    def draw_header(self, c, width, height, sale_data):
        """วาดส่วนหัวใบเสร็จ"""
        # ชื่อร้าน
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width/2, height - 50, "PAYMA STORE")
        
        c.setFont("Helvetica", 10)
        c.drawCentredString(width/2, height - 70, "123 ถนนพายมา แขวงพายมา เขตพายมา กรุงเทพ 10100")
        c.drawCentredString(width/2, height - 85, "โทร: 02-123-4567 | อีเมล: info@payma.com")
        
        # เส้นคั่น
        c.line(50, height - 100, width - 50, height - 100)
        
        # ข้อมูลใบเสร็จ
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 120, "ใบเสร็จรับเงิน")
        
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 140, f"เลขที่: {sale_data['receipt_no']}")
        c.drawString(50, height - 155, f"วันที่: {sale_data['date']}")
        
        c.drawString(width - 150, height - 140, "ผู้ขาย: Payma System")
        c.drawString(width - 150, height - 155, "ผู้ซื้อ: ลูกค้าทั่วไป")
        
        # เส้นคั่น
        c.line(50, height - 170, width - 50, height - 170)
    
    def draw_items(self, c, width, height, sale_data):
        """วาดรายการสินค้า"""
        # หัวข้อตาราง
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, height - 190, "ลำดับ")
        c.drawString(100, height - 190, "รายการสินค้า")
        c.drawString(width - 150, height - 190, "จำนวน")
        c.drawString(width - 80, height - 190, "ราคา")
        
        c.line(50, height - 195, width - 50, height - 195)
        
        # รายการสินค้า
        y_position = height - 210
        for i, item in enumerate(sale_data['items'], 1):
            c.setFont("Helvetica", 9)
            c.drawString(50, y_position, str(i))
            c.drawString(100, y_position, item['name'])
            c.drawString(width - 150, y_position, "1")
            c.drawString(width - 80, y_position, f"{item['price']:,.2f}")
            y_position -= 15
            
            if y_position < 100:  # ขึ้นหน้าใหม่ถ้าเนื้อที่ไม่พอ
                c.showPage()
                y_position = height - 50
        
        return y_position
    
    def draw_totals(self, c, width, height, sale_data):
        """วาดส่วนยอดรวม"""
        # คำนวณยอดรวมต่างๆ
        subtotal = sale_data['total']
        tax_amount = subtotal * (sale_data['tax_rate'] / 100)
        grand_total = subtotal + tax_amount
        
        y_position = 300  # ตำแหน่งเริ่มต้น
        
        c.setFont("Helvetica", 10)
        c.drawString(width - 150, y_position, "ยอดรวมก่อนภาษี:")
        c.drawString(width - 80, y_position, f"{subtotal:,.2f}")
        
        c.drawString(width - 150, y_position - 15, f"ภาษีมูลค่าเพิ่ม {sale_data['tax_rate']}%:")
        c.drawString(width - 80, y_position - 15, f"{tax_amount:,.2f}")
        
        c.line(width - 150, y_position - 20, width - 50, y_position - 20)
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(width - 150, y_position - 35, "ยอดรวมสุทธิ:")
        c.drawString(width - 80, y_position - 35, f"{grand_total:,.2f}")
        
        # ตัวเลขเป็นตัวหนังสือ (แบบง่ายๆ)
        c.setFont("Helvetica", 9)
        thai_baht = self.number_to_thai_baht(grand_total)
        c.drawString(50, y_position - 50, f"ตัวอักษร: {thai_baht}")
    
    def draw_footer(self, c, width, height):
        """วาดส่วนท้ายใบเสร็จ"""
        c.setFont("Helvetica", 8)
        c.drawCentredString(width/2, 100, "ขอบคุณที่ใช้บริการ Payma")
        c.drawCentredString(width/2, 85, "ใบเสร็จนี้เป็นหลักฐานการชำระเงินที่ถูกต้อง")
        c.drawCentredString(width/2, 70, "โปรดเก็บใบเสร็จนี้ไว้เป็นหลักฐานในการเคลมสินค้า")
        
        # ลายเซ็น
        c.line(width/2 - 100, 50, width/2 - 50, 50)
        c.drawCentredString(width/2 - 75, 40, "ผู้รับเงิน")
        
        c.line(width/2 + 50, 50, width/2 + 100, 50)
        c.drawCentredString(width/2 + 75, 40, "ลูกค้า")
    
    def number_to_thai_baht(self, amount):
        """แปลงตัวเลขเป็นตัวหนังสือภาษาไทย (แบบง่าย)"""
        units = ['', 'สิบ', 'ร้อย', 'พัน', 'หมื่น', 'แสน', 'ล้าน']
        numbers = ['ศูนย์', 'หนึ่ง', 'สอง', 'สาม', 'สี่', 'ห้า', 'หก', 'เจ็ด', 'แปด', 'เก้า']
        
        if amount == 0:
            return "ศูนย์บาทถ้วน"
        
        # แยกส่วนบาทและสตางค์
        baht = int(amount)
        satang = int(round((amount - baht) * 100))
        
        # แปลงส่วนบาท
        if baht == 0:
            baht_text = ""
        else:
            baht_text = self.convert_number(baht) + "บาท"
        
        # แปลงส่วนสตางค์
        if satang == 0:
            satang_text = "ถ้วน"
        else:
            satang_text = self.convert_number(satang) + "สตางค์"
        
        return baht_text + satang_text
    
    def convert_number(self, num):
        """แปลงตัวเลขเป็นตัวหนังสือ"""
        if num == 0:
            return ""
        
        numbers = ['', 'หนึ่ง', 'สอง', 'สาม', 'สี่', 'ห้า', 'หก', 'เจ็ด', 'แปด', 'เก้า']
        units = ['', 'สิบ', 'ร้อย', 'พัน', 'หมื่น', 'แสน', 'ล้าน']
        
        text = ""
        num_str = str(num)
        length = len(num_str)
        
        for i, digit in enumerate(num_str):
            digit_int = int(digit)
            unit_index = length - i - 1
            
            if digit_int > 0:
                if unit_index == 1 and digit_int == 2:
                    text += "ยี่สิบ"
                elif unit_index == 1 and digit_int == 1:
                    text += "สิบ"
                else:
                    if digit_int == 1 and unit_index == 0 and i > 0:
                        text += "เอ็ด"
                    else:
                        text += numbers[digit_int]
                    
                    if unit_index > 0:
                        text += units[unit_index]
        
        return text
