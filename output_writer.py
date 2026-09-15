from typing import List, Tuple #list ve tuple tip etiketidir kod yazarken bir değişkenin veya fonksiyonun hangi türde veri taşıması gerektiğini belirten not
"""
Python kodu çalıştırırken bu etiketleri umursamaz; asıl amaç insana ve kod editörüne rehberlik etmektir.

Etiketsiz: def topla(a, b):

(a ve b sayı mı, yazı mı, liste mi? Belli değil, tahmine dayalıdır.)

Etiketli: def topla(a: int, b: int) -> int:

(Girişler tamsayı (int) olmalı, sonuç da tamsayı (int) dönecektir.)"""

def write_maze_to_file(
        file_path: str,#dosyanın nereye kaydedileceği 
        grid: List[List[int]], #labirentin haritası. Hücrelerin sayı matrisi halidir
        entry:Tuple[int, int],# başlangıç noktasının kordinatı
        exit_coord: Tuple[int, int], # bitiş noktasının kordinatı
        path; str, # başlangıçtan bitişe giden en kısa yolun harf dizisi eesswwn gibi


) -> None:

#bu yukardaki fonksiyonun amacı hafızadaki labirenti kağıda dökmek maze.txt ye dökmek 













"""Output writer module for exporting generated mazes.

This module formats the maze grid into hexadecimal lines and appends
the entry, exit, and shortest path solution according to 42 subject rules.
"""

from typing import List, Tuple


def write_maze_to_file(
    file_path: str,
    grid: List[List[int]],
    entry: Tuple[int, int],
    exit_coord: Tuple[int, int],
    path: str,
) -> None:

with open(file_path, "w",encoding = " utf-8 ") as f: #açılan dosyayı kod içinde temsil eden geçici bir taka addır değişkendir 
#file path dosyanın nerde olduğunu ve adını söyler 
# w yazma modu ve ayrıca yoksa açılmasını varsa içindekileri silip tertemiz baştan da yazan o
# encoding="utf-8" Dosyaya yazılan harflerin hangi evrensel dil/karakter standardıyla kaydedileceğini belirler. Farklı işletim sistemlerinde (Mac, Linux, Windows) Türkçe karakterlerin veya özel sembollerin bozulmadan, garip şekillere (Ã§, Ä±) dönüşmeden düzgün okunmasını sağlar.
#with bloğu iş bittiğinde veya kodun ortasında beklenmedik bir hata çıktığında dosyayı arkada açık unutmadan güvenle kapatan bir mekanizmadır bellek sızıntısını önler

    # 1. Matrisi satır satır dönüp hex karakterlere çeviriyoruz
        for row in grid:
            hex_line = "".join(format(cell, "x") for cell in row)
            f.write(f"{hex_line}\n")

        # 2. Subject gereği araya 1 boş satır bırakıyoruz
        f.write("\n")

        # 3. Giriş, Çıkış ve Çözüm Yolunu yazdırıyoruz
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_coord[0]},{exit_coord[1]}\n")
        f.write(f"{path}\n")