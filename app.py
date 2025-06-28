import io, os, requests, fitz  # PyMuPDF is imported as fitz
from flask import Flask, request, send_file, abort

app = Flask(__name__)

@app.route("/ping")
def ping():
    print("✅ /ping was hit")
    return "pong"

@app.route("/render")
def render():
    print("📥 Request received for /render")  # <== this is the key debug line

    try:
        url  = request.args.get("url")
        page = request.args.get("page", type=int, default=1) - 1
        if not url or page < 0:
            return abort(400, "params: url & page (>=1) required")

        print(f"Fetching PDF from: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # throw for 4xx or 5xx errors

        pdf_bytes = response.content
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        print(f"✅ PDF opened, pages: {doc.page_count}")
        if page >= doc.page_count:
            return abort(400, f"PDF has only {doc.page_count} pages")

        pix = doc.load_page(page).get_pixmap(dpi=300)
        print(f"✅ Pixmap created, size: {pix.width}x{pix.height}, bytes: {len(pix.samples)}")
        buf = io.BytesIO(pix.tobytes("png"))
        buf.seek(0)
        return send_file(buf, mimetype="image/png")

    except Exception as e:
        import traceback
        print("ERROR:", str(e))
        traceback.print_exc()
        return abort(500, f"Internal server error: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)), debug=False)
