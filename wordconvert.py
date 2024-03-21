#Function to convert the data to a word document
from docx import Document

def to_word(data, filename):
    doc = Document()

    table = doc.add_table(rows=1, cols=len(data.columns))
    for i, column in enumerate(data.columns):
        table.cell(0, i).text = column

    for _, row in data.iterrows():
        row_cells = table.add_row().cells
        for i, value in enumerate(row):
            row_cells[i].text = str(value)

    doc.save(filename)

#Function to convert the result to a word document
def result_word(data,filename):
    doc = Document()

    table = doc.add_table(rows=1, cols=len(data.columns))
    for i, column in enumerate(data.columns):
        table.cell(0, i).text = column

    for _, row in data.iterrows():
        row_cells = table.add_row().cells
        for i, value in enumerate(row):
            row_cells[i].text = str(value)

    doc.save(filename)