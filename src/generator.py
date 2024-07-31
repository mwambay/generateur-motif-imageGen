
import os
import sys
chemin_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(chemin_parent)
from src.image_script import Image_objet
from src.hand import Hand
import random
import json
background_colors = {
    "simple" : [(255, 245,208),(195,255,219), "#FFF2FD", "#D3FFD8", "#D8E0FF", "#FFFFFF"],
    "util" : ["#C594FF", "#FF92FD", "#FFAABF", "#FF79CA", "#77FFF9"  ],
    "objet_black" : ["#996B6C","#7F9947", "#99337C", "#333499", "#111C99", "#000000"]
    
}

class Generator(Image_objet):
    def __init__(self, width, height, background_color = None) -> None:
        self.center_x = width // 2
        self.center_y = height // 2
        background_color = 'white'
        self.instructions = None

        if background_color == None:
            background_color = background_colors["simple"][random.randint(0, len(background_colors["simple"])-1)]
            
        self.background_color = background_color
        super().__init__(width, height, background_color)
        self.image = super().creat_image()
        self.draw = super().draw_objet(self.image)
    
    def save_file(self, name : str, type_file : str, data) -> None:
        try:
            with open(f"data\{name}.{type_file}", 'w', encoding='utf-8') as file:
                if type_file == 'txt':
                    file.write(data)
                else:
                    json.dump(data, file, indent = 4)
                file.close()
        except FileNotFoundError as e:
            print(e)
            
    def draw_ellipse(self, X, Y, rayon, color):
        self.draw.ellipse((X - rayon, Y - rayon, X + rayon, Y + rayon), fill=color)

    def draw_rectangle(self, X, Y, rayon, color):
        self.draw.rectangle((X - rayon, Y - rayon, X + rayon, Y + rayon), fill=color)

    def draw_polygon(self,  X, Y, rayon, color):
        self.draw.polygon((X - rayon, Y - rayon, X + rayon, Y + rayon), fill=color, width=10)

    def draw_shape(self, X, Y, rayon, color):
        self.draw.shape((X - rayon, Y - rayon, X + rayon, Y + rayon), fill=color)

    # dessiner une forme sur l'image 
    def draw_on_image(self, X, Y, color, start = None, end = None, draw_half_X : bool = False, draw_half_Y : bool = False, form = 'line', rayon : int = 120):
        if start == None and end == None:
            start, end = (X, Y)
        draw = {
            "cercle" : self.draw_ellipse,
            "rectangle" : self.draw_rectangle,
            "polygon" : self.draw_polygon,
            #"shape" : self.draw_shape( X, Y, rayon, color),
            "rounded_rectangle" :   self.draw.rounded_rectangle,
            "point" :   self.draw.point,
            #"regular_polygon" :   self.draw.regular_polygon( (X - rayon, Y - rayon, X + rayon, Y + rayon), fill=color,n_sides=5,),
            "arc" :   self.draw.arc,
            "line" :   self.draw.line,
            "chord" :   self.draw.chord
        }
        
        for form_ in draw:
            if form_ == form:
                if form_ not in ('arc', 'line', 'chord'):
                    draw[form]( X, Y, rayon, color)
                    break

                else:
                    if form_ in ('arc', 'chord'):
                        draw[form]((X - rayon, Y - rayon, X + rayon, Y + rayon), start, end, fill=color, width=9)
                    else:
                        draw[form](((X , Y), (start, end)), width=1, fill=color)

                    break

        if draw_half_X:
            self.draw_ellipse(X + rayon, Y, rayon, color=self.background_color)
            #self.draw_ellipse(X + rayon, Y, rayon, color=self.background_color)
        if draw_half_Y:
            self.draw_ellipse(X, Y + rayon, rayon, color=self.background_color)
            #self.draw_ellipse(X + rayon, Y, rayon, color=self.background_color)
             
        
    def define_position_of_text(self): 
        width = self.center_x
        height = self.center_y
        return (width, height)
    
    def define_color_text(self, is_random):
        if is_random:
            return background_colors["objet_black"][random.randint(0, len(background_colors["objet_black"])-1)]
        
    def define_color_form(self, is_random):
        if is_random:
            return background_colors["util"][random.randint(0, len(background_colors["util"])-1)]    
    
    def follow_instruction(self, model, hand, text, couleur, couleur_form, font):
        def load_text():
            try:
                return text_temp[ int(temp[1]) ].split(";")
            except:
                return ["Say hello to ME"]
        position = None
        if model in self.instructions.keys():
            for key, value in self.instructions[model].items():
                if isinstance(value, str):
                    if len(value.split()) > 2 and 'text' not in value:
                        info = value.split()
                        form = info[0]
                        rayon_perimeter =  int(info[1]) 
                        if int(value.split()[-1]) == 2:
                            self.draw_on_image(position[0], position[1], couleur_form, rayon=rayon_perimeter, draw_half_X=True, draw_half_Y=True , form=form)
                        else:
                            self.draw_on_image(position[0], position[1], couleur_form, rayon=rayon_perimeter, draw_half_X=True, draw_half_Y=False, form=form )
                    elif 'text' in value:
                        """
                        en temps normal la variable temp devra contenir
                        la valeur 'text' qui indique que la donnee a inserer est de type text
                        puis la taille, et en derniere position le mot cle define suivi de la police a definir
                        ex : << text 12 define Arial black >>
                        """
                        temp = value.split()
                        size = 12
                        text_temp = super().open_file('texte', 'txt')
                        # si la police ne pas precisee
                        if temp.__len__() <= 3:
                            # si la taille n'est pas precisee, on definit une taille par defaut de 12
                            if temp.__len__() == 2:
                                
                                text = load_text()
                                font = super().define_police(12, default_police=True)
                            else:
                                text = load_text()
                                size = int(temp[2])
                                # si la taille est precisee
                                font = super().define_police(size, default_police=True)
                        
                        else:
                            # si la police est precisee, alors on l'utilise
                            if temp[3] == 'define':
                                df = False
                                text = load_text()

                                size = int(temp[2])
                                # Appel de la methode <<define_police>> definie dans le classe <<image_objet>> implemente dans le fichier image_scipt
                                
                                couleur = temp[-1]
                                police = temp[-2]
                                if police == 'none':
                                    df = True
                                if '_' in police:
                                    police = police.replace('_', " ")

                                font = super().define_police(size, default_police=df, police_def=police)
                            

                                
                        # Creation du text a l'aide de l'objet hand
                        hand.text_on_image(text=text,
                             position=position, size=size, color=couleur, font=font , draw=self.draw, interligne=20, oneline=False)
                    else:
                        info = value.split()
                        form = info[0]
                        rayon_perimeter =  int(info[1])
                        self.draw_on_image(position[0], position[1], couleur_form, rayon=rayon_perimeter, form=form)

        
                else:

                    position = value

    # ecrire un texte sur l'image
    def pipeline(self, text, instructions = False, couleur = None) -> None:
        hand = Hand(self.width, self.height, self.center_x, self.center_y)
        texte = "Say hello to my Model;How are you "
        #self.save_file('texte', 'txt', texte)

        self.instructions = {
            "general" : {"position0": hand.position_calculation('head_left'),
                         "element0" : 'arc 20',
                         "position1": hand.position_calculation('head_left', decal_y=250),
                         "element1" : "text 0 100 define hhw blue",
                         "position2": hand.position_calculation('center', decal_x=30, decal_y=-300),
                         # Le mot cle div indique à la fonction si elle doit diviser la forme
                         "element2" : 'cercle 200 div 1',
                         "position3": hand.position_calculation('head_left', decal_y=250),
                         "element3" : 'text 1 30 define Blancha black',
                         "position4": hand.position_calculation('head_left', decal_y=250),
                         "element4" : 'text 2 30 define Blancha green',
                         
                         }
        }

        if isinstance(instructions, dict):
            print('hello')
            self.instructions['general'] = instructions
            print(self.instructions)
        if couleur == None:
            couleur = self.define_color_text(is_random = True)
        couleur_form = self.define_color_form(is_random=True)    
        
        position = self.define_position_of_text()
        width = position[0]
        height = position[1]
        font = super().define_police(50, default_police=False)

        #self.draw_on_image(hand.position_calculation[0], hand.position_calculation[1], couleur)
        #hand.quadriller_9X9(self.draw_on_image, 'red')

        self.follow_instruction('general',hand, text, couleur, couleur_form, font)

        self.image.save(r"images\image.png")
        return {'police' : font}

if __name__ == '__main__':
    generator = Generator(1020, 1020)
    generator.pipeline("Say Hello to MotifGen !")