import tkinter as tk
import pnglib as png
import minecraftskin as skin

class application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.geometry("206x110")
        self.parent.title("Skin to Icon")
        self.parent.resizable(False, False)
        self.parent.iconbitmap("output.ico")
        
        self.select = tk.Button(self.parent, text="Select Skin", width=28, height=2, command=self.select_skin)
        self.select.place(x=0, y=0)
        
        self.convert = tk.Button(self.parent, text="Convert to Icon", width=28, height=2, command=self.save_as_icon)
        self.convert.place(x=0, y=40)
        
        self.filetypes = ["png", "ico"]
        self.variable = tk.StringVar(self.parent)
        self.variable.set(self.filetypes[0])
        self.filetype_menu = tk.OptionMenu(self.parent, self.variable, *self.filetypes)
        self.filetype_menu.config(width=23)
        self.filetype_menu.place(x=0, y=80)
        
    def select_skin(self):
        img_path = tk.filedialog.askopenfilename()
        self.path = "/".join(img_path.split("/")[:-1])
        
        self.image = png.png_to_rgb(img_path)
    
    def save_as_icon(self):
        face   = skin.get_face(self.image)
        shadow = skin.get_face_mask(self.image)
        mask   = skin.get_face_mask(self.image)
        face   = png.scale_rgb(face, 59, 59)
        shadow = png.scale_rgb(shadow, 59, 59)
        mask   = png.scale_rgb(mask, 64, 64)
        face   = png.clamp_rgb_size(face, 512, 512)
        shadow = png.clamp_rgb_size(shadow, 512, 512)
        mask   = png.clamp_rgb_size(mask, 512, 512)
        
        shadow = png.rgb_to_ba(shadow, 204)
        shadow = png.blur_rgb(shadow, 10)
        
        combined_image = png.combine_rgb([face, shadow, mask])
        png.rgb_to_png(combined_image, self.path, "output", self.variable.get())
        
        tk.messagebox.showinfo(title="Info", message="Success!")

        
        
        
        

if __name__ == "__main__":
    root = tk.Tk()
    application(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
    