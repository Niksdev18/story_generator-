from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
import base64

def export_story_pdf(title, segments, images):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(width / 2, height - 50, title)

    y = height - 100
    pdf.setFont("Helvetica", 12)

    for idx, segment in enumerate(segments):
        text = f"Scene {idx + 1}: {segment}"
        pdf.drawString(50, y, text)
        y -= 100

        image_data = images[idx].split(",")[1]
        image_bytes = base64.b64decode(image_data)
        image_stream = BytesIO(image_bytes)

        pdf.drawInlineImage(image_stream, 50, y - 150, width=200, height=150)
        y -= 170

        if y < 100:
            pdf.showPage()
            y = height - 100

    pdf.save()
    buffer.seek(0)
    return buffer
