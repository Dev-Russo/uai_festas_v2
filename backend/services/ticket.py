from io import BytesIO
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A6
from reportlab.lib.units import mm


def generate_qr_png_bytes(data: str) -> bytes:
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    bio = BytesIO()
    img.save(bio, format="PNG")
    return bio.getvalue()


def generate_qr_matrix(data: str) -> list[list[bool]]:
    qr = qrcode.QRCode(box_size=1, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.get_matrix()


def generate_ticket_pdf_bytes(sale, product, event, qr_png_bytes: bytes) -> bytes:
    """Generates a simple ticket PDF (A6) with sale/product/event info and embedded QR PNG.
    `sale`, `product`, `event` can be ORM objects or dict-like with attributes/keys.
    Returns raw PDF bytes."""
    bio = BytesIO()
    c = canvas.Canvas(bio, pagesize=A6)
    width, height = A6

    margin = 5 * mm
    x = margin
    y = height - margin

    # Title
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y - 0 * mm, f"Ticket: {getattr(sale, 'id', sale.get('id') if isinstance(sale, dict) else '')}")

    c.setFont("Helvetica", 9)
    y -= 8 * mm
    c.drawString(x, y, f"Event: {getattr(event, 'name', event.get('name') if isinstance(event, dict) else '')}")
    y -= 6 * mm
    c.drawString(x, y, f"Product: {getattr(product, 'name', product.get('name') if isinstance(product, dict) else '')}")
    y -= 6 * mm
    c.drawString(x, y, f"Buyer: {getattr(sale, 'buyer_name', sale.get('buyer_name') if isinstance(sale, dict) else '')}")
    y -= 6 * mm
    c.drawString(x, y, f"CPF: {getattr(sale, 'buyer_cpf', sale.get('buyer_cpf') if isinstance(sale, dict) else '')}")
    y -= 6 * mm
    c.drawString(x, y, f"Price: R$ {getattr(sale, 'price', sale.get('price') if isinstance(sale, dict) else '')}")

    # Draw QR as vector (modules) at bottom-right for lossless PDF
    try:
        matrix = generate_qr_matrix(str(getattr(sale, 'unique_code', sale.get('unique_code') if isinstance(sale, dict) else '')))
        n = len(matrix)
        if n > 0:
            target_size = 40 * mm
            module_size = target_size / n
            qr_x = width - margin - target_size
            qr_y = margin

            c.setFillColorRGB(0, 0, 0)
            c.setStrokeColorRGB(0, 0, 0)
            for r in range(n):
                for col in range(n):
                    if matrix[r][col]:
                        x_pos = qr_x + col * module_size
                        y_pos = qr_y + (n - 1 - r) * module_size
                        c.rect(x_pos, y_pos, module_size, module_size, stroke=0, fill=1)
    except Exception:
        # fallback to raster embedding if vector drawing fails
        try:
            from PIL import Image
            from reportlab.lib.utils import ImageReader

            qr_img = Image.open(BytesIO(qr_png_bytes)).convert("RGBA")
            target_w = target_h = int(40 * mm)
            qr_img = qr_img.resize((target_w, target_h))
            qr_buf = BytesIO()
            qr_img.save(qr_buf, format="PNG")
            qr_buf.seek(0)

            img_reader = ImageReader(qr_buf)
            c.drawImage(img_reader, width - margin - target_w, margin, width=target_w, height=target_h)
        except Exception:
            pass

    c.showPage()
    c.save()
    bio.seek(0)
    return bio.read()
