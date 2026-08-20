from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

from .models import Certificate


# ============================================================
# CERTIFICATE LIST
# ============================================================

@login_required
def certificate_list(request):
    certificates = (
        Certificate.objects
        .filter(student=request.user)
        .select_related(
            "course",
            "course__instructor"
        )
    )

    return render(
        request,
        "certificates/certificate_list.html",
        {
            "certificates": certificates
        }
    )


# ============================================================
# CERTIFICATE DETAIL
# ============================================================

@login_required
def certificate_detail(request, certificate_id):

    certificate = get_object_or_404(
        Certificate.objects.select_related(
            "course",
            "course__instructor"
        ),
        id=certificate_id
    )

    return render(
        request,
        "certificates/certificate_detail.html",
        {
            "certificate": certificate
        }
    )


# ============================================================
# DOWNLOAD CERTIFICATE PDF
# ============================================================

@login_required
def download_certificate(request, certificate_id):

    certificate = get_object_or_404(
        Certificate.objects.select_related(
            "course",
            "course__instructor"
        ),
        id=certificate_id
    )

    # ==========================================================
    # SECURITY
    # ==========================================================

    if (
        request.user != certificate.student
        and request.user.role not in ["instructor", "admin"]
    ):
        return HttpResponse(
            "You do not have permission to download this certificate.",
            status=403
        )

    # ==========================================================
    # PDF RESPONSE
    # ==========================================================

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="Certificate_{certificate.id}.pdf"'
    )

    # ==========================================================
    # PAGE SETUP
    # ==========================================================

    page_width, page_height = landscape(A4)

    pdf = canvas.Canvas(
        response,
        pagesize=landscape(A4)
    )

    center_x = page_width / 2

    # ==========================================================
    # COLORS
    # ==========================================================

    primary = colors.HexColor("#4F46E5")
    dark = colors.HexColor("#111827")
    gray = colors.HexColor("#6B7280")
    light_gray = colors.HexColor("#9CA3AF")
    border_light = colors.HexColor("#C7D2FE")
    background = colors.white

    # ==========================================================
    # BACKGROUND
    # ==========================================================

    pdf.setFillColor(background)

    pdf.rect(
        0,
        0,
        page_width,
        page_height,
        fill=1,
        stroke=0
    )

    # ==========================================================
    # OUTER BORDER
    # ==========================================================

    pdf.setStrokeColor(primary)
    pdf.setLineWidth(5)

    pdf.roundRect(
        25,
        25,
        page_width - 50,
        page_height - 50,
        15,
        fill=0,
        stroke=1
    )

    # ==========================================================
    # INNER BORDER
    # ==========================================================

    pdf.setStrokeColor(border_light)
    pdf.setLineWidth(2)

    pdf.roundRect(
        42,
        42,
        page_width - 84,
        page_height - 84,
        10,
        fill=0,
        stroke=1
    )

    # ==========================================================
    # DECORATIVE CORNERS
    # ==========================================================

    corner_color = colors.HexColor("#F59E0B")

    pdf.setStrokeColor(corner_color)
    pdf.setLineWidth(4)

    corner_size = 45

    # Top-left
    pdf.line(
        55,
        page_height - 55,
        55 + corner_size,
        page_height - 55
    )

    pdf.line(
        55,
        page_height - 55,
        55,
        page_height - 55 - corner_size
    )

    # Top-right
    pdf.line(
        page_width - 55,
        page_height - 55,
        page_width - 55 - corner_size,
        page_height - 55
    )

    pdf.line(
        page_width - 55,
        page_height - 55,
        page_width - 55,
        page_height - 55 - corner_size
    )

    # Bottom-left
    pdf.line(
        55,
        55,
        55 + corner_size,
        55
    )

    pdf.line(
        55,
        55,
        55,
        55 + corner_size
    )

    # Bottom-right
    pdf.line(
        page_width - 55,
        55,
        page_width - 55 - corner_size,
        55
    )

    pdf.line(
        page_width - 55,
        55,
        page_width - 55,
        55 + corner_size
    )

    # ==========================================================
    # HEADER - COURSIFY LOGO
    # ==========================================================

    # Circle logo

    pdf.setFillColor(primary)

    pdf.circle(
        85,
        page_height - 65,
        30,
        fill=1,
        stroke=0
    )

    # C inside logo

    pdf.setFillColor(colors.white)

    pdf.setFont(
        "Helvetica-Bold",
        24
    )

    pdf.drawCentredString(
        85,
        page_height - 73,
        "C"
    )

    # Coursify text

    pdf.setFillColor(dark)

    pdf.setFont(
        "Helvetica-Bold",
        22
    )

    pdf.drawString(
        125,
        page_height - 73,
        "Coursify"
    )

    # Certificate label

    pdf.setFillColor(primary)

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawRightString(
        page_width - 75,
        page_height - 70,
        "CERTIFICATE"
    )

    # ==========================================================
    # MAIN TITLE
    # ==========================================================

    pdf.setFillColor(primary)

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawCentredString(
        center_x,
        page_height - 125,
        "CERTIFICATE OF COMPLETION"
    )

    # Certificate heading

    pdf.setFillColor(dark)

    pdf.setFont(
        "Helvetica-Bold",
        36
    )

    pdf.drawCentredString(
        center_x,
        page_height - 170,
        "Certificate"
    )

    # ==========================================================
    # DIVIDER
    # ==========================================================

    divider_y = page_height - 195

    pdf.setStrokeColor(border_light)
    pdf.setLineWidth(1)

    pdf.line(
        center_x - 210,
        divider_y,
        center_x - 25,
        divider_y
    )

    pdf.line(
        center_x + 25,
        divider_y,
        center_x + 210,
        divider_y
    )

    pdf.setFillColor(primary)

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawCentredString(
        center_x,
        divider_y - 5,
        "◆"
    )

    # ==========================================================
    # PRESENTED TO
    # ==========================================================

    pdf.setFillColor(gray)

    pdf.setFont(
        "Helvetica",
        13
    )

    pdf.drawCentredString(
        center_x,
        page_height - 235,
        "This certificate is proudly presented to"
    )

    # ==========================================================
    # STUDENT NAME
    # ==========================================================

    student_name = certificate.student.username

    pdf.setFillColor(dark)

    pdf.setFont(
        "Helvetica-Bold",
        27
    )

    pdf.drawCentredString(
        center_x,
        page_height - 275,
        student_name
    )

    # Student underline

    pdf.setStrokeColor(primary)
    pdf.setLineWidth(2)

    pdf.line(
        center_x - 120,
        page_height - 287,
        center_x + 120,
        page_height - 287
    )

    # ==========================================================
    # COMPLETION TEXT
    # ==========================================================

    pdf.setFillColor(gray)

    pdf.setFont(
        "Helvetica",
        13
    )

    pdf.drawCentredString(
        center_x,
        page_height - 315,
        "for successfully completing the course"
    )

    # ==========================================================
    # COURSE NAME
    # ==========================================================

    course_name = certificate.course.title

    pdf.setFillColor(primary)

    pdf.setFont(
        "Helvetica-Bold",
        21
    )

    pdf.drawCentredString(
        center_x,
        page_height - 350,
        course_name
    )

    # ==========================================================
    # DESCRIPTION
    # ==========================================================

    pdf.setFillColor(gray)

    pdf.setFont(
        "Helvetica",
        10.5
    )

    description_line_1 = (
        "Demonstrating dedication, commitment and successful"
    )

    description_line_2 = (
        "completion of the required learning activities."
    )

    pdf.drawCentredString(
        center_x,
        page_height - 375,
        description_line_1
    )

    pdf.drawCentredString(
        center_x,
        page_height - 392,
        description_line_2
    )

    # ==========================================================
    # CERTIFICATE ID
    # ==========================================================

    # IMPORTANT:
    # We generate the same ID shown on the website.

    certificate_number = (
        f"CFS-{certificate.id:05d}"
    )

    pdf.setFillColor(gray)

    pdf.setFont(
        "Helvetica-Bold",
        9
    )

    pdf.drawString(
        75,
        105,
        "CERTIFICATE ID"
    )

    pdf.setFillColor(dark)

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawString(
        75,
        88,
        certificate_number
    )

    # ==========================================================
    # ISSUED ON
    # ==========================================================

    pdf.setFillColor(gray)

    pdf.setFont(
        "Helvetica-Bold",
        9
    )

    pdf.drawRightString(
        page_width - 75,
        105,
        "ISSUED ON"
    )

    issued_date = certificate.issued_at.strftime(
        "%d %b %Y"
    )

    pdf.setFillColor(dark)

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawRightString(
        page_width - 75,
        88,
        issued_date
    )

    # ==========================================================
    # VERIFIED SEAL
    # ==========================================================

    seal_x = center_x
    seal_y = 95

    # Outer circle

    pdf.setStrokeColor(primary)
    pdf.setLineWidth(3)

    pdf.circle(
        seal_x,
        seal_y,
        31,
        fill=0,
        stroke=1
    )

    # Inner circle

    pdf.setFillColor(primary)

    pdf.circle(
        seal_x,
        seal_y,
        23,
        fill=1,
        stroke=0
    )

    # Check mark

    pdf.setFillColor(colors.white)

    pdf.setFont(
        "Helvetica-Bold",
        22
    )

    pdf.drawCentredString(
        seal_x,
        seal_y - 7,
        "✓"
    )

    # Verified text

    pdf.setFillColor(primary)

    pdf.setFont(
        "Helvetica-Bold",
        7
    )

    pdf.drawCentredString(
        seal_x,
        seal_y - 47,
        "VERIFIED"
    )

    # ==========================================================
    # INSTRUCTOR SIGNATURE
    # ==========================================================

    instructor_name = (
        certificate.course.instructor.username
    )

    instructor_x = page_width - 170

    pdf.setStrokeColor(light_gray)

    pdf.setLineWidth(1)

    pdf.line(
        instructor_x - 80,
        65,
        instructor_x + 80,
        65
    )

    pdf.setFillColor(dark)

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawCentredString(
        instructor_x,
        47,
        instructor_name
    )

    pdf.setFillColor(gray)

    pdf.setFont(
        "Helvetica",
        8
    )

    pdf.drawCentredString(
        instructor_x,
        34,
        "Course Instructor"
    )

    # ==========================================================
    # FOOTER LINE
    # ==========================================================

    pdf.setStrokeColor(
        colors.HexColor("#E5E7EB")
    )

    pdf.setLineWidth(1)

    pdf.line(
        70,
        25,
        page_width - 70,
        25
    )

    # ==========================================================
    # FOOTER TEXT
    # ==========================================================

    pdf.setFillColor(gray)

    pdf.setFont(
        "Helvetica",
        8
    )

    pdf.drawString(
        70,
        12,
        "Coursify Learning Platform"
    )

    pdf.drawRightString(
        page_width - 70,
        12,
        "Excellence • Learning • Growth"
    )

    # ==========================================================
    # FINISH PDF
    # ==========================================================

    pdf.showPage()

    pdf.save()

    return response