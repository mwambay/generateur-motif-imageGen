
import os
import sys
chemin_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(chemin_parent)
from PIL import Image, ImageDraw, ImageFont
import json
import random

class Image_objet:
    def __init__(self, width, height, background_color) -> None:
        self.width = width
        self.height = height
        self.background_color = background_color
    
    def creat_image(self):
        return Image.new("RGB", (self.width, self.height), self.background_color)

    def draw_objet(self, image):
        return ImageDraw.Draw(image)
    
    # Methode ouvrant les fichiers 
    def open_file(self, name, type_file):
            """
            Cette fonction prend deux parametres : le nom et le type du fichier et procede a l'ouverture du fichier
            Args:
                name (str) premier parametre
                type_file (str) second parametre
                
            Return:
                (str or dict or list...) 
            """
            if type_file == 'txt': # Verifie si le fichier est du type txt
                with open(f"data\{name}.{type_file}", encoding='utf-8') as file:
                    data = file.readlines()
                    file.close()
                return data
            else:                   # Sinon il suppose que c'est un Json
             with open(f"polices\{name}.{type_file}", encoding='utf-8') as file:
                data = json.load(file)
                file.close()
                return data
               
    
    def load_police(self, police_def = None):

        if police_def != None:
            return rf"polices\{police_def}.ttf"
        
        polices = self.open_file('polices', 'json')
        police = f"polices\{polices[random.randint(0, len(polices)-1)]}"
        print(police)
        return police
                
    def define_police(self, taille_police, default_police = False, police_def = None):
        if default_police:
            return ImageFont.load_default(size=taille_police)
        if police_def != None:
            try:
                return ImageFont.truetype(self.load_police(police_def), taille_police)
            except:
                return ImageFont.truetype(self.load_police(None), taille_police)



        return ImageFont.truetype(self.load_police(None), taille_police)

