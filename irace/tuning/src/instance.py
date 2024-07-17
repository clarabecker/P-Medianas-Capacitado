class Instance:
    # General
    N        = None
    distance = None
    dem      = None
    cap      = None
    p        = None


    # Auxiliary
    penalty = None

    def __init__(self, path):
        self._read(path)
        self._compute_penalty()

    def _compute_penalty(self):
        max_dists = 0
        for line in self.distance:
            max_dists += max(line)
        self.penalty = max_dists

    def _read(self, path):
        file = open(path, 'r')
        lines = file.readlines()
        #
        index = 0
        while len(lines[index].strip()) == 0 or lines[index][0] == '#' or lines[index][0] == ' ':
            index += 1
        #
        self.N = int(lines[index].strip())
        index += 1
        self.p = int(lines[index].strip())
        index += 1
        self.cap = int(lines[index].strip())
        index += 1
        self.dem = [int(x) for x in lines[index].strip().split()]
        index += 1
        #
        self.distance = [[0] * self.N for _ in range(self.N)]
        for line in lines[index:]:
            content = line.strip().split()
            i = int(content[0])
            j = int(content[1])
            dist = int(content[2])
            self.distance[i][j] = dist
            self.distance[j][i] = dist
        file.close()

