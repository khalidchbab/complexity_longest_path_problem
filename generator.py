import random

def generate(nbr_sommets):
    l_sommet = []
    for i in range(nbr_sommets):
        for j in range(i+1, nbr_sommets):
            p = random.random()
            if p > 0.4:
                poid = random.randrange(0, 50)
                l_sommet.append((i, j, poid))

    return l_sommet

def main():
    nbr_files = 5
    max_sommets = 50
    for n in range(nbr_files):
        with open('graph' + str(n), 'w') as f:
            nbr_sommets = random.randrange(20, max_sommets)
            f.write("%d\n" % nbr_sommets)
            sommets = generate(nbr_sommets)
            for s in sommets:
                f.write("%d %d %d\n" % (s[0], s[1], s[2]))

                
if __name__ == '__main__':
    main()