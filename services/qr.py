import qrcode
from io import BytesIO

def generar_qr(id_equipo, url_base):

    url = f"{url_base}/?id={id_equipo}"

    qr = qrcode.make(url)

    buf = BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)

    return buf