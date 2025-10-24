# Implementación mínima de imghdr para compatibilidad con Python 3.13
def what(file, h=None):
    header = h or (open(file,'rb').read(32) if isinstance(file, str) else None)
    if not header:
        return None
    if header[:3] == b'\xff\xd8\xff': return 'jpeg'
    if header.startswith(b'\x89PNG\r\n\x1a\n'): return 'png'
    if header.startswith(b'GIF87a') or header.startswith(b'GIF89a'): return 'gif'
    if header.startswith(b'BM'): return 'bmp'
    if header[:4] == b'RIFF' and header[8:12] == b'WEBP': return 'webp'
    return None
