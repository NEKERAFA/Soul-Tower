# -*- coding: utf-8 -*-

from src.sprites.ConditionalDrop import *

class Ring(ConditionalDrop):
    def collect(self, stage):
        # TODO modifica la condicion
        if stage.player.kill:
            stage.state = OnDialogueState(self.dialogueList[0], stage)
        else:
            stage.state = OnDialogueState(self.dialogueList[0], stage)
        self.kill()
