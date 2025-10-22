async function downloadPDF(filename, textElementId) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    const text = document.getElementById(textElementId).innerText;

    const pageHeight = doc.internal.pageSize.height;
    const lines = doc.splitTextToSize(text, 180);

    let y = 20;
    doc.setFontSize(12);
    doc.text(`Transcripción: ${filename}`, 10, 10);

    for (let i = 0; i < lines.length; i++) {
        if (y > pageHeight - 10) {
            doc.addPage();
            y = 20;
        }
        doc.text(lines[i], 10, y);
        y += 7;
    }

    doc.save(filename.replace(/\.[^/.]+$/, "") + ".pdf");
}