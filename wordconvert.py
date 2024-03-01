#Function to get the data in Docx format

from docx import Document
def generate_word_document(data):
    doc = Document()
    table = doc.add_table(rows=1, cols=len(data.columns))
    for i, column in enumerate(data.columns):
        table.cell(0, i).text = column

    for _, row in data.iterrows():
        row_cells = table.add_row().cells
        for i, value in enumerate(row):
            row_cells[i].text = str(value)

    doc.save('output/historical_data.docx')