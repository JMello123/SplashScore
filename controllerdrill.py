
class ControllerDrill():
    def __init__(self,**kwargs):
        self.status = {
            'point': 0,
            'attempt':0,
            'accuracy':.0,
            'sequence':[0,0],
            'best_sequence':0,
            'worst_sequence':0,
            'last_ten': [0,0,0,0,0,0,0,0,0,0]
        }

    def increment_point(self,*args):
        self.status['point'] += 1
        self.status['attempt'] += 1
        self.status['accuracy'] = self.status['point']/self.status['attempt']
        self.status['sequence'][0] += 1
        self.status['sequence'][1] = 0
        self._check_sequence()
        last_points = self._update_last_ten(is_point=True)
        text = str(self.status['point'])+ '/' +str(self.status['attempt']) + ' -> ' + str(round(self.status['accuracy']*100,1))+ '%'
        return text, last_points

    def increment_error(self, *args):
        self.status['attempt'] += 1
        self.status['accuracy'] = self.status['point']/self.status['attempt']
        self.status['sequence'][0] = 0
        self.status['sequence'][1] += 1
        self._check_sequence()
        last_points = self._update_last_ten()
        text = str(self.status['point'])+ '/' +str(self.status['attempt']) + ' -> ' + str(round(self.status['accuracy']*100,1))+ '%'
        return text, last_points
        
    def _check_sequence(self):
        '''
        Change the longest streak of every throw
        '''
        if self.status['sequence'][0] > self.status['best_sequence']:
            self.status['best_sequence'] = self.status['sequence'][0]
        if self.status['sequence'][1] > self.status['worst_sequence']:
            self.status['worst_sequence'] = self.status['sequence'][1]

    def _update_last_ten(self, is_point:bool = False):
        '''
        is_point: True if point is incremented
        return: list
        0: for non played
        1: for splash
        2: for wrong
        '''
        self.status['last_ten'].pop(0)
        if is_point:
            self.status['last_ten'].append(1)
            return self.status['last_ten']
        if not is_point:
            self.status['last_ten'].append(2)
            return self.status['last_ten']

    def reset_status(self):
        self.status['point'] = 0
        self.status['attempt'] = 0
        self.status['accuracy'] = .0
        self.status['best_sequence'] = 0
        self.status['sequence'] = [0,0]
        self.status['worst_sequence'] = 0
        self.status['last_ten'] = [0,0,0,0,0,0,0,0,0,0]
