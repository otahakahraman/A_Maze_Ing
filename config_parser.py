""" okuma . parsing ve validating konfigüre """
from dataclasses import dataclass #datacalsses den dataclass ı çeker
from typing import Tuple # pythonın tip belirleme kütüphanesinden tuple ı çeker
# tuple birden fazla veriyi bir arada tutan ve içeriği sonradan değiştirilmeyen veri türü


class ConfigError(Exception):
    pass

@dataclass #Python'daki @dataclass dekoratörü, veri depolamak amacıyla oluşturulan sınıfların (class) yazımını basitleştirmek ve hızlandırmak için kullanılır. Python 3.7 ile gelen bu özellik, sınıflar için arka planda otomatik olarak __init__(), __repr__() ve __eq__() gibi özel (dunder) metotları tanımlar.
class MazeConfig:
    width: int
    height: int
    entry: Tuple[int,int]#başlangıç noktasını tutar iki tam sayı ve değiştirilemez
    exit: Tuple[int,int]# çıkıs noktası
    out_put file: str # labirentin yazılacağı dosyanın adını metin olarak saklar
    perfect: bool #harita tipini belirler true haritada hiçbir alternatif yol ada veya döngü kestirme olmaz başlangıçtan çıkısa tek bir yol saptığın diğer yol mutlaka çıkmaz
    #false varsayılan mod birbirine bağlanan birden fazla halka var çıkmaz sokak yok canavardan kaçan kişi köşeye sıkışmaz dolanıp çıkar

