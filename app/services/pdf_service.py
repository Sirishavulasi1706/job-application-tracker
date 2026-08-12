from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate


def create_cover_letter_pdf(cover_letter):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    for line in cover_letter.split("\n"):

        if line.strip():

            story.append(
                Paragraph(line, styles["Normal"])
            )

    doc.build(story)

    buffer.seek(0)

    return buffer