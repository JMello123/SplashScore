
class ControllerDrill():
    def __init__(self,**kwargs):
        self._status = {
                    'point': 0,
                    'attempt':0,
                    'accuracy':.0,
                    'current_sequence_point': 0,
                    'current_sequence_errors': 0,
                    'best_sequence':0,
                    'worst_sequence':0,
                    'last_shots': [0,0,0,0,0,0,0,0,0,0,0]
                    }
        self.status_cache = [self._status.copy()]*2
        print('inicializando cache:',['last',
                self.status_cache[0]['point'],
                self.status_cache[0]['attempt'],
                'sequencia anterior',
                self.status_cache[1]['best_sequence'],
                self.status_cache[1]['worst_sequence'],
                'current',
                self.status_cache[1]['point'],
                self.status_cache[1]['attempt']],
                'sequencia atual',
                self.status_cache[1]['best_sequence'],
                self.status_cache[1]['worst_sequence'])

    @property
    def status(self):
        return self._status

    def get_last_shots(self):
        return self._status['last_shots']

    def increment_point(self, pos_min_ball_render=1, is_rollback=False , *args):
        self._status['point'] += 1
        self._status['attempt'] += 1
        self._status['accuracy'] = self._status['point']/self._status['attempt']
        self._status['current_sequence_point'] += 1
        self._status['current_sequence_errors'] = 0
        self._check_sequence() 
        if is_rollback:
            assert(pos_min_ball_render < 1)
            self._status['last_shots'].pop()
            self._status['last_shots'].append(1)
            self._update_status_cache()
            print('ACERTOU cache ao retornar do rollback:',
            ['last',
                self.status_cache[0]['point'],
                self.status_cache[0]['attempt'],
                'sequencia anterior',
                self.status_cache[1]['best_sequence'],
                self.status_cache[1]['worst_sequence'],
                'current',
                self.status_cache[1]['point'],
                self.status_cache[1]['attempt']],
                'sequencia atual',
                self.status_cache[1]['best_sequence'],
                self.status_cache[1]['worst_sequence'])
            return {'point': self._status['point'],
                    'attempt':self._status['attempt'],
                    'accuracy':self._status['accuracy'],
                    'last_shots':self._status['last_shots']
                    }
        else:
            self._update_last_shots(is_point=True)# atualiza os last_shots no modo normal 
            self._update_status_cache()
            print("ACERTOU cache:",[
                    'last',
                    self.status_cache[0]['point'],
                    self.status_cache[0]['attempt'],
                    'sequencia anterior',
                    self.status_cache[1]['best_sequence'],
                    self.status_cache[1]['worst_sequence'],
                    'current',
                    self.status_cache[1]['point'],
                    self.status_cache[1]['attempt']],
                    'sequencia atual',
                    self.status_cache[1]['best_sequence'],
                    self.status_cache[1]['worst_sequence'])
            return {'point': self._status['point'],
                    'attempt':self._status['attempt'],
                    'accuracy':self._status['accuracy'],
                    'last_shots':self._status['last_shots']
                    }

    def increment_error(self, pos_min_ball_render=1, is_rollback=False, *args):
        self._status['attempt'] += 1
        self._status['accuracy'] = self._status['point']/self._status['attempt']
        self._status['current_sequence_point'] = 0
        self._status['current_sequence_errors'] += 1
        self._check_sequence()
        if is_rollback:
            assert(pos_min_ball_render < 1)
            self._status['last_shots'].pop()
            self._status['last_shots'].append(2)
            self._update_status_cache()
            print('ERROU cache ao retornar do rollback:',[
                    'last',
                    self.status_cache[0]['point'],
                    self.status_cache[0]['attempt'],
                    'sequencia anterior',
                    self.status_cache[1]['best_sequence'],
                    self.status_cache[1]['worst_sequence'],
                    'current',
                    self.status_cache[1]['point'],
                    self.status_cache[1]['attempt']],
                    'sequencia atual',
                    self.status_cache[1]['best_sequence'],
                    self.status_cache[1]['worst_sequence'])
            return {'point': self._status['point'],
                    'attempt':self._status['attempt'],
                    'accuracy':self._status['accuracy'],
                    'last_shots':self._status['last_shots']
                 }
        else:
            self._update_last_shots()
            self._update_status_cache()
            print('ERROU cache', ['last',
                    self.status_cache[0]['point'],
                    self.status_cache[0]['attempt'],
                    'sequencia anterior',
                    self.status_cache[1]['best_sequence'],
                    self.status_cache[1]['worst_sequence'],
                    'current',
                    self.status_cache[1]['point'],
                    self.status_cache[1]['attempt']],
                    'sequencia atual',
                    self.status_cache[1]['best_sequence'],
                    self.status_cache[1]['worst_sequence'])
            return {'point': self._status['point'],
                    'attempt':self._status['attempt'],
                    'accuracy':self._status['accuracy'],
                    'last_shots':self._status['last_shots']
                 }

    def rollback_status(self):
        '''
        Change the attr:`status` to the previous state
        - Return: attr:`status`
        '''
        self._status = self.status_cache[0]
        self.status_cache[1] = self.status_cache[0].copy()
        print('Cache ao voltar:',['last',
        self.status_cache[0]['point'],
        self.status_cache[0]['attempt'],
        'sequencia anterior',
        self.status_cache[1]['best_sequence'],
        self.status_cache[1]['worst_sequence'],
        'current',
        self.status_cache[1]['point'],
        self.status_cache[1]['attempt']],
        'sequencia atual',
        self.status_cache[1]['best_sequence'],
        self.status_cache[1]['worst_sequence'])
        return self._status
        
    def _check_sequence(self):
        '''
        Change the longest streak of every throw
        '''
        if self._status['current_sequence_point'] > self._status['best_sequence']:
            self._status['best_sequence'] = self._status['current_sequence_point']
        if self._status['current_sequence_errors'] > self._status['worst_sequence']:
            self._status['worst_sequence'] = self._status['current_sequence_errors']

    def _update_status_cache(self):
        '''
        move attr:`status` for the last position and append new current attr:`status` 
        '''
        self.status_cache.append(self._status.copy())
        self.status_cache.pop(0)

    def _update_last_shots(self, is_point:bool = False):
        '''
        is_point: True if point is incremented
        is_rollback: True if 
        return: list
        0: for non played
        1: for splash
        2: for wrong
        '''
        if is_point:
            self._status['last_shots'].pop(0)
            self._status['last_shots'].append(1)
        if not is_point:
            self._status['last_shots'].pop(0)
            self._status['last_shots'].append(2)

    def reset_drill(self):
        self._status['point'] = 0
        self._status['attempt'] = 0
        self._status['accuracy'] = .0
        self._status['best_sequence'] = 0
        self._status['current_sequence_point']= 0
        self._status['current_sequence_errors']= 0
        self._status['worst_sequence'] = 0
        self._status['last_shots'] = [0,0,0,0,0,0,0,0,0,0,0]
        self.status_cache = [self._status.copy()]*2
        print("Reinicando cache", ['last',
            self.status_cache[0]['point'],
            self.status_cache[0]['attempt'],
            'sequencia anterior',
            self.status_cache[1]['best_sequence'],
            self.status_cache[1]['worst_sequence'],
            'current',
            self.status_cache[1]['point'],
            self.status_cache[1]['attempt']],
            'sequencia atual',
            self.status_cache[1]['best_sequence'],
            self.status_cache[1]['worst_sequence'])

