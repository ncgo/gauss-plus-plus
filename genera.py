from fpdf import FPDF

pdf = FPDF()
# Agregar una pagina al documento
pdf.add_page()

# Fuente y tamaño para el documento
pdf.set_font("Arial", size = 15)

# Creamos una celda
pdf.cell(200, 10, txt = "GeeksforGeeks", ln = 1, align = 'C')

# add another cell
pdf.cell(200, 10, txt = "A Computer Science portal for geeks.", ln = 2, align = 'C')

# save the pdf with name .pdf
pdf.output("GFG.pdf")

