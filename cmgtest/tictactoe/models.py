from django.db import models
import uuid

class TTTSession(models.Model):
    session = models.CharField(max_length=32, unique=True)
    board = models.CharField(max_length=9)
    updated_on = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    @classmethod
    def new_session(cls):
        while True:
            try:
                session = uuid.uuid4().hex
                
                ttt_session = cls.objects.create(session=session, board='_' * 9)
            except Exception, e:
                print e
                continue
            
            return ttt_session
    
    def validate_against(self, board):
        """ Checks if the given board state is reachable
            from the current board state in 1 move """
        
        # Assumes only valid board characters
        for ch1, ch2 in zip(self.board, board):
            if ch1 != ch2 and ch1 != '_':
                return False
        
        return True
    
    def __unicode__(self):
        return str((self.session, self.board, self.updated_on))
