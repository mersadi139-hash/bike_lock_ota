#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ساخت فایل version.txt برای OTA
--------------------------------
این اسکریپت فایل باینری app.bin را می‌گیرد، حجم و CRC32 آن را حساب می‌کند،
و فایل version.txt را دقیقاً با فرمتی که میکروکنترلر انتظار دارد می‌سازد.

طرز استفاده:
    python make_version.py app.bin 2

آرگومان اول: مسیر فایل bin
آرگومان دوم: شماره نسخه (همان عددی که در کد App داخل VERSION گذاشته‌ای + 1)
"""

import sys
import zlib


def main():
    if len(sys.argv) != 3:
        print("Usage: python make_version.py <app.bin> <version_number>")
        sys.exit(1)

    bin_path = sys.argv[1]
    version  = int(sys.argv[2])

    # خواندن کل فایل باینری
    with open(bin_path, "rb") as f:
        data = f.read()

    size = len(data)

    # محاسبه‌ی CRC32 استاندارد (همان الگوریتمی که سخت‌افزار STM32 با تنظیمات
    # Poly + Init=FFFFFFFF + RefIn + RefOut + XorOut=FFFFFFFF بازتولید می‌کند)
    crc = zlib.crc32(data) & 0xFFFFFFFF

    # ساخت محتوای فایل نسخه
    txt = "VER={}\nSIZE={}\nCRC={:08X}\n".format(version, size, crc)

    with open("version.txt", "w", newline="\n") as f:
        f.write(txt)

    # نمایش نتیجه
    print("------------------------------------------")
    print(" File   :", bin_path)
    print(" VER    :", version)
    print(" SIZE   :", size, "bytes")
    print(" CRC32  : {:08X}".format(crc))
    print("------------------------------------------")
    print(" version.txt created:")
    print(txt)


if __name__ == "__main__":
    main()
