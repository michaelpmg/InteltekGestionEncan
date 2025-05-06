'''
    Inteltek Gestion [IG]
    API pour le developpement rapide et simple de CMS
    Auteur: Michael Perreault
'''
import customtkinter
import pywinstyles
import os
from PIL import Image
from CTkToolTip import *

PRIMARY_ORANGE = "#FFA000"
SECONDARY_ORANGE = "#F57C00"
PRIMARY_BLUE = "#1565C0"
SECONDARY_BLUE = "#1E88E5"

SETTINGS_IMG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs", "settings.png")

#------------------------------------------ Inteltek Gestion API -----------------------------------
# --- IG Base Widget ---
''' IG Widgets are simply CTk frames '''
class IG_Widget(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

# --- IG Button ---
''' IG Buttons are simply CTk buttons '''
class IG_Button(customtkinter.CTkButton):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

# --- IG Label ----
''' IG Labels are simply CTk labels '''
class IG_Label(customtkinter.CTkLabel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

# --- IG Text Input ---
''' IG Text Input are simply CTk entry '''
class IG_TextInput(customtkinter.CTkEntry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(border_color=PRIMARY_ORANGE)

# --- IG Modal ---
''' IG Modals are simply CTk top levels '''
class IG_Modal(customtkinter.CTkToplevel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

class IG_Popup(IG_Modal):
    def __init__(self, app, msg):
        super().__init__(app)

        self.overrideredirect(True)
        self.configure(fg_color="#8BC34A")
        self.configure(corner_radius=6)
        self.grid_rowconfigure(0,weight=1);
        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(1, weight=1)
        
        pywinstyles.set_opacity(self, value=0.65)
        
        app_width = app.winfo_width()
        app_height = app.winfo_height()
        app_pos_x = app.winfo_x()
        app_pos_y = app.winfo_y()

        label = customtkinter.CTkLabel(self, text=msg, text_color="black")
        label.grid(row=0,column=0,padx=0,pady=0,sticky="nsew")

        px = 250
        py = 35

        popup_pos_x = int(app_pos_x + (app_width/2) - (px/2))
        popup_pos_y = int(app_pos_y + (app_height/2) - (py/2))
        
        geom_str = f'{px}x{py}+{popup_pos_x}+{popup_pos_y}'
        print(geom_str)
        self.geometry(geom_str)
        self.after(2500, lambda: self.destroy())

# --- IG Frame --- #
class IG_Frame(customtkinter.CTkFrame):
    def __init__(self, parent, title):
        super().__init__(parent)

        ''' intern ui setup '''
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # title
        self.grid_rowconfigure(1, weight=10) # content
        self.configure(fg_color="transparent", corner_radius=10)

        ''' label over the frame '''
        self.title = IG_Label(self, text=title ,font=("Arial Nova Light", 20), fg_color="transparent", height=50)
        self.title.grid(row=0, column=0, padx=0, pady=0, sticky="ew")

class IG_ModelContentFrame(IG_Widget):
    def __init__(self,parent,model):
        super().__init__(parent)
        self.configure(fg_color="white", border_color="lightgrey", border_width=2)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.content_ = IG_Widget(self)
        self.content_.grid(row=0,column=0, padx=50,pady=20,sticky="nsew")
        self.content_.configure(fg_color="transparent")
        self.content_.grid_columnconfigure(0, weight=1)
        self.content_.grid_columnconfigure(1, weight=4)
        
        self.model_ = model
        count = 0
        for key, value in self.model_.items():
            label = IG_Label(self.content_, text=key ,font=("Arial Nova Light", 14), fg_color="transparent", corner_radius=6)
            label.grid(row=count, column=0, padx=5, pady=5, sticky="ew")

            edit_input = IG_TextInput(self.content_, placeholder_text=value)
            edit_input.grid(row=count, column=1, padx=5, pady=5, sticky="ew")
            count = count+1

class IG_ModelView(IG_Frame):
    def __init__(self, parent, model_name, model):
        super().__init__(parent, model_name)

        self.content_frame_ = IG_ModelContentFrame(self, model)
        self.content_frame_.grid(row=1, padx=10, pady=(0,10), sticky="nsew")

        self.grid_rowconfigure(2, weight=1)
        save_button = IG_Button(
            self,
            text="Sauvegarder",
            command=lambda: print("Sauvegarder clicked!"),
            fg_color=PRIMARY_ORANGE,
            hover_color=SECONDARY_ORANGE,
            text_color="black",
            corner_radius=6
        )
        save_button.grid(row=2, column=0)
            
class IG_ModelListContentFrame(IG_Widget):
    def __init__(self, parent, model_list):
        super().__init__(parent)
        self.configure(fg_color="white", border_color="lightgrey", border_width=2, bg_color="transparent")
        self.grid_columnconfigure(0, weight=1)

        # header
        self.grid_rowconfigure(0, weight=1)
        # list
        self.grid_rowconfigure(1, weight=10)
        
        self.model_list_ = model_list

        # setup header
        
        self.header_ = IG_Widget(self)
        self.header_.configure(border_color="red", border_width=3, height=50, bg_color="transparent", fg_color="transparent", corner_radius=6)
        self.header_.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")

        # setup list
'''
        self.list_ = IG_Widget(self)
        self.list_.configure(border_color="blue", border_width=1, height=50,bg_color="transparent", fg_color="transparent", corner_radius=6)
        self.list_.grid(row=1,column=0, padx=2, pady=0, sticky="nsew")
'''
        
class IG_ModelListView(IG_Frame):
    def __init__(self, parent, model_name, model_list):
        super().__init__(parent, model_name)

        self.content_frame_ = IG_ModelListContentFrame(self, model_list)
        self.content_frame_.grid(row=1, padx=10, pady=2, sticky="nsew")


# -- IG Navigation --- #
class IG_Navigation(IG_Widget):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(corner_radius=0)
        self.parent_ = parent
        self.n_buttons_ = 0
        
        ''' internal ui setup '''
        self.grid_columnconfigure(0, weight=1) # makes the buttons take all available width
        self.configure(fg_color="white", border_width=2, border_color="gray",corner_radius=1) # color, borders

    def add_navigation(self, nav_name, img_path):
        ''' btn logo '''
        button_image = customtkinter.CTkImage(Image.open(img_path), size=(20, 20))
  
        new_button = customtkinter.CTkButton(
            self,
            text=nav_name,
            image=button_image,
            compound = "top",
            command=lambda: self.parent_.listen_navigation(nav_name),
            fg_color="transparent",
            hover_color=PRIMARY_ORANGE,
            text_color="black",
            corner_radius=0
        )

        ''' button ui placement and padding '''
        pdy = 5 if self.n_buttons_ == 0 else 10
        new_button.grid(row=self.n_buttons_, column=0, padx=5, pady=(pdy, 5), sticky="ew")
        
        self.n_buttons_ = self.n_buttons_ + 1

class IG_App(customtkinter.CTk):
    def __init__(self, geometry="800x600", title="IG APP"):
        super().__init__()
        
        self.title(title)
        self.geometry(geometry)

        # Navigation and Information panels UI configuration.
        self.grid_columnconfigure(0, weight=0)  # navigation panel 
        self.grid_columnconfigure(1, weight=1)  # information panel
        self.grid_rowconfigure(0, weight=1)     # 1 row full height

        self.navigation_frame_ = IG_Navigation(self)
        self.navigation_frame_.grid(row=0, column=0, sticky="nsew")
        self.current_frame_ = None
        self.set_current_frame(IG_Widget(self))

        self.settings_ = {
            "Courriel" : "exemple@gmail.com",
            "Logo" : "/chemin/vers/logo.png"
        }
        
        self.navigation_frame_.add_navigation("Settings", SETTINGS_IMG_PATH)

        pywinstyles.change_header_color(self, color=PRIMARY_BLUE)
        
    def set_current_frame(self, frame):
        if self.current_frame_ is not None:
            self.current_frame_.destroy()
        self.current_frame_ = frame
        self.current_frame_.grid(row=0, column=1, sticky="nsew")

    def listen_navigation(self, nav_name):
        self.set_current_frame(self.get_navigation_widget(nav_name))

    def get_navigation_widget(self, nav_name):
        return IG_ModelView(self, nav_name, self.settings_) if nav_name == "Settings" else None

    def show_popup(self, time_ms, msg):
        popup = IG_Popup(self, msg)

    def start(self):
        self.mainloop()
