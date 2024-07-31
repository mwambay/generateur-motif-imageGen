
class Hand():
    def __init__(self, width, height, center_x = 100, center_y = 100) -> None:
        self.width = width;
        self.height = height;
        if center_x == None and center_y == None:
            center_x, center_y = (width // 2, height // 2)
        self.center_x = width // 2
        self.center_y = height // 2 
        self.left_center_y = (0, center_y)
        self.right_center_y = (width * 2, center_y)
        self.top_center_x = (center_x, 0)
        self.low_center_x = (center_x, height)
        self.wedge_1 = (0, 0)
        self.wedge_12 = (width * 2, height*2)
        self.wedge_2 = (0, height)
        self.wedge_22 = (width , 0)
        self.memoire = []

        self.strategic_position = {
            "head_left" : {"x" : (center_x / 2) - (center_x / 2) / 2,
                           "y" : (center_y/ 2) - (center_y / 2) / 2 },
            
            "head_right" : {"x" : center_x + (center_x / 2),
                           "y" : (center_y/ 2) - (center_y / 2) / 2 },
            
            "bottom_left" : {"x" : (center_x / 2) - (center_x / 2) / 2,
                "y" : center_y + (center_y / 2)},
            
            "bottom_right" : {"x" : center_x  + (center_x / 2),
                "y" : center_y + (center_y / 2)}
        }
    
    # Methode permettant de quadriller l'image pour permettre la localisation de points strategiques
    def quadriller_9X9(self, draw_on_image, couleur):
        draw_on_image(self.low_center_x[0], self.low_center_x[1]
                      , couleur,self.top_center_x[0], self.top_center_x[1])
        draw_on_image(self.left_center_y[0], self.left_center_y[1], couleur, self.right_center_y[0], self.right_center_y[1])
        draw_on_image(self.wedge_1[0], self.wedge_1[1], couleur, self.wedge_12[0], self.wedge_12[1])
        draw_on_image(self.wedge_2[0], self.wedge_2[1], couleur, self.wedge_22[0], self.wedge_22[1])
        
    # methode renvoyant les coordonnees d'une cible a partir d'un mot cle
    def position_calculation(self, position, decal_x = 0, decal_y = 0):
        decallage = 250
        if position == 'center':
            coordonnees = (self.center_x + decal_x, self.center_y + decal_y)
            while coordonnees in self.memoire:
                #print(coordonnees, self.memoire)
                coordonnees = (coordonnees[0], coordonnees[1] + decallage)     
                
            self.memoire.append(coordonnees)
            return coordonnees

        coordonnees = (self.strategic_position[position]['x'] + decal_x,
                self.strategic_position[position]['y'] + decal_y
                )
        while coordonnees in self.memoire:
            #print(coordonnees, self.memoire)
            coordonnees = (coordonnees[0], coordonnees[1] + decallage)     
            
        self.memoire.append(coordonnees)
        return coordonnees
    
    # Afficher le texte sur l'image
    def text_on_image(self, **kwargs):
        if kwargs['oneline']:
            kwargs['draw'].text(kwargs['position'], kwargs['text'][0], fill=kwargs['color'], font=kwargs['font'])
            return None
        position = kwargs['position']
        x, y = (position[0], position[1])

        for sentence in kwargs['text']:
            try:
                kwargs['draw'].text((x, y), sentence, fill=kwargs['color'], font=kwargs['font'])
                y += kwargs['size'] + kwargs['interligne']
            except:
                kwargs['draw'].text((x, y), sentence, fill='black', font=kwargs['font'])
                y += kwargs['size'] + kwargs['interligne']
        if (x,y) not in self.memoire:
            self.memoire.append((x,y))