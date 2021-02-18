class statsByQuery():

    def __init__(self, query):
        self.queryset = query.values()

    def getTotal(self):
        total = 0
        correct = 0
        for item in self.queryset:
            total += item['total']
            correct += item['correct']

        return {'total': total, 'correct': correct}
