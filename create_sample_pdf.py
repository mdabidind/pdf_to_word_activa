from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

def create_sample_pdf(output_path="sample.pdf"):
    """Create a sample PDF file for testing the converter"""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=1,  # Center alignment
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=10
    )
    
    # Create content elements
    elements = []
    
    # Title
    elements.append(Paragraph("Sample PDF Document for Conversion Testing", title_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Introduction
    elements.append(Paragraph("Introduction", heading_style))
    elements.append(Paragraph(
        "This is a sample PDF document created for testing the PDF to Word conversion functionality. "
        "It contains various elements like paragraphs, tables, and formatting to test how well "
        "the conversion preserves these elements.", 
        normal_style
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    # Sample text with formatting
    elements.append(Paragraph("Formatted Text Examples", heading_style))
    elements.append(Paragraph(
        "This paragraph contains <b>bold text</b>, <i>italic text</i>, and <u>underlined text</u> "
        "to test how formatting is preserved during conversion.", 
        normal_style
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    # Table
    elements.append(Paragraph("Sample Table", heading_style))
    data = [
        ['Header 1', 'Header 2', 'Header 3'],
        ['Row 1, Col 1', 'Row 1, Col 2', 'Row 1, Col 3'],
        ['Row 2, Col 1', 'Row 2, Col 2', 'Row 2, Col 3'],
        ['Row 3, Col 1', 'Row 3, Col 2', 'Row 3, Col 3']
    ]
    table = Table(data, colWidths=[2*inch, 2*inch, 2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.2*inch))
    
    # List
    elements.append(Paragraph("Sample List", heading_style))
    elements.append(Paragraph("This is a bulleted list:", normal_style))
    elements.append(Paragraph("• Item 1", normal_style))
    elements.append(Paragraph("• Item 2", normal_style))
    elements.append(Paragraph("• Item 3", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Numbered list
    elements.append(Paragraph("This is a numbered list:", normal_style))
    elements.append(Paragraph("1. First item", normal_style))
    elements.append(Paragraph("2. Second item", normal_style))
    elements.append(Paragraph("3. Third item", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Conclusion
    elements.append(Paragraph("Conclusion", heading_style))
    elements.append(Paragraph(
        "This sample PDF document demonstrates various elements that can be tested during "
        "the PDF to Word conversion process. The quality of the conversion can be assessed "
        "by comparing how well these elements are preserved in the resulting Word document.", 
        normal_style
    ))
    
    # Build the PDF
    doc.build(elements)
    print(f"Sample PDF created at: {os.path.abspath(output_path)}")
    return os.path.abspath(output_path)

if __name__ == "__main__":
    create_sample_pdf()