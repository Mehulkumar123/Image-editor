from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter
class Editor:
    def __init__(self, master):
        self.master = master
        master.title("Image Editor")
        self.image = None
        self.photo = None
        self.canvas = Canvas(master, width=500, height=500)
        self.canvas.pack(side=TOP, padx=10, pady=10)
        self.slider_frame = Frame(master)
        self.slider_frame.pack(side=TOP, padx=10, pady=10)
        self.blur_slider = self.create_slider(self.slider_frame, "Blur", 0, 20, self.blur_image)
        self.sharpen_slider = self.create_slider(self.slider_frame, "Sharpen", 0, 20, self.sharpen_image)
        self.rotate_slider = self.create_slider(self.slider_frame, "Rotate", -180, 180, self.rotate_image)
        self.open_button = self.create_button(master, "Open", self.open_image)
        self.save_button = self.create_button(master, "Save", self.save_image)
    def create_slider(self, parent, label_text, min_value, max_value, command):
        label = Label(parent, text=label_text)
        label.pack(side=LEFT, padx=10, pady=10)
        slider = Scale(parent, from_=min_value, to=max_value, orient=HORIZONTAL, command=command)
        slider.pack(side=LEFT, padx=10, pady=10)
        slider.set(0)
        return slider
    def create_button(self, parent, button_text, command):
        button = Button(parent, text=button_text, command=command)
        button.pack(side=LEFT, padx=10, pady=10)
        return button
    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.image = Image.open(file_path)
                self.image = self.image.resize((500, 500))
                self.photo = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(0, 0, anchor=NW, image=self.photo)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while opening the image: {e}")
    def save_image(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.image.save(file_path)
                messagebox.showinfo("Image saved", f"Image saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the image: {e}")
    def apply_filters(self):
        blur_value = int(self.blur_slider.get())
        sharpen_value = int(self.sharpen_slider.get())
        rotate_value = int(self.rotate_slider.get())
        if self.image:
            image_copy = self.image.copy()
            if blur_value > 0:
                image_copy = image_copy.filter(ImageFilter.GaussianBlur(radius=blur_value))
            if sharpen_value > 0:
                image_copy = image_copy.filter(ImageFilter.UnsharpMask(radius=sharpen_value, percent=150))
            if rotate_value != 0:
                image_copy = image_copy.rotate(rotate_value)
            self.photo = ImageTk.PhotoImage(image_copy)
            self.canvas.create_image(0, 0, anchor=NW, image=self.photo)
    def blur_image(self, value):
        self.apply_filters()
    def sharpen_image(self, value):
        self.apply_filters()
    def rotate_image(self, value):
        self.apply_filters()
root = Tk()
editor = Editor(root)
root.mainloop()
