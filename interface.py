import os
import sys
chemin_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(chemin_parent)
from PIL import Image, ImageTk
import customtkinter
import json
import os
from src.generator import Generator

from src.image_script import Image_objet
from src.hand import Hand

def interpreter():
    def format_(struct : list) -> list:
        temp = []
        for index, text in enumerate(struct):
            if text.strip('\n') == 'end':
                break
            if len(text) > 0:
                temp.append(text) 
        return temp
    
    texte = prompt.get(1.0, customtkinter.END)
    instructions = prompt_2.get(1.0, customtkinter.END)
    instructions = instructions.split('\n')
    texte = texte.split("\n")

    texte = format_(texte)
    instructions = format_(instructions)
    print(texte)
    instruct = {}
    hand = Hand(int(largeur.get()), int(longeur.get()))
    
    for element in range(len(texte)):
        instru = instructions[element].split()
        instruct['position'+ str(element)] = hand.position_calculation(instru[0], int(instru[1]), int(instru[2]))
        instruct['element'+ str(element)] = texte[element]
        
    generator = Generator(int(largeur.get()), int(longeur.get()))
    data = generator.pipeline("Say Hello to MotifGen !", instructions=instruct)
    dps_image()

class TextBoxAjustable(customtkinter.CTkTextbox):
    def __init__(self, master: any, width = 200, height = 200, lenght_ajustable = 30,  **kwargs):
        self.master = master
        self.taille_ajustable = lenght_ajustable
        self.width = width
        self.height = height
        self.prompt = None
        self.memory = self.taille_ajustable

        
    def bind_(self):
        self.prompt.bind('<Return>', self.resize_w)
        self.prompt.bind("<FocusIn>", self.on_get)
        self.prompt.bind("<FocusOut>", self.out_get)

    def on_get(self, event):
        self.prompt.configure(border_color='blue', border_width = 2)
        self.prompt.configure(height = self.memory )

        
    def out_get(self, event):
        self.prompt.configure(border_color='#969696', border_width = 1, height = self.taille_ajustable
                         )
        self.prompt.configure(height = self.height )

    def resize_w(self, event):
        print(self.taille_ajustable)
        
        if self.taille_ajustable < 150:
            self.taille_ajustable += 10
        self.prompt.configure(height = self.taille_ajustable )
        self.memory = self.taille_ajustable


    
    def creat_objet(self):
        return customtkinter.CTkTextbox(self.master, width=self.width, height= self.height, corner_radius=0, fg_color='transparent', border_width=1, wrap=customtkinter.WORD, font=("courier", 15, 'italic'))
    def grid(self, row, column, pady = 0, padx = 0):
        self.prompt = self.creat_objet()
        self.bind_()
        self.prompt.grid(row=row, column=column, padx = padx, pady = pady)
        
    def pack(self, pady = 0, padx = 0):
        self.prompt = self.creat_objet()
        self.bind_()
        self.prompt.pack(padx = padx, pady = pady)
        
    def get(self,debut, fin):
       return self.prompt.get(debut, fin)

dossier = "data"
liste_de_images = os.listdir(dossier)
def select_model():
 
        
        def load_polices_list():
            polices = Image_objet.open_file(None, 'polices', 'json')
            
            for indice, police in enumerate(polices):
                polices[indice] = police.replace('.ttf', '')
            return polices
        
        label_police = customtkinter.CTkLabel(frame_generale, text='taille police')
        label_police.grid(row = 0, column=0, padx = 20)
        taille_police = customtkinter.CTkSlider(frame_generale)
        taille_police.grid(row = 0, column=1)
        # definir la police
        label_police = customtkinter.CTkLabel(frame_generale, text='police')
        label_police.grid(row = 0, column=2, padx = 20)
        _police = customtkinter.CTkOptionMenu(frame_generale, values=load_polices_list())
        _police.grid(row = 0, column=3)
        buton = customtkinter.CTkButton(frame_generale, text='submit')
        buton.grid(row=1, column=1)



def display_images():
    ligne = 4
    colone = 0
    for image in liste_de_images:
        if 'jpeg' in image or 'png' in image or 'jpg' in image:
            image = Image.open(rf'data\{image}')
            image.thumbnail((260, 260), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            label_image = customtkinter.CTkLabel(frame, image=photo,  text="", text_color='blue', font=("arial", 9, 'italic'))
            label_image.grid(row=ligne, column=colone, padx = 5)
            colone += 1
            if colone == 3:
                colone = 0
                ligne += 1
            
indice = 0


window = customtkinter.CTk()
window.geometry("1020x680")
window.title('motifGen!')

# canvas = customtkinter.CTkCanvas(window, bd=0, highlightthickness=0)
# canvas.configure(background=window.cget("background") )


#f rame_scrollable = customtkinter.CTkFrame(canvas, fg_color='transparent')


frame_generale = customtkinter.CTkFrame(window, fg_color='transparent')
frame_generale.pack(expand=True)


label_text_box = customtkinter.CTkLabel(frame_generale, text='Text : ')
label_text_box.grid(row = 1, column = 0, pady = 20, padx=10)

prompt = TextBoxAjustable(frame_generale, width=500, height=100, lenght_ajustable=100)
prompt.grid(row=1, column=1, pady=20, padx = 30)

label_text_box = customtkinter.CTkLabel(frame_generale, text='Prompt : ')
label_text_box.grid(row = 2, column = 0, pady = 20, padx=10)

prompt_2 = TextBoxAjustable(frame_generale, width=500, height=100, lenght_ajustable=100)
prompt_2.grid(row=2, column=1)
def dps_image():
    image = Image.open(rf'images\image.png')
    image.thumbnail((260, 260), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    display_image.configure(image = photo)
display_image = customtkinter.CTkLabel(frame_generale, text='', image=None)
display_image.grid(row=1, column=3)

submit = customtkinter.CTkButton(frame_generale, text='Submit', command=interpreter)
submit.grid(row=4, column=1)

messages_assistant = ['vous disposez de deux champs pour communiquer avec le model',
                      'le premier vous permet de saisir les differents textes qui seront affiches',
                      'et le second vous permet de saisir le prompt qui guidera le model dans sa generation']

def insert_text_in_champ():
    global indice
    if indice > 2:
        indice = 0
    assistant_champ.delete(1.0, customtkinter.END)
    assistant_champ.insert(customtkinter.END, messages_assistant[indice])
    indice += 1
    window.after(7000, insert_text_in_champ)

frame_dim = customtkinter.CTkFrame(frame_generale, fg_color='transparent')
frame_dim.grid(row = 0, column = 1, pady = 20, padx=10)

largeur_label = customtkinter.CTkLabel(frame_dim, text='width : ')
largeur_label.grid(row = 0, column = 0, pady = 20)

largeur = customtkinter.CTkEntry(frame_dim)
largeur.grid(row=0, column=1, padx=40)

longeur_label = customtkinter.CTkLabel(frame_dim, text='height : ')
longeur_label.grid(row = 0, column = 2,padx=10)

longeur = customtkinter.CTkEntry(frame_dim)
longeur.grid(row=0, column=3)

largeur.insert(customtkinter.END, '500')
longeur.insert(customtkinter.END, '500')

assistant_champ = customtkinter.CTkTextbox(frame_generale, border_width=0, fg_color='#6FEDCA', height=100, text_color='black', wrap=customtkinter.WORD)
assistant_champ.grid(row=3, column=1, pady=20)

insert_text_in_champ()


# #display_images()
# scroll = customtkinter.CTkScrollbar(window, orientation='vertical', command=canvas.yview)
# scroll.pack(side = 'right', fill='y')


# scroll_x = customtkinter.CTkScrollbar(window, orientation='horizontal', command=canvas.yview)
# scroll_x.pack(side = 'top', fill='x')

# canvas.configure(yscrollcommand=scroll.set)
# canvas.pack(expand=True, fill='both')


# canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 *(event.delta / 120)), "units"))
# frame_scrollable.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
# canvas.create_window((0,0), window=frame_scrollable,anchor='nw' )

window.mainloop()