@app.route("/render")
def render():
    try:
        url  = request.args.get("url")
        page = request.args.get("page", type=int, default=1) - 1
        if not url or page < 0:
            return abort(400, "params: url & page (>=1) required")

        print(f"Fetching PDF from: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # will throw for 4xx or 5xx errors

        pdf_bytes = response.content
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        if page >= doc.page_count:
            return abort(400, f"PDF has only {doc.page_count} pages")

        pix = doc.load_page(page).get_pixmap(dpi=300)
        buf = io.BytesIO(pix.tobytes("png")); buf.seek(0)
        return send_file(buf, mimetype="image/png")

    except Exception as e:
        print("ERROR:", str(e))
        return abort(500, f"Internal server error: {str(e)}")
