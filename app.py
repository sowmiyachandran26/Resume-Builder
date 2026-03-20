from flask import Flask, render_template, request, make_response
import pdfkit

app = Flask(__name__)

# CHANGE THIS PATH if wkhtmltopdf is installed elsewhere
config = pdfkit.configuration(
    wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
)

PDF_OPTIONS = {
    'page-size': 'A4',
    'margin-top': '0mm',
    'margin-right': '0mm',
    'margin-bottom': '0mm',
    'margin-left': '0mm',
    'encoding': 'UTF-8',
    'enable-local-file-access': None
}

def get_template(template_id):
    templates = {
        "1": "template1.html",
        "2": "template2.html",
        "3": "template3.html",
        "4": "template4.html",
        "5": "template5.html",
    }
    return templates.get(template_id, "template1.html")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('resume_form.html')

@app.route('/resume', methods=['POST'])
def resume():
    data = request.form
    template = get_template(data.get('template', '1'))
    return render_template(template, data=data)

@app.route('/download', methods=['POST'])
def download():
    data = request.form
    template = get_template(data.get('template', '1'))
    rendered = render_template(template, data=data)
    pdf = pdfkit.from_string(rendered, False, configuration=config, options=PDF_OPTIONS)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=resume.pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True)
