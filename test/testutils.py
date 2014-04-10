
import Tkinter
from PIL import Image, ImageTk

        
def SimpleShow(im):
    def button_click_exit_mainloop(event):
        event.widget.quit()
    root = Tkinter.Tk()
    root.bind("<Button>", button_click_exit_mainloop)
    root.geometry('+%d+%d' % (100,100))
    root.geometry('%dx%d' % (im.size[0],im.size[1]))
    tkpi = ImageTk.PhotoImage(im)
    label_image = Tkinter.Label(root, image=tkpi)
    label_image.place(x=0,y=0,width=im.size[0],height=im.size[1])
    root.mainloop()