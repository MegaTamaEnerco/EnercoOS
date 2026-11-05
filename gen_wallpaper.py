import math
import struct
import zlib

def make_tahoe_wallpaper(width=1920, height=1080, path='pkgs/enerco-branding/enerco-mac.png'):
    print(f"Generating macOS Tahoe wallpaper ({width}x{height})...")
    raw = bytearray()
    
    inv_w = 1.0 / width
    inv_h = 1.0 / height
    
    for y in range(height):
        raw.append(0) # PNG filter type: None
        ny = y * inv_h # 0.0 at top, 1.0 at bottom
        
        # Base deep midnight background gradient
        bg_r = 7.0 + 12.0 * ny
        bg_g = 10.0 + 16.0 * ny
        bg_b = 20.0 + 38.0 * ny
        
        for x in range(width):
            nx = x * inv_w # 0.0 at left, 1.0 at right
            
            # Central ambient radiant glow (macOS Tahoe ambient light)
            dx = (nx - 0.5) * 1.6
            dy = (ny - 0.55) * 1.8
            dist2 = dx * dx + dy * dy
            ambient = max(0.0, 1.0 - math.sqrt(dist2))
            ambient_glow = ambient * ambient * (3.0 - 2.0 * ambient) # smoothstep
            
            # Wave Ribbon 1: Primary Tahoe Azure & Cobalt Wave
            w1_y = 0.58 + 0.16 * math.sin(nx * 3.8 - 0.6) + 0.08 * math.cos(nx * 7.2)
            d1 = abs(ny - w1_y)
            r1 = math.exp(-d1 * 14.0) # Sharp luminous core
            r1_halo = math.exp(-d1 * 4.5) * 0.5 # Soft atmospheric glow
            
            # Wave Ribbon 2: Secondary Cyan & Turquoise Glass Ribbon
            w2_y = 0.66 + 0.14 * math.sin(nx * 4.4 + 1.2) - 0.06 * math.cos(nx * 8.6 + 0.4)
            d2 = abs(ny - w2_y)
            r2 = math.exp(-d2 * 18.0)
            r2_halo = math.exp(-d2 * 5.0) * 0.4
            
            # Wave Ribbon 3: Violet / Magenta Aurora Glow
            w3_y = 0.48 + 0.12 * math.cos(nx * 3.2 + 0.8) + 0.07 * math.sin(nx * 6.0)
            d3 = abs(ny - w3_y)
            r3 = math.exp(-d3 * 16.0)
            r3_halo = math.exp(-d3 * 4.0) * 0.35
            
            # Blend channels with physical tone mapping
            r = bg_r + ambient_glow * 18.0 + (r3 * 140.0 + r3_halo * 65.0) + (r1 * 25.0 + r1_halo * 15.0) + (r2 * 10.0)
            g = bg_g + ambient_glow * 32.0 + (r1 * 95.0 + r1_halo * 45.0) + (r2 * 165.0 + r2_halo * 75.0) + (r3 * 20.0)
            b = bg_b + ambient_glow * 80.0 + (r1 * 210.0 + r1_halo * 105.0) + (r2 * 230.0 + r2_halo * 110.0) + (r3 * 180.0 + r3_halo * 85.0)
            
            # Vignette around perimeter for cinematic focus
            vignette = 1.0 - 0.28 * (dx * dx * 0.4 + dy * dy * 0.6)
            r *= vignette
            g *= vignette
            b *= vignette
            
            # Clamp to 0..255
            ir = min(255, max(0, int(r)))
            ig = min(255, max(0, int(g)))
            ib = min(255, max(0, int(b)))
            
            raw.extend((ir, ig, ib, 255))
            
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)

    header = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
    compressed = zlib.compress(bytes(raw), 9)
    idat = chunk(b'IDAT', compressed)
    iend = chunk(b'IEND', b'')

    with open(path, 'wb') as f:
        f.write(header + ihdr + idat + iend)
    print(f"Generated macOS Tahoe wallpaper: {path} ({len(header+ihdr+idat+iend)} bytes)")

if __name__ == '__main__':
    make_tahoe_wallpaper(1920, 1080, 'pkgs/enerco-branding/enerco-mac.png')
