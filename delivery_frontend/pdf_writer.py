"""from fpdf import FPDF
#from backend import get_open_tasks, parse_tasks


def report_open_tasks():
    """
    #takes data from SQL db and transforms to PDF on some conditions
    """
    data = get_open_tasks()
    pdf = FPDF(format="A4")
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Open Tasks by Request Date", ln=1, align="C")
    holder = 0
    for num, obj in enumerate(data):
        pdf.set_font("Arial", size=14)
        pdf.cell(0, 10, txt="Docket# "+str(obj[0])+" Customer: "+obj[1] +
                 " Request date : "+obj[2], ln=1, align="L")
        pdf.set_font("Arial", size=9)
        for line, entry in enumerate(parse_tasks(obj[3])):
            if entry is None:
                continue
            try:
                # print(entry)
                pdf.cell(0, 10, txt="       Task: " +
                         entry[0]+" Due Date:   "+entry[2], ln=1, align="L")
            except:
                pass
            holder += 1
    pdf.output("Reports/sample_report.pdf")


if __name__ == "__main__":
    report_open_tasks()
"""