import math
import struct
import zlib

def make_png(width, height, path):
    # Create raw RGBA bitmap of Cupertino Sonoma/Sequoia dark gradient
    raw = bytearray()
    for y in range(height):
        raw.append(0) # filter type none
        t_y = y / height
        base_r = int(12 + 18 * t_y)
        base_g = int(22 + 45 * t_y)
        base_b = int(48 + 85 * t_y)
        for x in range(width):
            t_x = x / width
            # Cupertino subtle abstract wave/glow
            dx = (x - width * 0.5) / (width * 0.5)
            dy = (y - height * 0.5) / (height * 0.5)
            glow = max(0.0, 1.0 - math.sqrt(dx * dx * 0.6 + dy * dy * 1.2))
            wave = 0.5 + 0.5 * math.sin(t_x * 4.0 + t_y * 2.0)
            
            r = min(255, int(base_r + 25 * glow + 10 * wave))
            g = min(255, int(base_g + 55 * glow + 20 * wave))
            b = min(255, int(base_b + 95 * glow + 40 * wave))
            raw.extend((r, g, b, 255))
            
    # Encode PNG chunks
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)

    header = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
    compressed = zlib.compress(bytes(raw), 9)
    idat = chunk(b'IDAT', compressed)
    iend = chunk(b'IEND', b'')

    with open(path, 'wb') as f:
        f.write(header + ihdr + idat + iend)
    print(f"Generated valid PNG: {path} ({len(header+ihdr+idat+iend)} bytes)")

if __name__ == '__main__':
    make_png(1920, 1080, 'pkgs/enerco-branding/enerco-mac.png')

