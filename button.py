import pygame as P

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.buttonClicked = False
        self.selected = False

    def draw(self, turretPanelArea):
        buttonResponse = False
        #Get mouse position
        mousePosition = P.mouse.get_pos()

        #Check mouseover and clicked conditions
        if self.rect.collidepoint(mousePosition):
            if P.mouse.get_pressed()[0] == 1 and self.buttonClicked == False:
                buttonResponse = True
                self.buttonClicked = True
                self.selected = True

        if P.mouse.get_pressed()[0] == 0:
            self.buttonClicked = False
        #Draw button on screen
        turretPanelArea.blit(self.image, self.rect)

        return buttonResponse