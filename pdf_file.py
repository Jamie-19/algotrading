from fpdf import FPDF

def df_to_pdf(data, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    
    # Convert the index to a column
    data_reset = data.reset_index()

    # Add column headers
    for column in data_reset.columns:
        pdf.cell(40, 10, str(column), 1, 0, 'C')
    pdf.ln()

    # Add data rows
    for row in data_reset.itertuples(index=False):
        for cell in row:
            pdf.cell(40, 10, str(cell), 1, 0, 'C')
        pdf.ln()

    pdf.output(filename)
