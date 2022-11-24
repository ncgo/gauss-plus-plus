from fpdf import FPDF

class PDF(FPDF):
    def __init__(self):
        self.headerDatos = ["titulo", "spring", "1"]
        self.titulo = ""
        self.instrucciones = ""
        self.problemasIncluidos = []
        self.footerDatos = ""
        self.state = 0
        self.font_family ='dejavu'
        self.underline =0
        self.font_style = ''

    def header(self):
        # Select Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(50)
        self.cell(30, 10, self.headerDatos[0], 0, 0, 'C', 0)
        self.cell(30, 10, self.headerDatos[1], 0, 0, 'C', 0)
        self.cell(30, 10, self.headerDatos[2], 0, 0, 'C', 0)
        # Line break
        self.ln(20)

def doit(pdf):
    # Agregar una pagina al documento
    pdf.add_page()
    pdf.header()
    # Fuente y tamaño para el documento
    pdf.set_font("Arial", size = 15)
    # Creamos una celda
    pdf.cell(200, 10, txt = "GeeksforGeeks", ln = 1, align = 'C')
    # add another cell
    pdf.cell(200, 10, txt = "A Computer Science portal for geeks.", ln = 2, align = 'C')
    # save the pdf with name .pdf
    pdf.output("GFG.pdf")