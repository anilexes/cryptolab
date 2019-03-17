import numpy as np

class LFSR:
    # Инициализация алгоритма, задание полинома и начального состояния
    def __init__(self, polinom=[4, 1], initstate=[]):

        # Пустое начальное состояние - генерируем его рандомно
        if not len(initstate):
            while not 1 in initstate:
                initstate = np.random.randint(0,2,np.max(polinom))

        # Необходимые для алгоритма переменные
        self.initstate = initstate
        self.polinom = polinom
        self.state = self.initstate.astype(int)
        self.count = 1
        self.sequence = self.polinom[-1]
        self.outbit = -1
        self.feedbackbit = -1
        self.M = self.initstate.shape[0]
        self.expectedPeriod = 2**self.M -1
        self.polinom.sort(reverse=True)
        feed = ' '
        for i in range(len(self.polinom)):
            feed = feed + 'x^'+str(self.polinom[i])+' + '
        feed = feed + '1'
        self.feedpoly = feed
        self.byte_n = 0

    # Можно вывести информацию о сгенерированной последовательности
    def info(self):
        print('%d-битный LFSR с полиномом: %s' %(self.M,self.feedpoly))
        print('Периодичность: ',self.expectedPeriod)
        print('Итерация : ', self.count)
        print('Выходной бит : ', self.outbit)
        print(' : ',self.feedbackbit)
        if self.count>0 and self.count<1000:
            print(' Output Sequence %s'%(''.join([str(int(x)) for x in self.sequence])))
    

    # Шаг для генерирования последовательности поэлементно
    def step(self):
        b = np.logical_xor(self.state[self.polinom[0]-1], self.state[self.polinom[1]-1])
        if len(self.polinom) > 2:
            for i in range(2, len(self.polinom)):
                b = np.logical_xor(self.state[self.polinom[i]-1],b)
        
        self.state = np.roll(self.state, 1)
        self.state[0] = b*1
        self.feedbackbit = b*1
        if self.count==0:
            self.sequence = self.state[-1]
        else:
            self.sequence = np.append(self.sequence, self.state[-1])
        self.outbit = self.state[-1]
        self.count +=1
        return self.state[-1]

    # Выполнение алгоритма
    def process(self):
        for i in range(self.expectedPeriod):
            self.step()
        return self.sequence

    # Возвращение итоговой последовательности в виде строки
    def getMSequence(self):
        return ''.join([str(int(x)) for x in self.sequence])

    # Метод, позволяющий взять следующий байт сгенерированной последовательности, бесконечно, столько, сколько нужно
    def getByte(self):
        if self.expectedPeriod < 8:
            self.sequence = (self.sequence * 4)[:8]        

        res = self.sequence[self.byte_n:self.byte_n+8]
        if len(res) < 8:
            self.byte_n = 8 - len(res)
            res = np.append(res,self.sequence[:self.byte_n])
        else:
            self.byte_n += 8

        return res
