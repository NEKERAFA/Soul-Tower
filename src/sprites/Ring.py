# -*- coding: utf-8 -*-

from src.sprites.ConditionalDrop import *
from src.scenes.stage.OnDialogueState import *
from src.scenes.stage.OnCreditsState import *

class Ring(ConditionalDrop):
    def collect(self, stage):
        stage.state = OnCreditsState(stage)
        # Modifica la condicion
        if stage.player.choseAnythingNotShared:
            if stage.player.choiceAdder > 0:
                stage.state = OnDialogueState(self.dialogueList[0], stage)
            else:
                stage.state = OnDialogueState(self.dialogueList[1], stage)
        else:
            stage.state = OnDialogueState(self.dialogueList[2], stage)
        self.kill()
