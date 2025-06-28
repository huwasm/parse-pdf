import io, os, requests, fitz                # PyMuPDF is imported as fitz
from flask import Flask, request, send_file, abort

app = Flask(__name__)

@app.route("/render")
def render():
    url  = request.args.get("url")
    page = request.args.get("page", type=int, default=1) - 1   # 0-based
    if not url or page < 0:
        return abort(400, "params: url & page (>=1) required")

    pdf_bytes = requests.get(url, timeout=30).content
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    if page >= doc.page_count:
        return abort(400, f"PDF has only {doc.page_count} pages")

    pix = doc.load_page(page).get_pixmap(dpi=300)
    buf = io.BytesIO(pix.tobytes("png")); buf.seek(0)
    return send_file(buf, mimetype="image/png")

if __name__ == "__main__":                   # local test: python app.py
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
