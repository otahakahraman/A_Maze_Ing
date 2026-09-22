"""
config_parser.py: Dosyadan ayarları okuyup doğruluyor.

generator.py: Labirenti ve çözüm yolunu üretiyor.

output_writer.py: Labirent matrisini hex formatında maze.txt içine yazıyor.

visualizer.py: Ekrana renkli labirent basıp tuşları (s, c, q) dinliyor.

a_maze_ing.py Ne Yapacak?
Terminalden verilen config dosyasını alacak (örneğin: python3 a_maze_ing.py config.txt).

Parametre verilmemişse veya dosya bulunamazsa temiz bir hata basıp çıkacak.

Labirenti ürettirip önce dosyaya yazacak, ardından ekranda canlı görselleştiriciyi başlatacak.
"""

"""A-Maze-Ing oluşturucu ve görselleştirici için ana giriş noktası."""

import sys #argümanlarını sys.ergv okumakv ve hatalı durumlarda programı sonlandırmak için sys.exit için standart python kütüphanesini içe aktarır
from config_parser import parse_config #farklı dosyalardaki kodları çağrıyorum
from maze_generator.generator import  MazeGenerator
from output_writer import write_maze_to_file
from visualizer import interactive_loop, path_to_coordinates

def main() -> None:
    if len(sys.argv) < 2: # terminalden girilen komutu liste olarak tutar (len(...))
        print("Hata: Lütfen bir yapılandırma dosyası belirtin.")
        print("Kullanım: python3 a_maze_ing.py <config_dosyasi>")
        sys.exit(1)

    config_path = sys.argv[1] #belirtilen yapılandırma dosyasını yolunu değişkene kaydeder

# 2. Config dosyasını oku ve doğrula
    try:
        config = parse_config(config_path)
    except Exception as e:
        print(f"Yapılandırma Hatası: {e}")
        sys.exit(1) # hatalı bir çıkış olduğunu belirtir 0 doğru olandır 1 genel hata 2 argüman 3 girdi yapılandırma hatası

# 3. Labirenti ve çözüm yolunu üret
    maze = MazeGenerator(config.width, config.height, config.seed)
    maze.generator(config.entry[0], config.entry[1], config.perfect)
    grid = maze.grid
    path_str = maze.find_short_path(config.entry, config.exit_coord)
    
    # 4. Labirenti ve çözümü dosyaya yaz (Subject gereksinimi: maze.txt)
    output_filename = "maze.txt"
    write_maze_to_file(
        file_path=output_filename,
        grid=grid,
        entry=config.entry,
        exit_coord=config.exit_coord,
        path=path_str
    )
    print(f"Labirent başarıyla '{output_filename}' dosyasına kaydedildi.")

    # 5. Çözüm yolunu (x, y) koordinat kümesine çevir
    path_coords = path_to_coordinates(config.entry, path_str)

    # 6. Terminalde interaktif görselleştirmeyi başlat
    interactive_loop(
        grid=grid,
        entry=config.entry,
        exit_coord=config.exit_coord,
        path_coords=path_coords,
    )


if __name__ == "__main__":
    main()