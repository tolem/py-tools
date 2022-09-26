import PYPDF2
import sys

inputs = sys.argv[1:]

def pdf_combiner(pdfs):
  merger= PYPDF2.PdfFileMerger()
  for pdf in pdfs:
    merger.append(pdf)
   merger.write('I.20.jpeg')
  return True

pdf_combiner(inputs)
  
