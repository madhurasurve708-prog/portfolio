import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# --- Custom Numbered Canvas for Elegant Headers and Footers ---
class NumberedCanvas(canvas.Canvas):
    doc_title = "PROJECT SHOWCASE"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Draw a premium modern vertical color banner on the cover page
            self.saveState()
            self.setFillColor(colors.HexColor("#0f172a")) # Slate 900
            self.rect(0, 0, 18, 792, fill=True, stroke=False)
            self.setFillColor(colors.HexColor("#0d9488")) # Teal 600
            self.rect(18, 0, 6, 792, fill=True, stroke=False)
            self.restoreState()
            return
            
        self.saveState()
        # Running Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0f172a"))
        self.drawString(54, 750, self.doc_title.upper())
        
        self.setStrokeColor(colors.HexColor("#cbd5e1")) # Slate 300 divider
        self.setLineWidth(0.5)
        self.line(54, 742, 612 - 54, 742)
        
        # Running Footer
        self.line(54, 50, 612 - 54, 50)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b")) # Slate 500
        self.drawString(54, 38, "Prepared by Madhura Surve | Python Backend & AI Developer")
        
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 38, page_text)
        self.restoreState()

class SevaSetuCanvas(NumberedCanvas):
    doc_title = "CASE STUDY: SEVA SETU CIVIC PLATFORM"

class AirbnbCanvas(NumberedCanvas):
    doc_title = "PROJECT REPORT: AIRBNB FULL-STACK CLONE"

# --- Formatting Helpers ---
def cell_p(text, is_header=False):
    """Wraps text in a Paragraph style to enable text wrapping in ReportLab table cells."""
    if is_header:
        style = ParagraphStyle(
            'TableHeader',
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=12,
            textColor=colors.white
        )
    else:
        style = ParagraphStyle(
            'TableCell',
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#334155")
        )
    return Paragraph(text, style)

def make_callout(text, style):
    """Creates a stylized blockquote with a teal left border and light background."""
    p = Paragraph(text, style)
    t = Table([[p]], colWidths=[504])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LINELEFT', (0,0), (0,-1), 4, colors.HexColor("#0d9488")), # 4pt teal left border
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    return t

def make_tech_table(data):
    """Generates a structured, styled table for technical toolkits."""
    t = Table(data, colWidths=[120, 150, 234])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('TOPPADDING', (0,0), (-1,0), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,1), (-1,-1), 8),
        ('BOTTOMPADDING', (0,1), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t

# --- PDF Generation Functions ---

def generate_seva_setu_pdf():
    filename = "Seva_Setu_Case_Study.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    body_style = ParagraphStyle(
        'SSBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#334155"),
        spaceAfter=10
    )
    
    bullet_style = ParagraphStyle(
        'SSBullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=6
    )
    
    title_style = ParagraphStyle(
        'SSTitle',
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=8
    )
    
    subtitle_style = ParagraphStyle(
        'SSSubtitle',
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#475569"),
        spaceAfter=40
    )
    
    h1_style = ParagraphStyle(
        'SSH1',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=18,
        spaceAfter=10,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SSH2',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0d9488"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    meta_label = ParagraphStyle(
        'SSMetaLabel',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#64748b")
    )
    
    meta_val = ParagraphStyle(
        'SSMetaVal',
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#1e293b")
    )
    
    callout_style = ParagraphStyle(
        'SSCallout',
        parent=body_style,
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=0
    )

    story = []
    
    # --- PAGE 1: COVER PAGE ---
    story.append(Spacer(1, 40))
    story.append(Paragraph("CASE STUDY 01 — CIVIC TECH", ParagraphStyle('SSMetaCat', fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=colors.HexColor("#0d9488"), spaceAfter=15)))
    story.append(Paragraph("SEVA SETU", title_style))
    story.append(Paragraph("Digital Civic Complaint Management Platform", subtitle_style))
    
    # Ornamental separator bar
    story.append(Table([['']], colWidths=[100], rowHeights=[4], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0d9488"))]))
    story.append(Spacer(1, 200))
    
    # Metadata Block
    meta_data = [
        [Paragraph("Developer", meta_label), Paragraph("Madhura Surve", meta_val)],
        [Paragraph("Role", meta_label), Paragraph("Backend Architect & Relational Schema Designer", meta_val)],
        [Paragraph("Framework", meta_label), Paragraph("FastAPI (Python) + Supabase + React Native", meta_val)],
        [Paragraph("Status", meta_label), Paragraph("Nearing Production Launch (Local Municipal Trials)", meta_val)],
        [Paragraph("Source Code", meta_label), Paragraph("github.com/madhurasurve708-prog/seva-setu", meta_val)],
    ]
    meta_table = Table(meta_data, colWidths=[100, 404])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.HexColor("#f1f5f9")),
    ]))
    story.append(meta_table)
    story.append(PageBreak())
    
    # --- PAGE 2: CASE STUDY DETAILS ---
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "Seva Setu is a centralized complaint management platform designed to bridge the communication gap between "
        "local citizens and municipal administrators. By building a high-performance backend, modeling normalized "
        "relational schemas, and implementing seamless authentication, this system transforms messy civic processes "
        "into clear, traceable, and structured digital workflows.",
        body_style
    ))
    
    story.append(Paragraph("2. The Challenge & Core Research", h1_style))
    story.append(Paragraph(
        "Traditional civic complaint handling involves scattered phone calls, physical logs, and a lack of ticket transparency. "
        "Citizens have no way to verify if their concerns (such as road repair, waste management, or water issues) are being addressed, "
        "while municipal staff struggle with manual routing and division tracking.",
        body_style
    ))
    
    # Custom quote highlight
    research_quote = (
        "<b>Field Research Highlight:</b> To ground the system in actual workflows, user surveys were conducted with "
        "local citizens to map out resolution friction. Additionally, we collaborated directly with municipal officials "
        "to align the administrative features with actual city division operations and escalation rules."
    )
    story.append(make_callout(research_quote, callout_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("3. System Architecture & Relational Design", h1_style))
    story.append(Paragraph(
        "I designed and developed the FastAPI backend application in Python, utilizing PostgreSQL as the core relational database. "
        "The architecture is organized to enforce strict role-based access control (citizens, department representatives, ward officers, "
        "and administrators). For secure object storage, I integrated Supabase buckets to handle citizen photo evidence uploads directly "
        "upon complaint creation.",
        body_style
    ))
    
    story.append(Paragraph("4. Developer Role & Contributions", h1_style))
    story.append(Paragraph("&bull; <b>Relational Schemas:</b> Modeled and implemented database schemas mapping complex associations between citizens, complaints, departments, wards, and escalation histories.", bullet_style))
    story.append(Paragraph("&bull; <b>REST API Backend:</b> Built FastAPI service controllers, routing logic, validation layers, and custom payload handlers.", bullet_style))
    story.append(Paragraph("&bull; <b>Supabase Storage integration:</b> Programmed backend pipelines to secure file paths and upload citizen complaint photos.", bullet_style))
    story.append(Paragraph("&bull; <b>Stakeholder Alignment:</b> Transformed municipal administrative protocols into programmatic rules, enabling ward-based auto-routing.", bullet_style))
    
    story.append(PageBreak())
    
    # --- PAGE 3: TECHNICAL STACK & KEY FEATURES ---
    story.append(Paragraph("5. Featured Technology Stack", h1_style))
    
    tech_data = [
        [cell_p("Layer", True), cell_p("Technologies", True), cell_p("Core Purpose / Application", True)],
        [cell_p("Backend / REST API"), cell_p("Python, FastAPI"), cell_p("High-speed routing, validation (Pydantic), dependency injection, and API endpoint implementation.")],
        [cell_p("Database / Storage"), cell_p("PostgreSQL, Supabase"), cell_p("Relational schema storage, data normalization, transaction isolation, and secure bucket storage for media uploads.")],
        [cell_p("Mobile Front-End"), cell_p("React Native, Expo, TS"), cell_p("Cross-platform mobile application utilizing Expo modules to capture images, location data, and track ticket status (built by partner).")],
        [cell_p("Security / Access"), cell_p("JWT, Suppabase Auth"), cell_p("Role-based token validation (RBAC) ensuring secure separation between citizen features and municipal dashboards.")],
    ]
    story.append(make_tech_table(tech_data))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("6. Key Platform Capabilities", h1_style))
    story.append(Paragraph("The backend application implements several key functional workflows:", body_style))
    
    story.append(Paragraph("&bull; <b>Citizen Authentication & Session Management:</b> Secure login mechanisms for citizens to manage their ticket registry.", bullet_style))
    story.append(Paragraph("&bull; <b>Interactive Complaint Registry:</b> API pathways enabling complaints to be filed with descriptions, department tags, and photo attachments.", bullet_style))
    story.append(Paragraph("&bull; <b>Automated Ward-Based Routing:</b> Logic mapping complaint coordinates to specific ward jurisdiction tables, sending alerts to corresponding ward officials.", bullet_style))
    story.append(Paragraph("&bull; <b>Official Dashboards & Escalation:</b> Web pathways for department representatives to accept tickets, post updates, or escalate to senior officers.", bullet_style))
    story.append(Paragraph("&bull; <b>Real-Time Progress Updates:</b> Citizen tracking routes mapping ticket lifecycle status (Submitted &rarr; In Progress &rarr; Resolved).", bullet_style))
    
    story.append(Paragraph("7. Project Results & Current Status", h1_style))
    result_text = (
        "<b>Current Status:</b> Seva Setu has successfully transitioned from an initial concept prototype "
        "to a field-vetted digital platform. The REST API backend has been fully tested, and the integrated mobile application "
        "is currently nearing its official production launch, scheduled for trial runs in local municipal wards."
    )
    story.append(make_callout(result_text, callout_style))
    
    doc.build(story, canvasmaker=SevaSetuCanvas)


def generate_airbnb_pdf():
    filename = "Airbnb_Clone_Project_Report.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    body_style = ParagraphStyle(
        'ABBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#334155"),
        spaceAfter=10
    )
    
    bullet_style = ParagraphStyle(
        'ABBullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=6
    )
    
    title_style = ParagraphStyle(
        'ABTitle',
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=8
    )
    
    subtitle_style = ParagraphStyle(
        'ABSubtitle',
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#475569"),
        spaceAfter=40
    )
    
    h1_style = ParagraphStyle(
        'ABH1',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=18,
        spaceAfter=10,
        keepWithNext=True
    )
    
    meta_label = ParagraphStyle(
        'ABMetaLabel',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#64748b")
    )
    
    meta_val = ParagraphStyle(
        'ABMetaVal',
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#1e293b")
    )
    
    callout_style = ParagraphStyle(
        'ABCallout',
        parent=body_style,
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=0
    )

    story = []
    
    # --- PAGE 1: COVER PAGE ---
    story.append(Spacer(1, 40))
    story.append(Paragraph("PROJECT SHOWCASE 02 — FULL STACK", ParagraphStyle('ABMetaCat', fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=colors.HexColor("#0d9488"), spaceAfter=15)))
    story.append(Paragraph("AIRBNB CLONE", title_style))
    story.append(Paragraph("Full-Stack Property Booking Application", subtitle_style))
    
    # Ornamental separator bar
    story.append(Table([['']], colWidths=[100], rowHeights=[4], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0d9488"))]))
    story.append(Spacer(1, 200))
    
    # Metadata Block
    meta_data = [
        [Paragraph("Developer", meta_label), Paragraph("Madhura Surve", meta_val)],
        [Paragraph("Architecture", meta_label), Paragraph("Full-Stack MERN (MongoDB, Express, React, Node)", meta_val)],
        [Paragraph("Focus Area", meta_label), Paragraph("Session Authentication & Database Schema Workflows", meta_val)],
        [Paragraph("Status", meta_label), Paragraph("Completed Project / Learning Milestone", meta_val)],
        [Paragraph("Source Code", meta_label), Paragraph("github.com/madhurasurve708-prog/airbnb-clone", meta_val)],
    ]
    meta_table = Table(meta_data, colWidths=[100, 404])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.HexColor("#f1f5f9")),
    ]))
    story.append(meta_table)
    story.append(PageBreak())
    
    # --- PAGE 2: PROJECT DETAILS ---
    story.append(Paragraph("1. Project Overview", h1_style))
    story.append(Paragraph(
        "This project is a full-stack property booking application built to mimic the core features of Airbnb. "
        "The goal of this implementation was to master database-driven web application architecture, session "
        "management, API route design, and dynamic component styling. The application allows users to sign up, "
        "authenticate, browse available property listings, view detail pages, and execute reservation workflows.",
        body_style
    ))
    
    story.append(Paragraph("2. MERN Stack Architecture", h1_style))
    story.append(Paragraph(
        "The application is structured into decoupled client and server layers. The client is a single-page application "
        "built in React that makes asynchronous API requests to a Node.js/Express.js backend server. The backend processes "
        "queries, implements validation, and coordinates transactions with a MongoDB database using an Object-Document Mapper (ODM).",
        body_style
    ))
    
    # Custom note
    stack_note = (
        "<b>Architecture Focus:</b> Decoupling the front-end layout from the backend routing allowed me to focus on "
        "building strict RESTful controllers. By handling session authentication and protected API endpoints, "
        "the application ensures that only registered users can book properties or create custom listings."
    )
    story.append(make_callout(stack_note, callout_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("3. Technical Stack Table", h1_style))
    
    tech_data = [
        [cell_p("MERN Layer", True), cell_p("Technologies", True), cell_p("Core Role / Integration Details", True)],
        [cell_p("Database"), cell_p("MongoDB, Mongoose"), cell_p("Storing listing parameters, booking dates, user profiles, and indexing schemas for listings search.")],
        [cell_p("Backend Server"), cell_p("Node.js, Express.js"), cell_p("Configuring RESTful controllers, routing, handling CORS, and implementing session authentication.")],
        [cell_p("Frontend View"), cell_p("React, JavaScript"), cell_p("Creating dynamic state-driven layouts, custom hooks for fetching data, and responsive client pages.")],
        [cell_p("Styling"), cell_p("Vanilla CSS"), cell_p("Writing clean, custom stylesheets without relying on external UI libraries to master CSS Grid, Flexbox, and responsive design.")],
    ]
    story.append(make_tech_table(tech_data))
    story.append(Spacer(1, 10))

    story.append(PageBreak())
    
    # --- PAGE 3: CAPABILITIES & OUTCOMES ---
    story.append(Paragraph("4. Key Implementation Features", h1_style))
    
    story.append(Paragraph("&bull; <b>Property Listings Registry:</b> Database-driven catalogs mapping property names, geographical details, pricing metrics, and host accounts.", bullet_style))
    story.append(Paragraph("&bull; <b>Custom Search & Filters:</b> Query-driven routes retrieving filtered listings based on user search parameters.", bullet_style))
    story.append(Paragraph("&bull; <b>Secure Session Authentication:</b> Protected route middlewares and secure password hashing ensuring safe login and booking validation.", bullet_style))
    story.append(Paragraph("&bull; <b>Relational Booking Workflows:</b> Booking records linking listing IDs to user IDs with check-in/check-out date conflict validations.", bullet_style))
    story.append(Paragraph("&bull; <b>Responsive Layout:</b> Custom vanilla CSS stylesheets utilizing Flexbox and Media Queries for consistent layouts across mobile, tablet, and desktop viewports.", bullet_style))
    
    story.append(Paragraph("5. Developer Role & Core Contributions", h1_style))
    story.append(Paragraph(
        "As the lead full-stack developer on this project, my work spanned both backend operations and front-end user experience. "
        "I designed the MongoDB schemas using Mongoose to ensure quick queries and data consistency. "
        "I implemented secure authentication, protected Express API endpoints, and built dynamic React views that "
        "interact with the database backend.",
        body_style
    ))
    
    story.append(Paragraph("6. Project Learning Outcomes", h1_style))
    learn_text = (
        "<b>Key Takeaway:</b> Developing this Airbnb Clone provided hands-on experience with asynchronous state "
        "management, API integration, and database relationship mapping in MongoDB. Creating a responsive, premium "
        "UI with vanilla CSS reinforced best practices in responsive design, Flexbox layouts, and browser compatibility."
    )
    story.append(make_callout(learn_text, callout_style))
    
    doc.build(story, canvasmaker=AirbnbCanvas)


if __name__ == "__main__":
    print("Generating Seva Setu Case Study PDF...")
    generate_seva_setu_pdf()
    print("Generating Airbnb Clone Project Report PDF...")
    generate_airbnb_pdf()
    print("Done! Generated 2 PDF files in the workspace.")
