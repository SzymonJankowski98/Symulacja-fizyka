import tkinter
import random
import math
import numpy
import matplotlib.pylab as plt

W1 = 10
W2 = -10
RADIUS = 5
WIDTH = 500
HEIGHT = 500
TIME_LIMIT = 1000
ATOMS = 100
OUT_FILE = "Wykresik.txt"


def scalar(v1, v2):
    return v1[0]*v2[0]+v1[1]*v2[1]


def vector_value(v):
    return math.sqrt(v[0]**2+v[1]**2)


def degree_betwean(v1, v2):
    return math.degrees(math.acos(scalar(v1, v2)/(vector_value(v1)*vector_value(v2))))


def newx(v, degree):
    return vector_value(v)*math.cos(degree)


def newy(v, degree):
    return vector_value(v)*math.sin(degree)


class Atom:
    def __init__(self, rx, ry, radius, speed):
        self.r = [rx, ry]
        self.v = [random.random() * speed * 2 - speed, random.random() * speed * 2 - speed]
        self.radius = radius


class Simulation:
    def __init__(self, n):
        self.n = n
        self.w = self.w_counter()
        self.atoms = self.generator()
        self.deltat = 1 / (self.w)*100
        self.state = []
        self.state_counter = 0

    def w_counter(self):
        s = 0
        for i in range(self.n):
            s += W1 ** 2 + W2 ** 2
        return int(math.sqrt(s))

    def generator(self):
        tab = []
        speed = self.w / self.n * 2
        for i in range(10):
            #p1 = RADIUS+RADIUS/50
            #p2 = RADIUS+RADIUS/50
            for j in range(self.n // 10):
                '''if p2 < HEIGHT / 10:
                    tab.append(Atom(p1, p2 + i * (HEIGHT//10), RADIUS, speed))
                    p1 += 2*RADIUS + RADIUS / 50
                    if p1 > WIDTH/10:
                        p1 = RADIUS+RADIUS/50
                        p2 += 2*RADIUS+RADIUS/50
                else:
                    tab.append(Atom(random.randint(RADIUS, WIDTH // 10 - 1), random.randint(i * HEIGHT // 10 + 1, i * HEIGHT // 10 + HEIGHT // 10 - 1), RADIUS, speed))
                '''
                x = random.randint(RADIUS, WIDTH // 10 - 1)
                y = random.randint(i * HEIGHT // 10 + 1, i * HEIGHT // 10 + HEIGHT // 10 - 1)
                ok = self.no_crash(tab, x, y)
                while not ok:
                    x = random.randint(RADIUS, WIDTH // 10 - 1)
                    y = random.randint(i * HEIGHT // 10 + 1, i * HEIGHT // 10 + HEIGHT // 10 - 1)
                    ok = self.no_crash(tab, x, y)
                tab.append(Atom(x, y, RADIUS, speed))

        return tab

    def no_crash(self, tab, x, y):
        for i in tab:
            if math.sqrt((i.r[0] - x) ** 2 + (i.r[1] - y) ** 2) < RADIUS * 2 + RADIUS / 100:
                return False
        return True


    def loop(self):
        simulation_window.delete(tkinter.ALL)
        for i in self.atoms:
            simulation_window.create_oval(i.r[0] - i.radius, i.r[1] - i.radius, i.r[0] + i.radius, i.r[1] + i.radius, fill=('#%02x%02x%02x' % (0, 255, 0)))
        self.crash_atom()
        self.crash_wall()
        self.move()
        self.save_state()
        if (self.state_counter + 1) * self.deltat < TIME_LIMIT:
            main_window.after(1, self.loop)
        else:
            main_window.quit()

    def move(self):
        for i in self.atoms:
            i.r[0] += i.v[0] * self.deltat
            i.r[1] += i.v[1] * self.deltat

    def crash_wall(self):
        x = 1 / 100 * RADIUS
        for i in self.atoms:
            if i.r[0] + RADIUS > WIDTH + x or i.r[0] - RADIUS < 0 + x:
                i.v[0] = -i.v[0]
            if i.r[1] + RADIUS > HEIGHT - x or i.r[1] - RADIUS < 0 + x:
                i.v[1] = -i.v[1]

    def crash_atom(self):
        x = 1 / 100 * RADIUS
        for i in range(len(self.atoms)):
            for j in range(len(self.atoms)):
                if i != j and math.sqrt((self.atoms[j].r[0] - self.atoms[i].r[0]) ** 2 + (self.atoms[j].r[1] - self.atoms[i].r[1]) ** 2) < RADIUS * 2 + x:
                    tempvector = [self.atoms[i].r[0]-self.atoms[j].r[0], -(self.atoms[i].r[1]-self.atoms[j].r[1])]
                    di = degree_betwean(tempvector, self.atoms[i].v)
                    dj = degree_betwean(tempvector, self.atoms[j].v)
                    newi = [newx(self.atoms[i].v, di), newy(self.atoms[i].v, di) + newx(self.atoms[j].v, dj)]
                    newj = [newx(self.atoms[j].v, dj), newy(self.atoms[j].v, dj) + newx(self.atoms[i].v, di)]
                    tempvector = [1, 0]
                    di = degree_betwean(tempvector, newi)
                    dj = degree_betwean(tempvector, newj)
                    self.atoms[i].v = [newx(self.atoms[i].v, di), newy(self.atoms[i].v, di)]
                    self.atoms[j].v = [newx(self.atoms[j].v, dj), newy(self.atoms[j].v, dj)]

    def save_state(self):
        time = 0
        if self.state_counter == 0:
            time = self.deltat
        else:
            time = self.state[self.state_counter - 1][0] + self.deltat
        self.state.append([time])
        for i in range(len(self.atoms)):
            self.state[self.state_counter].append(
                [self.atoms[i].r[0], self.atoms[i].r[1], self.atoms[i].v[0], self.atoms[i].v[1]])
        self.state_counter += 1

    def excecice3(self):
        results = []
        for i in range(len(self.state)):
            result = [0] * 10 ** 4
            for j in range(1, len(self.state[0])):
                result[self.whitch_state(self.state[i][j])] += 1
            results.append([self.state[i][0], result])
        return results

    def whitch_state(self, atom):
        nx = int((atom[0] / WIDTH) * 10)
        if nx == 10:
            nx = 9
        ny = int((atom[1] / HEIGHT) * 10)
        if ny == 10:
            ny = 9
        nvx = int(((atom[2] + W1) / (2 * W1)) * 6)
        if nvx == 6:
            nvx = 5
        nvy = int(((atom[3] + W1) / (2 * W1)) * 6)
        if nvy == 6:
            nvy = 5
        return nx * 1000 + ny * 100 + nvx * 10 + nvy

    def excecice4(self, tab):
        N = math.factorial(ATOMS)
        results = []
        for i in range(len(tab)):
            temp = 1
            for j in range(0, len(tab[i][1])):
                if tab[i][1][j] > 0:
                    temp *= tab[i][1][j]
            # temps = math.exp(temp * math.log(temp) - temp)
            # result = N /(temps)
            results.append([tab[i][0], temp])
        return N, results

    def excecice5(self, N, tab):
        ns = math.log(N)
        results = []
        for i in range(len(tab)):
            ok = tab[i][1] * math.log(tab[i][1]) - tab[i][1]
            uno = ns - ok
            results.append([tab[i][0], uno])
        return results

    def saving(self, tab):
        file = open(OUT_FILE, "w")
        for i in range(len(tab)):
            file.write('{}\t{}\n'.format(tab[i][0], tab[i][1]))
        file.close()

    def chart(self, tab):
        x_axis = []
        y_axis = []
        for i in tab:
            x_axis.append(i[0])
            y_axis.append(i[1])
        plt.title("wykres")
        plt.plot(x_axis, y_axis, color='darkblue')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        plt.legend()
        plt.show()


main_window = tkinter.Tk()

simulation_window = tkinter.Canvas(main_window, width=WIDTH, height=HEIGHT, bg="Black")
simulation_window.pack()

sim = Simulation(ATOMS)
sim.loop()

main_window.mainloop()

x3 = sim.excecice3()
for j in range(len(x3)):
    l = 0
    for i in range(1, len(x3[0][1])):
        if x3[j][1][i] > 1:
            print(j, x3[j][1][i])
N, x4 = sim.excecice4(x3)
x5 = sim.excecice5(N, x4)
sim.chart(x5)