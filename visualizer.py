#görselleştirici

"""Terminal visualizer for maze rendering and interactive display.

This module converts a bitmask maze matrix into an ASCII terminal representation
with ANSI colors, path toggling, and interactive controls.

Labirent çizimi ve etkileşimli görüntüleme için terminal görselleştiricisi.

Bu modül, bit maskesi tabanlı bir labirent matrisini;
 ANSI renkleri, yol açma/kapama özelliği ve etkileşimli kontroller 
 içeren bir ASCII terminal gösterimine dönüştürür.

 """

from typing import List, Tuple, Set

# Duvar bit değerleri (Subject kuralı)
NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

# ANSI Renk Kodları (Terminali renklendirmek için kullanılan standart metinler)
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Kullanıcının 'c' tuşuna bastıkça sırayla geçebileceği renk paleti
WALL_COLORS = [WHITE, CYAN, GREEN, YELLOW, BLUE, RED]

#koordinat yolu
def path_to_coordinates(
    entry: Tuple[int, int], path_str: str
) -> Set[Tuple[int, int]]:

    # """ Yönsel bir yol dizgisini ('NESW') bir (x, y) koordinat kümesine dönüştürür.

    # Converts a directional path string ('NESW') into a set of (x, y) coordinates."""

    coords: Set[Tuple[int, int]] = {entry} #kordinatımı başlangıç noktasına eşitliyorum
    curr_x, curr_y = entry #curr mevcut konum

    moves = { # yönleri ayrıca sayısal kordinat olarak tanımlıyoruz
        "N": (0, -1),
        "S": (0, 1),
        "E": (1, 0),
        "W": (-1, 0),
    }
#step adım -- path_str algoritmanın sonucunu aldığı metin
# """ aşşadaki fonksiyon fonksiyondan aldığı kordinatlar olarak 
# gösteriyor onlara dönüştürüyo
# neden böyle birşey yapıyo bize sadece metin olark verdiğinde
# neresi uygunluk anlamayız o yüzden onları kordinata uygunlicaz """
    for step in path_str:
        if step in moves:
            dx, dy = moves[step]
            curr_x += dx
            curr_y += dy
            coords.add((curr_x, curr_y))

    return coords

#labirenti oluştur

# """ labirenti matrisi grid, başlangıç/bitiş noktalarını
#  ve isteğe bağlı çözüm yolunu görselleştirerek terminalde 
#  bastırılmaya uygun renklendirilmiş bir metin str döndürür """

def render_maze( 
        grid: List[List[int]], #labirentin yapısını 2d tutan matris
        entry: Tuple[int, int],#başlangıç noktası
        exit_coord: Tuple[int, int], #çıkış
        path_coord: Set[Tuple[int, int]], #çözüm yolunu bula kordinat kümesi
        show_path: bool = False, #çözüm yolunda var mı yok mu onu söyleyen bayrak
        wall_color: str = WHITE,# duvarların renk kodu
    ) -> str:


    height = len(grid) #labirentin yüksekliği
    width = len(grid[0]) #genişlik
    lines: List[str] = [] #oluşturulan tüm metin satırlarını sırayla saklayacak liste

   #range menzil.  
   #bu döngü ekrana basmak için uygun sırayı ayarlar ekrana
   #basılacak olan metni satır satır inşa eder
#    """ x ve y kodda sayısal olarak kullanılıyo çünkü range ile
#    istenen değere gelene kadar 0 den başlayarak sayısal değerini
#    arttırıyor"""
    for y in range(height): #en dış döngü başlangıcı labirentın her satırını yukardan aşşa işler her 
        top_line = "" #top_line adında boş bir string oluşturduk
        mid_line = ""
        for x in range(width): #iç döngü başlangıcı satırdaki hücreleri soldan sağa tek tek gezer 
            cell = grid[y][x] # ve ilgili hücrelerin duvar bilgisini cell alır
            #algoritma bize kordinatin kutularını cell kısmını bize sayısal değer 
            # olarak verir yönlerin toplamı bu da bize bit sayısal değerini
            #  ikilik sistemde söyler 0000 -> 0 0010 -> 2 dir 
            #  & (AND) işlemi "Bu iki sayı birbirine eşit mi?" diye bakmaz. "İki sayıda da aynı anda 1 olan basamak var mı?" diye baka
             
            # 1.tavanı (kuzey duvarı) ciz: cell & 1 != 0 ise duvar var
            top_line += f"{wall_color}+{RESET}" # burda köşelere parantez içindeki kodların görevinde + simgesi koymayı söyler daha sonra o rengi varsayılana getirir

            if cell & NORTH: #beirli bir hücrenin kuzey yönünde duvar mı yoksa geçit mi olduğunu kontrol eden mantıksal bir sorgudur
                top_line += f"{wall_color}---{RESET}"
            else:
                top_line += "   " # kuzeyinde bişey varsa --- koyar yoksa boşluk


            #2. sol duvarı (Batı Duvarı) çiz: cell & 8 != 0 ise duvar var
            if cell & WEST:
                mid_line += f"{wall_color}|{RESET}"
            else:
                mid_line += " "

            #3. hücrenin içini doldur (giriş, çıkış yol veya boşluk)
            coord = (x, y)
            if coord == entry:
                mid_line += f"{GREEN} E {RESET}"
            elif coord == exit_coord:
                mid_line += f"{RED} X {RESET}"
            elif show_path and coord in path_coord: #çözüm lyolu gösterilicekse (showpath) ve şu an baktığımız hücre çözüm yolundaysa onu işaretle
                mid_line += f"{YELLOW} \u00b7 {RESET}" #f"{YELLOW} · {RESET}" BUNUN ORTADAKİ NKTAya hata veriyo editör bunu araştır
            else:
                mid_line += "   "
        #satırın en sağını kapatma duvarları
        top_line += f"{wall_color}+{RESET}"
        last_cell = grid[y][width - 1] #y.satırdaki  en sağ hücre yi bulur
        if last_cell & EAST: # ensağdaki hücrenin tarafında duvar var mı
            mid_line += f"{wall_color}|{RESET}"
        else:
            mid_line += " "

        lines.append(top_line)
        lines.append(mid_line)

    bottom_line = "" # artık labirentin son aşşağıdaki kısımlarını çizelim
    for x in range(width):
        cell = grid[height - 1][x] #height -1 (labirentin en alt kısmı) 0 dan başlandığı için -1
        bottom_line += f"{wall_color}+{RESET}"
        if cell & SOUTH: 
            bottom_line += f"{wall_color}---{RESET}"
        else:
            bottom_line += "   "
    bottom_line += f"{wall_color}+{RESET}"
    lines.append(bottom_line)

    return "\n".join(lines) # kodda tüm satırları liste olarak tutarız 
# oyüzdendirki her listenin sonuna newline ekliyoruzki labirent aşşa doğru büyüsün
# join metodu listede sırası ile belirttiğiniz metinleri ayraç (burdaki \n) ile ayırmakdır

"""
aşşağıdaki kodun amacı terminal üzerinden labirentle etkileşime 
girmesini sağlar
Sonsuz bir döngü kurarak ekranı temizler
labirenti güncel ayarlarla ekrana basar ve kullanıcıdan gelen komutlara göre 
çözüm yolunu açıp lapatır, duvar rengini değiştirir veya programdan çıkar
"""

def interactive_loop( #etkileşimli döngü
        grid:List[List[int]], #labiret matrisi
        entry: Tuple[int, int], #başlangıç
        exit_coord: Tuple[int,int], #bitiş       
        path_coords: set[Tuple[int, int]], # çözüm yolunu oluşturan kordinat kümesi
) -> None: # fonksiyonun geriye bir değer döndürmediğini falan filan

    """yolları değiştirmek ve renkleri değiştirmek için 
    terminal etkileşim döngüsünü çaşlıştırır"""

    show_path = False #çözüm yolunu başlangıçta vermez
    color_index = 0 #listenin ilk rengini varsayılan beyaz seçmek için indeksi 0 olarak başlatır

    while True:# kullanıcı q tuşuna basana kadar çalışıcak sonsuz döngü
        print("\033[H\033[J", end="")#ANSI kaçış dizisidir (escape code).
        """terminal ekranındaki eski görüntüleri siler ve imleci sol üst köşeye taşır
        yani labirent kendi yerinden oynamaz akıcılık sağlanır
        böylece labirent üst üste birikmez aynı yerde güncellenir"""

        current_color = WALL_COLORS[color_index]
        rendered = render_maze( #döngünün her adımda labirenti güncel ayarla
            grid=grid, #seçilen renk yolun açık/kapalı olması vb tek bir metin haline getirir
            entry=entry, #terminale yazdırır ve kullanıcının basabileceği tuşları ekranda gösterir
            exit_coord=exit_coord,
            path_coord=path_coord,
            path_coords=path_coords,
            show_path=show_path,
            wall_color=current_color,
        )
        print(rendered)
        print("\n[s]: Çözümü Aç/Kapat | [c]: Renk Değiştir | [q]: Çıkış")

        try:
            cmd = input("\nKomut girin: ").strip().lower()#stript sağında solunda boşlukları siler lower küçük harfe çevirir
        except (KeyboardInterrupt, EOFError):#kullanıcı aniden ctrl+d veya ctrl+c ile programdan çıkarsa uygulamanın ççökmesini engeller
            print("\nÇıkılıyor...")
            break 

        if cmd == "s": # try komutunda aldığım girdi cmd 
            show_path = not show_path #çözüm yolu gösteren komutdur showpath bool olarak durur
        elif cmd == "c":
            color_index = (color_index + 1) % len(WALL_COLORS)#bir sonrakine geçmesi en sona geldiğinde ise ise tekrardan başa dönmesi için koyuldu
        elif cmd == "q":
            print("Görüşmek üzere")
            break