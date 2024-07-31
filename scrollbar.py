import customtkinter

app = customtkinter.CTk()
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

textbox = customtkinter.CTkTextbox(app, activate_scrollbars=False)
textbox.grid(row=0,column=0,sticky="nsew")

textbox_scroll =customtkinter.CTkScrollbar(app, command=textbox.yview)
textbox_scroll.grid(row=0,column=1,sticky="ns"
                )

textbox.configure(yscrollcommand=textbox_scroll.set)
app.mainloop()
