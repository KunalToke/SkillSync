from flask import Blueprint, render_template, request, send_file
import io
from docx import Document
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

resume_bp = Blueprint('resume', __name__)

@resume_bp.route('/resume', methods=['GET', 'POST'])
def resume():
    if request.method == 'POST':
        resume_data = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "skills": request.form.get("skills"),
            "education": request.form.get("education"),
            "experience": request.form.get("experience"),
            "projects": request.form.get("projects"),
            "template": request.form.get("template")
        }

        if "export_pdf" in request.form:
            return export_pdf(resume_data)
        elif "export_docx" in request.form:
            return export_docx(resume_data)

        return render_template("resume.html", resume=resume_data)

    return render_template("resume.html", resume=None)


def export_docx(data):
    doc = Document()
    doc.add_heading(data["name"], 0)
    doc.add_paragraph(f"Email: {data['email']} | Phone: {data['phone']}")
    doc.add_heading("Skills", level=1)
    doc.add_paragraph(data["skills"])
    doc.add_heading("Education", level=1)
    doc.add_paragraph(data["education"])
    doc.add_heading("Experience", level=1)
    doc.add_paragraph(data["experience"])
    doc.add_heading("Projects", level=1)
    doc.add_paragraph(data["projects"])

    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return send_file(file_stream, as_attachment=True, download_name="resume.docx")


def export_pdf(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"<b>{data['name']}</b>", styles["Title"]))
    story.append(Paragraph(f"Email: {data['email']} | Phone: {data['phone']}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Skills</b>", styles["Heading2"]))
    story.append(Paragraph(data["skills"], styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Education</b>", styles["Heading2"]))
    story.append(Paragraph(data["education"], styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Experience</b>", styles["Heading2"]))
    story.append(Paragraph(data["experience"], styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Projects</b>", styles["Heading2"]))
    story.append(Paragraph(data["projects"], styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="resume.pdf", mimetype="application/pdf")
