import random
BIT={"N": 1, "E": 2, "S": 4, "W": 8}
OPPOSITE={"N":"S", "E":"W", "W":"E", "S":"N"}
DX_DY={"N":(0,-1), "S":(0,1), "E":(1,0), "W":(-1,0)}

class MazeGenerator:
    def __init__(self ,width :int ,height :int,seed :int) -> None:
        self.height=height
        self.width=width
        self.grid: list[list[int]]=[[0xF for _ in range(width)] for _ in range( height)]
        self.rng=random.Random(seed)
        self.visited : list[list[bool]] = [[False for _ in range(width)] for _ in range (height)]

    def get_neighbours(self,x1:int ,y1:int):
        res=[]
        for direction,(dx,dy)in DX_DY.items():
            nx,ny=x1+dx,y1+dy
            if ((0<=nx <=self.width-1) and (0<=ny <=self.height-1) and not self.visited[ny][nx]):
                res.append((nx,ny))
        return res

    def get_open_neighbours(self,x1:int ,y1:int):
        res=[]
        for direction,(dx,dy) in DX_DY.items():
            nx,ny=x1+dx,y1+dy
            if ((0<=nx<=self.width-1 and 0<=ny<=self.height-1) and ((self.grid[y1][x1]& BIT[direction])==0)):
                res.append((nx,ny))
        return res
        

    def find_direction(self,x1 : int, y1: int , x2 : int, y2: int):
        dx,dy=x2-x1,y2-y1
        for direction,(ddx,ddy) in DX_DY.items():
            if(ddx,ddy)==(dx,dy):
                return direction
        raise ValueError(f"({x1},{y1}) ile ({x2},{y2}) komsu degil")

    def carve(self ,x1 : int, y1: int , x2 : int, y2: int):
        direction=self.find_direction(x1,y1,x2,y2)
        opposite=OPPOSITE[direction]

        self.grid[y1][x1]&= ~BIT[direction]
        self.grid[y2][x2]&= ~BIT[opposite]

    def generator(self,x: int, y: int):
        stack:list[tuple[int,int]]=[(x,y)]
        self.visited[y][x]=True
        while(stack):
            cx,cy=stack[-1]
            neigh=self.get_neighbours(cx,cy)

            if(neigh):
                xn,yn=self.rng.choice(neigh)
                self.carve(cx,cy,xn,yn)
                self.visited[yn][xn]=True
                stack.append((xn,yn))
            else:
                stack.pop()
        
    def find_short_path(self,entry:tuple[int,int],uscite:tuple[int,int]):
        from collections import deque



if __name__=="__main__":
    gen=MazeGenerator(4,4,41)
    for i in gen.grid:
        print(i)

    gen.generator(0,0)
    for i in gen.grid:
            print(i)
    

        
    



































# import random







# BIT = {"N": 1, "E": 2, "S": 4, "W": 8}
# OPPOSITE = {"N": "S", "E": "W", "S": "N", "W": "E"}
# DX_DY = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}


# class MazeGenerator:
#     def __init__(self, width: int, height: int, seed: int | None = None) -> None:
#         self.width = width
#         self.height = height
#         # Her hücre başlangıçta 0xF: tüm duvarlar kapalı
#         self.grid: list[list[int]] = [
#             [0xF for _ in range(width)] for _ in range(height)
#         ]
#         self.visited: list[list[bool]] = [
#             [False for _ in range(width)] for _ in range(height)
#         ]
#         # seed verilirse random.seed() ile aynı labirent tekrar üretilebilir
#         self.rng = random.Random(seed)

#     def get_neighbors(self, x: int, y: int) -> list[tuple[str, int, int]]:
#         """Grid sınırları içindeki tüm komşuları döndürür."""
#         neighbors = []
#         for direction, (dx, dy) in DX_DY.items():
#             nx, ny = x + dx, y + dy
#             if 0 <= nx < self.width and 0 <= ny < self.height:
#                 neighbors.append((direction, nx, ny))
#         return neighbors

#     def remove_wall(
#         self, x1: int, y1: int, direction: str, x2: int, y2: int
#     ) -> None:
#         """İki komşu hücre arasındaki duvarı kaldırır (her iki tarafı da günceller)."""
#         self.grid[y1][x1] &= ~BIT[direction]
#         self.grid[y2][x2] &= ~BIT[OPPOSITE[direction]]

#     def carve_from(self, x: int, y: int) -> None:
#         """Recursive Backtracker: (x, y)'den başlayıp tüm ulaşılabilir
#         hücreleri gezerek bir spanning tree (perfect maze) oluşturur.
#         """
#         self.visited[y][x] = True

#         # Komşuları al, ziyaret edilmemiş olanları filtrele
#         neighbors = self.get_neighbors(x, y)
#         unvisited = [
#             (d, nx, ny) for d, nx, ny in neighbors if not self.visited[ny][nx]
#         ]

#         # Sıralarını karıştır — labirentin her seferinde farklı çıkmasını sağlar
#         self.rng.shuffle(unvisited)

#         for direction, nx, ny in unvisited:
#             # shuffle sonrası bir önceki adımda bu komşu ziyaret edilmiş olabilir
#             # (başka bir dal üzerinden ulaşılmış olabilir), tekrar kontrol şart
#             if self.visited[ny][nx]:
#                 continue

#             self.remove_wall(x, y, direction, nx, ny)
#             self.carve_from(nx, ny)   # <-- recursive çağrı: yeni hücreden devam et
#             # bu satırdan sonrasına geldiğimizde, nx,ny'nin tüm dalları bitmiş
#             # demektir -> otomatik olarak "geri dönmüş" oluyoruz (backtrack)


# # --- Kullanım örneği ---
# maze = MazeGenerator(width=3, height=3, seed=42)
# maze.carve_from(0, 0)   # (0,0)'dan başlayarak tüm labirenti oluştur

# for row in maze.grid:
#     print(" ".join(format(cell, "x") for cell in row))