import os
from django.conf import settings
from vitec.models import Service_Order, Instrument, Institution
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from django.http import HttpResponse
import io
from reportlab.lib.colors import HexColor




def draw_header_footer(canvas, doc):
    
    # Draw letterhead on every page
    letterhead_image_path = os.path.join(settings.BASE_DIR, 'static/images/vitec_so_letterhead.jpg') # Update to actual path

    # Set the image width to the full page width minus margins
    page_width, page_height = A4  # A4 size in points (595.27, 841.89)
    left_margin, right_margin = doc.leftMargin, doc.rightMargin
    letterhead_width = page_width - left_margin - right_margin

    # Position the image at the top with adjusted width
    canvas.drawImage(letterhead_image_path, left_margin, page_height - 140, width=letterhead_width, height=120, preserveAspectRatio=True)

    # Draw footer with page number
    page_number = canvas.getPageNumber()
    canvas.setFont("Helvetica", 11)
    canvas.drawRightString(doc.width + 30, 20, f"Page {page_number}")

# Create Tables
def create_table(data, headers, doc):
    table_data = [headers] + data
    page_width, page_height = A4
    total_width = page_width - doc.leftMargin - doc.rightMargin

    # Calculate dynamic column widths
    num_columns = len(headers)
    first_col_width = 30  # Fixed width for the "#" column
    remaining_width = total_width - first_col_width
    other_col_width = remaining_width / (num_columns - 1)

    col_widths = [first_col_width] + [other_col_width] * (num_columns - 1)

    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#f2f2f2")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),  # Increase top padding
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, HexColor("#E8E8E8")),
    ]))

    # Ensure the headers are repeated on each page if the table spans multiple pages
    table._argW[0] = 30  # Adjust for the first column width
    table.splitByRow = True  # Allow splitting the table rows
    table.repeatRows = True  # Repeat the header row
    return table
    
def create_so_pdf(so_number):
    service_order = get_object_or_404(Service_Order, so_number=so_number)
    instruments = Instrument.objects.filter(id__in=service_order.instrument_list)
    institution = Institution.objects.get(name=service_order.institution)

    pipettes = [i.pipette for i in instruments if i.instrument_type == "Pipette"]
    rpms = [i.rpm for i in instruments if i.instrument_type == "RPM"]
    temperatures = [i.temperature for i in instruments if i.instrument_type == "Temperature"]
    microscopes = [i.microscope for i in instruments if i.instrument_type == "Microscope"]
    timers = [i.timer for i in instruments if i.instrument_type == "Timer"]
    thermoRPMs = [i.thermorpm for i in instruments if i.instrument_type == "ThermoRPM"]

    phone_number = f"({institution.phone_number[:3]}) {institution.phone_number[3:6]}-{institution.phone_number[6:]}"
    date = service_order.date.strftime("%m/%d/%Y")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=140, bottomMargin=50)
    elements = []

    styles = getSampleStyleSheet()
    header_style = styles['Heading1']

    custom_style = ParagraphStyle(
        name='CustomStyle',
        fontName='Helvetica',
        fontSize=12,  # 12 points is approximately 16px
    )

    # Define the data with bold labels
    details_data = [
        [Paragraph(f"<b>Date:</b> {date}", custom_style), Paragraph(f"<b>INV#:</b> {service_order.so_number}", custom_style)],
        [Paragraph(f"<b>Institution:</b> {service_order.institution}", custom_style), Paragraph(f"<b>Contact:</b> {institution.contact}", custom_style)],
        [Paragraph(f"<b>Department:</b> {service_order.department or 'N/A'}", custom_style), Paragraph(f"<b>Email:</b> {institution.email}", custom_style)],
        [Paragraph(f"<b>Additional Contact:</b> {service_order.additional_contact or 'N/A'}", custom_style), Paragraph(f"<b>Phone:</b> {phone_number}", custom_style)],
        [Paragraph(f"<b>Address:</b> {institution.address}", custom_style), None]
    ]

    details_table = Table(details_data, colWidths=[doc.width / 2 + 30, doc.width / 2 - 30])
    details_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),  # Remove extra padding to align with left margin
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),  # Optional: Ensure symmetry
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7.5),
    ]))

    elements.append(details_table)
    elements.append(Spacer(1, 12))

    header_style = ParagraphStyle(
    name='NoMarginHeader',
    parent=styles['Heading1'],  # Use the base Heading1 style
    leftIndent=-6.5,               # Ensure no additional left indent
    fontName='Helvetica-Bold',  # Regular weight instead of bold
    fontSize=16,
    )


    if pipettes:
        pipette_data = [[str(i+1), p.id, p.make, p.pipette_type, p.volume] for i, p in enumerate(pipettes)]
        elements.append(Paragraph("Pipettes", header_style))
        elements.append(create_table(pipette_data, ["#", "ID", "Make", "Pipette Type", "Volume"], doc))
        elements.append(Spacer(1, 24))

    if rpms:
        rpm_data = [[str(i+1), r.id, r.make, r.model, r.rpm_type] for i, r in enumerate(rpms)]
        elements.append(Paragraph("RPMs", header_style))
        elements.append(create_table(rpm_data, ["#", "ID", "Make", "Model", "RPM Type"], doc))
        elements.append(Spacer(1, 24))

    if temperatures:
        temp_data = [[str(i+1), t.id, t.make, t.model, t.temperature_type] for i, t in enumerate(temperatures)]
        elements.append(Paragraph("Temperatures", header_style))
        elements.append(create_table(temp_data, ["#", "ID", "Make", "Model", "Temperature Type"], doc))
    
    if microscopes:
        mircroscope_data = [[str(i+1), m.id, m.make, m.model, m.microscope_type] for i, m in enumerate(microscopes)]
        elements.append(Paragraph("Microscopes", header_style))
        elements.append(create_table(mircroscope_data, ["#", "ID", "Make", "Model", "Microscope Type"], doc))
        elements.append(Spacer(1, 24))
    
    if timers:
        timer_data = [[str(i+1), t.id, t.make, t.model, t.timer_type] for i, t in enumerate(timers)]
        elements.append(Paragraph("Timers", header_style))
        elements.append(create_table(timer_data, ["#", "ID", "Make", "Model", "Timer Type"], doc))
        elements.append(Spacer(1, 24))
    
    if thermoRPMs:
        timer_data = [[str(i+1), t.id, t.make, t.model, t.thermoRPM_type] for i, t in enumerate(thermoRPMs)]
        elements.append(Paragraph("ThermoRPMs", header_style))
        elements.append(create_table(timer_data, ["#", "ID", "Make", "Model", "ThermoRPM Type"], doc))
        elements.append(Spacer(1, 24))

    

    # Add Header/Footer Template
    doc.build(elements, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="service_order_{so_number}.pdf"'
    response['Content-Description'] = 'File Transfer'
    response['Content-Type'] = 'application/pdf'
    response.write(buffer.getvalue())
    buffer.close()

    return response
