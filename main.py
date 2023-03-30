import pygame
import sys

from funcs import *



field = []
filler = []
spoilmap = []
SQSIDE = 20
CANDIDATES = 0
for i in range(SQSIDE):
    filler.append('.')
for m in range(SQSIDE):
    field.append(filler.copy())

for m in range(SQSIDE):
    spoilmap.append(filler.copy())
voters = field.copy()
candidatesc = []




#visuals vvvvvvv
pygame.init()

screen = pygame.display.set_mode((505, 405))
# r = pygame.Rect(0,0,20,20)
# pygame.draw.rect(screen, (255, 0, 0), r, 0)
CELLSIZE = 20
y=0
while y!= CELLSIZE*21:
    pygame.draw.line(screen, (255,255,255), (0,y), (CELLSIZE*20,y), 3)
    y+=CELLSIZE
x=0
while x!= CELLSIZE*21:
    pygame.draw.line(screen, (255,255,255), (x,0), (x,CELLSIZE*20), 3)
    x+=CELLSIZE

pygame.draw.line(screen, (255,255,255), (CELLSIZE*22,20), (CELLSIZE*23,20), 3)
pygame.draw.line(screen, (255,255,255), (CELLSIZE*22,40), (CELLSIZE*23,40), 3)
pygame.draw.line(screen, (255,255,255), (CELLSIZE*22,20), (CELLSIZE*22,40), 3)
pygame.draw.line(screen, (255,255,255), (CELLSIZE*23,20), (CELLSIZE*23,40), 3)

def vis():
    for x in range(SQSIDE):
        for y in range(SQSIDE):
            r = pygame.Rect(x*20+2, y*20+2, 17, 17)
            if voters[y][x] == 'A':
                pygame.draw.rect(screen, (255, 0, 0), r, 0)
            elif voters[y][x] == 'B':
                pygame.draw.rect(screen, (0, 0, 255), r, 0)
            elif voters[y][x] == 'C':
                pygame.draw.rect(screen, (0, 255, 0), r, 0)
            elif voters[y][x] == 'D':
                pygame.draw.rect(screen, (255, 255, 0), r, 0)
            elif voters[y][x] == 'E':
                pygame.draw.rect(screen, (0, 255, 255), r, 0)
            elif voters[y][x] == 'F':
                pygame.draw.rect(screen, (255, 0, 255), r, 0)
            elif voters[y][x] == 'G':
                pygame.draw.rect(screen, (150, 0, 255), r, 0)
            else:
                pygame.draw.rect(screen, (175, 255, 0), r, 0)
            if (x,y) in candidatesc:
                r = pygame.Rect(x * 20 + 6, y * 20 + 6, 9, 9)
                pygame.draw.rect(screen, (0, 0, 0), r, 0)
            if spoilmap[y][x] == 'X':
                r = pygame.Rect(x * 20 + 4, y * 20 + 4, 13, 13)
                pygame.draw.rect(screen, (0, 0, 0), r, 0)
            if spoilmap[y][x] == 'Y':
                r = pygame.Rect(x * 20 + 4, y * 20 + 4, 13, 13)
                pygame.draw.rect(screen, (100, 100, 100), r, 0)

def winnerupdate(hvotestats):
    r = pygame.Rect(22 * 20 + 2, 1 * 20 + 2, 17, 17)
    first = int(max(range(len(hvotestats)), key=hvotestats.__getitem__))
    if first == 0:
        pygame.draw.rect(screen, (255, 0, 0), r, 0)
    elif first == 1:
        pygame.draw.rect(screen, (0, 0, 255), r, 0)
    elif first == 2:
        pygame.draw.rect(screen, (0, 255, 0), r, 0)
    elif first == 3:
        pygame.draw.rect(screen, (255, 255, 0), r, 0)
    elif first == 4:
        pygame.draw.rect(screen, (0, 255, 255), r, 0)
    elif first == 5:
        pygame.draw.rect(screen, (255, 0, 255), r, 0)
    elif first == 6:
        pygame.draw.rect(screen, (150, 0, 255), r, 0)
    else:
        pygame.draw.rect(screen, (175, 255, 0), r, 0)
#//////


#honest_vote(candidatesc, CANDIDATES, SQSIDE, voters)
#hstats = honest_vote(candidatesc, CANDIDATES, SQSIDE, voters)
#winnerupdate(hstats)
#fptp(candidatesc, CANDIDATES, SQSIDE, voters, hstats)
#vis()







while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            psx, psy = pygame.mouse.get_pos()
            psx = psx - (psx % 20)
            psy = psy - (psy % 20)
            if (psx/20, psy/20) not in candidatesc:
                if CANDIDATES != 8:
                    candidatesc.append((psx/20, psy/20))
                    CANDIDATES+=1
                    r = pygame.Rect(psx + 6, psy + 6, 9, 9)
                    pygame.draw.rect(screen, (255, 255, 255), r, 0)
            else:
                candidatesc.remove((psx/20, psy/20))
                CANDIDATES-=1
                r = pygame.Rect(psx + 6, psy + 6, 9, 9)
                pygame.draw.rect(screen, (0, 0, 0), r, 0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                CANDIDATES = 8
                randomcandidates(CANDIDATES, field, SQSIDE, candidatesc)
            if event.key == pygame.K_h:
                spoilmap = []
                for m in range(SQSIDE):
                    spoilmap.append(filler.copy())

                honest_vote(candidatesc, CANDIDATES, SQSIDE, voters)
                hstats = honest_vote(candidatesc, CANDIDATES, SQSIDE, voters)
                winnerupdate(hstats)
                vis()
            if event.key == pygame.K_s:
                hstats = honest_vote(candidatesc, CANDIDATES, SQSIDE, voters)
                firsth = int(max(range(len(hstats)), key=hstats.__getitem__))
                spoil(candidatesc, CANDIDATES, SQSIDE, spoilmap, firsth, voters)
                honest_vote(candidatesc, CANDIDATES, SQSIDE, voters)
                vis()
            if event.key == pygame.K_f:
                hstats = honest_vote(candidatesc, CANDIDATES, SQSIDE, voters)
                fptp(candidatesc, CANDIDATES, SQSIDE, voters, hstats)
                fstats = fptp(candidatesc, CANDIDATES, SQSIDE, voters, hstats)
                winnerupdate(fstats)
                vis()
    pygame.display.flip()

