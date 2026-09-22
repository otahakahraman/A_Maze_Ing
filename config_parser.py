""" okuma . parsing ve validating konfigüre """
import ast
from dataclasses import dataclass #datacalsses den dataclass ı çeker
from typing import Tuple # pythonın tip belirleme kütüphanesinden tuple ı çeker
# tuple birden fazla veriyi bir arada tutan ve içeriği sonradan değiştirilmeyen veri türü


class ConfigError(Exception):
    pass

@dataclass #Python'daki @dataclass dekoratörü, veri depolamak amacıyla oluşturulan sınıfların (class) yazımını basitleştirmek ve hızlandırmak için kullanılır. Python 3.7 ile gelen bu özellik, sınıflar için arka planda otomatik olarak __init__(), __repr__() ve __eq__() gibi özel (dunder) metotları tanımlar.
class MazeConfig:
    width: int
    height: int
    seed: int
    entry: Tuple[int,int]#başlangıç noktasını tutar iki tam sayı ve değiştirilemez
    exit_coord: Tuple[int,int]# çıkıs noktası
    output_file: str # labirentin yazılacağı dosyanın adını metin olarak saklar
    perfect: bool #harita tipini belirler true haritada hiçbir alternatif yol ada veya döngü kestirme olmaz başlangıçtan çıkısa tek bir yol saptığın diğer yol mutlaka çıkmaz
    #false varsayılan mod birbirine bağlanan birden fazla halka var çıkmaz sokak yok canavardan kaçan kişi köşeye sıkışmaz dolanıp çıkar

"""buranın altında yazan şeyi chatgbt yazdı. sen orayı nasıl olduğunu öğren. gerekirse tekrar yaz"""

def parse_config(file_path: str) -> MazeConfig:
    values: dict[str, str] = {}

    try:
        with open(file_path, encoding="utf-8") as config_file:
            for line_number, line in enumerate(config_file, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ConfigError(f"{line_number}. satırda '=' eksik")
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip()
    except OSError as error:
        raise ConfigError(f"Yapılandırma dosyası okunamadı: {error}") from error

    required = {"WIDTH", "HEIGHT", "SEED", "ENTRY", "EXIT_COORD", "OUTPUT_FILE", "PERFECT"}
    missing = required - values.keys()
    if missing:
        raise ConfigError(f"Eksik ayarlar: {', '.join(sorted(missing))}")

    try:
        width = int(values["WIDTH"])
        height = int(values["HEIGHT"])
        seed = int(values["SEED"])
        entry = _parse_coordinate(values["ENTRY"])
        exit_coord = _parse_coordinate(values["EXIT_COORD"])
        perfect = _parse_bool(values["PERFECT"])
    except ValueError as error:
        raise ConfigError(f"Geçersiz ayar değeri: {error}") from error

    if width <= 0 or height <= 0:
        raise ConfigError("WIDTH ve HEIGHT sıfırdan büyük olmalı")
    if not _inside_grid(entry, width, height):
        raise ConfigError("ENTRY grid sınırları dışında")
    if not _inside_grid(exit_coord, width, height):
        raise ConfigError("EXIT_COORD grid sınırları dışında")
    if entry == exit_coord:
        raise ConfigError("ENTRY ve EXIT_COORD aynı olamaz")
    if not values["OUTPUT_FILE"]:
        raise ConfigError("OUTPUT_FILE boş olamaz")

    return MazeConfig(
        width=width,
        height=height,
        seed=seed,
        entry=entry,
        exit_coord=exit_coord,
        output_file=values["OUTPUT_FILE"],
        perfect=perfect,
    )


def _parse_coordinate(value: str) -> Tuple[int, int]:
    parsed = ast.literal_eval(value if value.startswith("(") else f"({value})")
    if not isinstance(parsed, tuple) or len(parsed) != 2:
        raise ValueError("koordinat iki elemanlı olmalı")
    if not all(isinstance(item, int) for item in parsed):
        raise ValueError("koordinat değerleri tam sayı olmalı")
    return parsed


def _parse_bool(value: str) -> bool:
    normalized = value.lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise ValueError("PERFECT TRUE veya FALSE olmalı")


def _inside_grid(coordinate: Tuple[int, int], width: int, height: int) -> bool:
    x, y = coordinate
    return 0 <= x < width and 0 <= y < height

