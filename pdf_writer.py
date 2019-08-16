from PyPDF4 import PdfFileWriter

#http://www.blog.pythonlibrary.org/2018/06/05/creating-pdfs-with-pyfpdf-and-python/






def report_open_tasks():
    """
    takes data from SQL db and transforms to PDF
    """
    #pdf = open(r"report.pdf","wb")
    writer = PdfFileWriter("reort.pdf")
    for i in range(100):
        writer.write("This is the simple report done by program")


if __name__=="__main__":
    report_open_tasks()