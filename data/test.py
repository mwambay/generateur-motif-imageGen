from tkinter import*

root = Tk()
canvas = Canvas(root)
canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
scrollbar = Scrollbar(root,command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
scrollble_frame = Frame(canvas)
canvas.create_window((0,0), window=scrollble_frame, anchor='nw')
for i in range(500):
    Label(scrollble_frame, text=f"Label{i}").pack()
j = Label(root, text="ok").pack()
root.mainloop()



def resize(event):
    canvas.configure(scrollregion=canvas.bbox('all'))
    canvas_height = canvas.winfo_height()
    scrollble_frame_height = scrollble_frame.winfo_height()
    if canvas_height > scrollble_frame_height:
        canvas.move(scrollble_frame, 0, (canvas_height-scrollble_frame_height)//2)

canvas.bind('<Configure>', resize)