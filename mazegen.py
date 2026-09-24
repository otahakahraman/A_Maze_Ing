"""Standalone maze generator module for the A-Maze-ing project.

Basic use::

    from mazegen import MazeGenerator

    generator = MazeGenerator(width=20, height=15, seed=42)
    generator.generator(x=0, y=0, perfect=False)
    maze = generator.grid
    solution = generator.find_short_path((0, 0), (19, 14))

``maze`` is a list of rows containing integer wall masks, not the exported
hexadecimal text format. Bits 1, 2, 4, and 8 represent north, east, south,
and west walls. ``solution`` is a string of N/E/S/W moves. Use different
width, height, and seed values to customize the generated maze.
"""

import random
from collections import deque



BIT={"N": 1, "E": 2, "S": 4, "W": 8}
OPPOSITE={"N":"S", "E":"W", "W":"E", "S":"N"}
DX_DY={"N":(0,-1), "S":(0,1), "E":(1,0), "W":(-1,0)}
PATTERN_42 :list[list[int]]= [ [1,0,0,0,1,1,1],
                               [1,0,0,0,0,0,1],
                               [1,1,1,0,1,1,1], 
                               [0,0,1,0,1,0,0],
                               [0,0,1,0,1,1,1]]

class MazeGenerator:
    def __init__(self ,width :int ,height :int,seed :int) -> None:
        self.height=height
        self.width=width
        self.grid: list[list[int]]=[[0xF for _ in range(width)] for _ in range( height)]
        self.rng=random.Random(seed)
        self.visited : list[list[bool]] = [[False for _ in range(width)] for _ in range (height)]


    def get_neighbours(self,x1:int ,y1:int) -> list[tuple[int,int]]:
        """Bulunduğu hücre ile komşu olan ve visit edilmemiş olan hücreleri döndürür."""
        res=[]
        for direction,(dx,dy)in DX_DY.items():
            nx,ny=x1+dx,y1+dy
            if ((0<=nx <=self.width-1) and (0<=ny <=self.height-1) and not self.visited[ny][nx]):
                res.append((nx,ny))
        return res

    def get_open_neighbours(self,x1:int ,y1:int) -> list[tuple[int,int]]:
        """Bulunduğu hücre ile komşu hücre arasındaki duvarın açık olduğu komşuları döndürür."""
        res=[]
        for direction,(dx,dy) in DX_DY.items():
            nx,ny=x1+dx,y1+dy
            if ((0<=nx<=self.width-1 and 0<=ny<=self.height-1) and ((self.grid[y1][x1]& BIT[direction])==0)):
                res.append((nx,ny))
        return res
    
    def get_all_neighbours(self,x:int ,y:int) -> list[tuple[int,int]]:
        """Bulunduğu hücre ile komşu olan tüm hücreleri döndürür."""
        res=[]
        for direction,(dx,dy)in DX_DY.items():
            nx,ny=x+dx,y+dy
            if ((0<=nx <=self.width-1) and (0<=ny <=self.height-1)):
                res.append((nx,ny))
        return res

    def find_direction(self,x1 : int, y1: int , x2 : int, y2: int) -> str:
        """Bulunduğu hücre ile komşu hücre arasındaki yönü döndürür. (N, S, E, W)"""
        dx,dy=x2-x1,y2-y1
        for direction,(ddx,ddy) in DX_DY.items():
            if(ddx,ddy)==(dx,dy):
                return direction
        raise ValueError(f"({x1},{y1}) ile ({x2},{y2}) komsu degil")

    def carve(self ,x1 : int, y1: int , x2 : int, y2: int) -> None:
        """Labirentteki iki hücre arasındaki duvarı kaldırır ve böylece bir geçit oluşturur."""

        direction=self.find_direction(x1,y1,x2,y2)
        opposite=OPPOSITE[direction]

        self.grid[y1][x1]&= ~BIT[direction]
        self.grid[y2][x2]&= ~BIT[opposite]

    def generator(self,x: int, y: int,perfect: bool) -> None:
        """fonksiyonların çalışmasını sağlar"""
        self.apply_pattern()
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
        if not perfect :
            try_again=self.width*self.height//2
            for _ in range (try_again):
                x1=self.rng.randrange(self.width)
                y1=self.rng.randrange(self.height)
                direct=self.rng.choice(list(BIT.keys()))
                opposite=OPPOSITE[direct]
                x2=x1+DX_DY[direct][0]
                y2=y1+DX_DY[direct][1]
                if not(0 <= x2 < self.width and 0 <= y2 < self.height):
                    continue
                if self.grid[y1][x1] == 0xF or self.grid[y2][x2] == 0xF:
                    continue
                if (self.grid[y1][x1]&BIT[direct]):
                    self.grid[y1][x1]&= ~BIT[direct]
                    self.grid[y2][x2]&= ~BIT[opposite]
            self.count_open_neigh_and_carve()
            self.fix_opens()

    def count_open_neigh_and_carve(self) -> None:
        """Labirentteki köşe hücreleri bulur ve rastgele bir komşu ile duvarı kaldırır. Bu işlem, labirentin daha karmaşık ve ilginç hale gelmesini sağlar."""
        corner_list:list[tuple[int,int]]=[]
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 0xF:
                    continue
                count=len(self.get_open_neighbours(x,y))
                if count<2 :
                    corner_list.append((x,y))

        while (len(corner_list)>2):
            cx,cy = self.rng.choice(corner_list)
            neigh = set(self.get_all_neighbours(cx,cy))
            n_neight = neigh - set(self.get_open_neighbours(cx, cy))
            n_neight = {c for c in n_neight if self.grid[c[1]][c[0]] != 0xF}
            if not n_neight:
                corner_list.remove((cx, cy))
                continue
            s_carve=self.rng.choice(list(n_neight))   
            ccx,ccy=s_carve

            self.carve(cx,cy,ccx,ccy)
            corner_list.remove((cx,cy))

    def find_short_path(self,entry:tuple[int,int],uscite:tuple[int,int]) -> str:
        """Labirentteki en kısa çözüm yolunu bulur."""
        queue=deque([entry])  
        visited_bfs={entry}
        came_from:dict[tuple[int,int],tuple[int,int]]={}
        while(queue):
            current=queue.popleft()
            if current==uscite:
                break
            x,y=current
            for neighbor in self.get_open_neighbours(x,y):
                if neighbor not in visited_bfs:
                    visited_bfs.add(neighbor)
                    came_from[neighbor]=current
                    queue.append(neighbor)
        current=uscite
        if uscite not in visited_bfs:
            raise ValueError("Giriş ile çıkış arasında açık bir yol yok")
        road=""   

        while(current!=entry):
            before=came_from[current]
            sx,sy=before
            dx,dy=current
            road=self.find_direction(sx,sy,dx,dy) +road
            current=before
        return road

    def apply_pattern(self) -> None:
        """Labirent üzerine '42' desenini uygular."""
        pattern_height=len(PATTERN_42)
        pattern_width=len(PATTERN_42[0])
        if(self.width<pattern_width or self.height<pattern_height ):
            print("Grid '42' desenine sigacak kadar buyuk degil, desen atlaniyor.")
            return
        
        offset_y = (self.height-pattern_height)//2
        offset_x = (self.width-pattern_width)//2
        if self.width % 2 == 0:
            offset_x += 1
        for py in range(pattern_height):
            for px in range(pattern_width):
                if (PATTERN_42[py][px] == 1 ):
                    gx=offset_x+px
                    gy=offset_y+py
                    self.grid[gy][gx]=0xF
                    self.visited[gy][gx]=True

                    


    def add_wall(self,x1:int,y1:int,x2:int,y2:int) -> None:
        """Labirentteki iki hücre arasına duvar ekler."""
        direction=self.find_direction(x1,y1,x2,y2)
        opposite=OPPOSITE[direction]
        self.grid[y1][x1]|= BIT[direction]
        self.grid[y2][x2]|= BIT[opposite]

    def fix_opens(self) -> None:
        """3x3'lük boş alan taraması yapar ve duvar atar."""
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                fully_open = True

                for row in range(y, y + 3):
                    for col in range(x, x + 2):
                        if (self.grid[row][col] & BIT["E"] or
                                self.grid[row][col + 1] & BIT["W"]):
                            fully_open = False

                for row in range(y, y + 2):
                    for col in range(x, x + 3):
                        if (self.grid[row][col] & BIT["S"] or
                                self.grid[row + 1][col] & BIT["N"]):
                            fully_open = False

                if fully_open:
                    self.add_wall(x + 1, y + 1, x + 2, y + 1)

    def write_to_file(self, output_file: str, entry:tuple[int,int], uscite:tuple[int,int]) -> None:
        """Labirenti ve çözüm yolunu belirtilen dosyaya yazar."""
        with open(output_file,"w") as f:
            for row in self.grid:
                line="".join(f"{cell:x}" for cell in row)
                f.write(line+"\n")
            f.write("\n")  
            f.write(f"{entry[0]},{entry[1]}\n{uscite[0]},{uscite[1]}\n")
            f.write(self.find_short_path(entry,uscite))
            f.write("\n") 

    def control(self,entry:tuple[int,int] , uscite:tuple[int,int]) -> None:
        """Giriş ve çıkış koordinatlarının geçerliliğini kontrol eder."""
        entry_x=entry[0]
        entry_y=entry[1]
        uscite_x=uscite[0]
        uscite_y=uscite[1]
        if entry == uscite:
            raise ValueError("Giriş ve çıkış aynı olamaz")

        if(0>entry_x or entry_x>=self.width or 0>entry_y or entry_y>=self.height):
            raise ValueError("Giriş koordinatları geçersiz!")
        if(0>uscite_x or uscite_x>=self.width or 0>uscite_y or uscite_y>=self.height):
            raise ValueError("Çıkış koordinatları geçersiz!")
        if(self.grid[entry_y][entry_x] == 0xF or self.grid[uscite_y][uscite_x] == 0xF):
            raise ValueError("Giriş ve çıkışlar pattern üzerinde olamaz!")
