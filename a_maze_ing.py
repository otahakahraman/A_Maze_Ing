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

import argparse
import sys

from config_parser import parse_config
from maze_generator.generator import MazeGenerator
from output_writer import write_maze_to_file
from visualizer import interactive_loop, path_to_coordinates


def generate_maze(config_path: str) -> tuple:
    config = parse_config(config_path)
    maze = MazeGenerator(config.width, config.height, config.seed)
    maze.generator(config.entry[0], config.entry[1], config.perfect)
    maze.control(config.entry, config.exit_coord)
    grid = maze.grid
    path_str = maze.find_short_path(config.entry, config.exit_coord)

    output_filename = "maze.txt"
    write_maze_to_file(
        file_path=output_filename,
        grid=grid,
        entry=config.entry,
        exit_coord=config.exit_coord,
        path=path_str,
    )

    path_coords = path_to_coordinates(config.entry, path_str)
    return config, grid, path_str, path_coords


def main() -> None:
    parser = argparse.ArgumentParser(description="A-Maze-Ing maze generator")
    parser.add_argument("config_path", help="Yapılandırma dosyası yolu")
    parser.add_argument(
        "--no-visualize",
        action="store_true",
        help="Labirenti üretip dosyaya yaz, ama interaktif görselleştirme ekranını açma.",
    )
    args = parser.parse_args()

    try:
        config, grid, path_str, path_coords = generate_maze(args.config_path)
    except Exception as exc:
        print(f"Yapılandırma Hatası: {exc}")
        sys.exit(1)

    print(f"Labirent başarıyla 'maze.txt' dosyasına kaydedildi.")

    if not args.no_visualize:
        interactive_loop(
            grid=grid,
            entry=config.entry,
            exit_coord=config.exit_coord,
            path_coords=path_coords,
        )


if __name__ == "__main__":
    main()