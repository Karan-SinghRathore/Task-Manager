"""
Generates assets/icon.ico from assets/icon.svg at multiple resolutions.

Uses Qt's own SVG renderer (QtSvg, already part of the PySide6 dependency)
to rasterize each size, then Pillow assembles the multi-resolution .ico.
No native Cairo/GTK libraries required.

Requires: pip install PySide6 pillow
Run manually whenever icon.svg changes:
    python scripts/generate_icon.py
"""
import sys
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVG_PATH = ROOT / "assets" / "icon.svg"
ICO_PATH = ROOT / "assets" / "icon.ico"

SIZES = [16, 32, 48, 64, 128, 256]


def render_svg_to_pil(svg_path: Path, size: int):
    from PySide6.QtCore import QByteArray, Qt
    from PySide6.QtGui import QImage, QPainter
    from PySide6.QtSvg import QSvgRenderer
    from PIL import Image

    renderer = QSvgRenderer(str(svg_path))
    if not renderer.isValid():
        raise RuntimeError(f"Invalid SVG file: {svg_path}")

    image = QImage(size, size, QImage.Format_ARGB32)
    image.fill(Qt.transparent)

    painter = QPainter(image)
    renderer.render(painter)
    painter.end()

    buffer = QByteArray()
    from PySide6.QtCore import QBuffer

    qbuffer = QBuffer(buffer)
    qbuffer.open(QBuffer.WriteOnly)
    image.save(qbuffer, "PNG")
    qbuffer.close()

    return Image.open(BytesIO(bytes(buffer.data()))).convert("RGBA")


def main():
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError:
        print("Missing dependency. Install with: pip install PySide6 pillow")
        sys.exit(1)

    if not SVG_PATH.exists():
        print(f"SVG source not found: {SVG_PATH}")
        sys.exit(1)

    # QSvgRenderer/QImage need a QGuiApplication instance to be alive.
    app = QApplication.instance() or QApplication(sys.argv)

    png_frames = [render_svg_to_pil(SVG_PATH, size) for size in SIZES]

    largest = png_frames[-1]
    largest.save(
        ICO_PATH,
        format="ICO",
        sizes=[(s, s) for s in SIZES],
        append_images=png_frames[:-1],
    )
    print(f"Wrote {ICO_PATH} with sizes {SIZES}")


if __name__ == "__main__":
    main()
