import random
from collections import deque

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

    def get_neighbours(self,x1:int ,y1:int):#bulunduğu noktanın her komşusunu yazar
        res=[]
        for direction,(dx,dy)in DX_DY.items():
            nx,ny=x1+dx,y1+dy
            if ((0<=nx <=self.width-1) and (0<=ny <=self.height-1) and not self.visited[ny][nx]):
                res.append((nx,ny))
        return res

    def get_open_neighbours(self,x1:int ,y1:int):#bulunduğu noktanın gidilebilecek(duvar olmayan) komşusunu yazar
        res=[]
        for direction,(dx,dy) in DX_DY.items():
            nx,ny=x1+dx,y1+dy
            if ((0<=nx<=self.width-1 and 0<=ny<=self.height-1) and ((self.grid[y1][x1]& BIT[direction])==0)):
                res.append((nx,ny))
        return res

    def find_direction(self,x1 : int, y1: int , x2 : int, y2: int):#bulunduğu noktanın, senin verdiğin noktanın neresinde olduğunu yazar
        dx,dy=x2-x1,y2-y1
        for direction,(ddx,ddy) in DX_DY.items():
            if(ddx,ddy)==(dx,dy):
                return direction
        raise ValueError(f"({x1},{y1}) ile ({x2},{y2}) komsu degil")

    def carve(self ,x1 : int, y1: int , x2 : int, y2: int):#labirenti deler
        direction=self.find_direction(x1,y1,x2,y2)
        opposite=OPPOSITE[direction]

        self.grid[y1][x1]&= ~BIT[direction]
        self.grid[y2][x2]&= ~BIT[opposite]

    def generator(self,x: int, y: int,perfect: bool):#yukardaki fonksiyonların çalışmasını sağlar
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
                if not(0<=x2<self.width and 0<=y2<self.height ):
                    continue
                if (self.grid[y1][x1]&BIT[direct]):
                    self.grid[y1][x1]&= ~BIT[direct]
                    self.grid[y2][x2]&= ~BIT[opposite]
            self.count_open_neigh_and_carve()
    def get_all_neighbours(self,x:int ,y:int):
        res=[]
        for direction,(dx,dy)in DX_DY.items():
            nx,ny=x+dx,y+dy
            if ((0<=nx <=self.width-1) and (0<=ny <=self.height-1)):
                res.append((nx,ny))
        return res

    def count_open_neigh_and_carve(self):
        corner_list:list[tuple[int,int]]=[]
        for y in range(self.height):
            for x in range(self.width):
                count=len(self.get_open_neighbours(x,y))
                if count<2:
                    corner_list.append((x,y))

        while (len(corner_list)>2):
            cx,cy=self.rng.choice(corner_list)
            neigh=set(self.get_all_neighbours(cx,cy))
            n_neight=neigh-set(self.get_open_neighbours(cx,cy))
            if not n_neight:
                corner_list.remove((cx, cy))
                continue
            s_carve=self.rng.choice(list(n_neight))   
            ccx,ccy=s_carve

            self.carve(cx,cy,ccx,ccy)
            corner_list.remove((cx,cy))



    
    def find_short_path(self,entry:tuple[int,int],uscite:tuple[int,int]) -> str:#çözüm için en kısa yolu bulur
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
        road=""   

        while(current!=entry):
            before=came_from[current]
            sx,sy=before
            dx,dy=current
            road=self.find_direction(sx,sy,dx,dy) +road
            current=before
        return road
    
    def write_to_file(self, output_file: str, entry:tuple[int,int], uscite:tuple[int,int]):#labirenti, giriş çıkışı ve çözüm yolunu verdiğin isimdeki dosyaya yazar
        with open(output_file,"w") as f:
            for row in self.grid:
                line="".join(f"{cell:x}" for cell in row)
                f.write(line+"\n")
            f.write("\n")  
            f.write(f"{entry[0]},{entry[1]}\n{uscite[0]},{uscite[1]}\n")
            f.write(self.find_short_path(entry,uscite))
            f.write("\n") 


if __name__=="__main__":
    gen=MazeGenerator(4,4,2)
    for i in gen.grid:
        print(i)

    gen.generator(0,0,False)
    for i in gen.grid:
            print(i)
    gen.write_to_file("a.txt",(0,0),(3,3))


