import PyPDF2
import os

def merge_pdfs_in_folder(folder_path, output_filename):
    pdf_merger = PyPDF2.PdfMerger()

    # Get all PDF files in the specified folder
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

    for pdf in pdf_files:
        with open(os.path.join(folder_path, pdf), 'rb') as pdf_file:
            pdf_merger.append(pdf_file)

    with open(output_filename, 'wb') as output_file:
        pdf_merger.write(os.path.join(output_filename))

# Example usage
folder_path = r'L:\Huanchen\Thyrovoice\Py_VRP\group_by_sur_type\group_by_all\Total\Album'
# load all pdf files in the directory
output_file = 'L:\Huanchen\Thyrovoice\Py_VRP\group_by_sur_type\Total_group_by_all_ALL.pdf'
merge_pdfs_in_folder(folder_path, output_file)