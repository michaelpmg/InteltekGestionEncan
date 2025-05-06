import InteltekGestionAPI as IG
import os

PRIMARY_ORANGE = "#FFA000"
SECONDARY_ORANGE = "#F57C00"
PRIMARY_BLUE = "#1565C0"
SECONDARY_BLUE = "#1E88E5"

AUCTION_IMG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs", "auction.png")
CLIENT_IMG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs", "client.png")
        
class GEI_App(IG.IG_App):
    def __init__(self):
        super().__init__(
            geometry="800x600",
            title="Gestion Encans Inteltek [GEI]"
        )

        self.navigation_frame_.add_navigation("Encans", AUCTION_IMG_PATH)
        self.navigation_frame_.add_navigation("Clients", CLIENT_IMG_PATH)
        
    def get_navigation_widget(self, nav_name):
        app_view = super().get_navigation_widget(nav_name)
        return app_view if app_view is not None else IG.IG_ModelListView(
            self,
            model_name=nav_name,
            model_list=[
                {"id":"1", "Nom":"Michael"},
                {"id":"2", "Nom":"Marc"}
            ]
        )
        

if __name__=="__main__":
    app = GEI_App()
    app.start()
