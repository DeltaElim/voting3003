from random import randint

def randomcandidates(n, field, SQSIDE, candidatesc):
    for i in range(n):
        placed = False
        while not placed:
            x = randint(0,SQSIDE - 1)
            y = randint(0,SQSIDE - 1)
            if field[y][x] == '.':
                field[y][x] = str(chr(i + 65))
                candidatesc.append((x,y))
                placed = True

def honest_vote(candidatesc, CANDIDATES, SQSIDE, voters):
    votestats = []
    for i in range(CANDIDATES):
        votestats.append(0)

    for y in range(SQSIDE):
        for x in range(SQSIDE):
            distances = []
            for i in range(CANDIDATES):
                distances.append((candidatesc[i][0]-x)**2+(candidatesc[i][1]-y)**2)
            index_min = min(range(len(distances)), key=distances.__getitem__)
            votestats[index_min] += 1
            voters[y][x] = str(chr(65 + int(index_min)))
    return votestats

def fptp(candidatesc, CANDIDATES, SQSIDE, voters, hvotestats):
    #votestats = honest_vote()
    first = int(max(range(len(hvotestats)), key=hvotestats.__getitem__))
    votenof = hvotestats.copy()
    votenof[first] = 0
    second = int(max(range(len(votenof)), key=votenof.__getitem__))
    votestats = []
    for i in range(CANDIDATES):
        votestats.append(0)

    for y in range(SQSIDE):
        for x in range(SQSIDE):
            distances = []
            for i in range(CANDIDATES):
                distances.append((candidatesc[i][0] - x) ** 2 + (candidatesc[i][1] - y) ** 2)
            minv = int(min(range(len(distances)), key=distances.__getitem__))
            if min(distances) <= 2:
                voters[y][x] = str(chr(65 + int(minv)))
                votestats[minv] += 1
            elif distances[first] < distances[second]:
                voters[y][x] = str(chr(65 + int(first)))
                votestats[first] += 1
            elif distances[first] > distances[second]:
                voters[y][x] = str(chr(65 + int(second)))
                votestats[second] += 1
            else:
                if randint(1,2) == 1:
                    voters[y][x] = str(chr(65 + int(first)))
                    votestats[first] += 1
                else:
                    voters[y][x] = str(chr(65 + int(second)))
                    votestats[second] += 1
    return votestats


def spoil(candidatesc, CANDIDATES, SQSIDE, spoilmap, firsth, voters):
    CANDIDATES += 1
    for x in range(SQSIDE):
        for y in range(SQSIDE):
            candidatesc.append((x,y))
            newhstats = honest_vote(candidatesc, CANDIDATES, SQSIDE, voters)
            if int(max(range(len(newhstats)), key=newhstats.__getitem__)) != firsth:
                if int(max(range(len(newhstats)), key=newhstats.__getitem__)) == CANDIDATES-1:
                    spoilmap[y][x] = 'X'
                else:
                    spoilmap[y][x] = 'Y'
            candidatesc.pop()
    CANDIDATES -= 1