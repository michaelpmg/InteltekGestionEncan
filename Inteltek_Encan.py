import customtkinter as ctk
import json
import os
import CTkListbox as ctklb
from tkinter import messagebox

# load clients from a file
# This is a simple JSON file to store client data
CLIENTS_FILE = "clients.json"
def load_clients():
    if os.path.exists(CLIENTS_FILE):
        with open(CLIENTS_FILE, "r") as file:
            return json.load(file)
    return []

def save_clients_to_file(clients):
    with open(CLIENTS_FILE, "w") as file:
        json.dump(clients, file)

# Load settings from a file
# This is a simple JSON file to store settings data
SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)

settings = load_settings()

# Initialize the app
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AuctionApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Auction Manager")
        self.geometry("800x600")

        # Navigation bar
        self.navbar = ctk.CTkFrame(self, width=200, corner_radius=2, border_width=2, border_color="lightgrey", fg_color="white")

        self.navbar.pack(side="left", fill="y")

        button_style = {
            "fg_color": "white",
            "hover_color": "orange",
            "corner_radius": 0,
            "border_width": 0,
            "text_color": "black"
        }

        button_size = 75 # Define a square size for the buttons

        self.nav_clients = ctk.CTkButton(self.navbar, text="Clients", command=self.show_clients, **button_style, width=button_size, height=button_size)
        self.nav_clients.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        self.nav_auctions = ctk.CTkButton(self.navbar, text="Auctions", command=self.show_auctions, **button_style, width=button_size, height=button_size)
        self.nav_auctions.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        self.nav_settings = ctk.CTkButton(self.navbar, text="Settings", command=self.show_settings, **button_style, width=button_size, height=button_size)
        self.nav_settings.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

        # Configure grid weights for navbar
        self.navbar.grid_rowconfigure((0, 1, 2), weight=0)  # Set row weights to 0 to avoid extra vertical space
        self.navbar.grid_columnconfigure(0, weight=1)

        # Main content area
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Load clients
        self.clients = load_clients()

        # Initialize views
        self.show_clients()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_clients(self):
        self.clear_content()

        # Client list
        self.client_list = ctklb.CTkListbox(self.content_frame)
        self.client_list.pack(fill="both", expand=True, padx=10, pady=10)

        # Button frame to hold buttons in a horizontal line
        button_frame = ctk.CTkFrame(self.content_frame)
        button_frame.pack(pady=10)

        # View Client Details button
        self.view_client_button = ctk.CTkButton(button_frame, text="View Details", command=self.show_client_details)
        self.view_client_button.pack(side="left", padx=5)

        # Delete Client button
        self.delete_client_button = ctk.CTkButton(button_frame, text="Delete Client", command=self.delete_client)
        self.delete_client_button.pack(side="left", padx=5)

        # Add client button
        self.add_client_button = ctk.CTkButton(button_frame, text="Add Client", command=self.add_client)
        self.add_client_button.pack(side="left", padx=5)

        # Populate client listbox
        for client in self.clients:
            self.client_list.insert("end", client)

    def delete_client(self):
        selected_index = self.client_list.curselection()
        if selected_index is not None:
            client_name = self.client_list.get(selected_index)
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {client_name}?")
            if confirm:
                self.clients.pop(selected_index)
                save_clients_to_file(self.clients)
                self.show_clients()
        else:
            messagebox.showerror("Error", "No client selected!")

    def show_client_details(self):
        selected_index = self.client_list.curselection()
        if selected_index is not None:
            client_name = self.client_list.get(selected_index)

            client_details_window = ctk.CTkToplevel(self)
            client_details_window.title("Client Details")
            client_details_window.geometry("300x150")

            client_name_label = ctk.CTkLabel(client_details_window, text=f"Client Name: {client_name}")
            client_name_label.pack(pady=10)

            close_button = ctk.CTkButton(client_details_window, text="Close", command=client_details_window.destroy)
            close_button.pack(pady=10)

    def add_client(self):
        def save_client():
            client_name = client_name_entry.get()
            if client_name:
                self.clients.append(client_name)
                save_clients_to_file(self.clients)
                add_client_window.destroy()
                self.show_clients()
            else:
                messagebox.showerror("Error", "Client name cannot be empty!")

        add_client_window = ctk.CTkToplevel(self)
        add_client_window.title("Add Client")
        add_client_window.geometry("300x150")

        client_name_label = ctk.CTkLabel(add_client_window, text="Client Name:")
        client_name_label.pack(pady=10)

        client_name_entry = ctk.CTkEntry(add_client_window)
        client_name_entry.pack(pady=10)

        save_button = ctk.CTkButton(add_client_window, text="Save", command=save_client)
        save_button.pack(pady=10)

    def show_auctions(self):
        self.clear_content()
        label = ctk.CTkLabel(self.content_frame, text="Auctions View")
        label.pack(pady=20)

    def show_settings(self):
        self.clear_content()

        email_label = ctk.CTkLabel(self.content_frame, text="User Email:")
        email_label.pack(pady=10)

        email_entry = ctk.CTkEntry(self.content_frame, placeholder_text=settings.get("user_email", ""))
        email_entry.pack(pady=10)

        logo_label = ctk.CTkLabel(self.content_frame, text="Path to logo.png:")
        logo_label.pack(pady=10)

        logo_entry = ctk.CTkEntry(self.content_frame, placeholder_text=settings.get("logo_path", ""))
        logo_entry.pack(pady=10)

        def save_settings_callback():
            settings["user_email"] = email_entry.get()
            settings["logo_path"] = logo_entry.get()
            save_settings(settings)
            messagebox.showinfo("Settings", "Settings saved!")

        save_button = ctk.CTkButton(self.content_frame, text="Save Settings", command=save_settings_callback)
        save_button.pack(pady=10)

# Run the app
if __name__ == "__main__":
    app = AuctionApp()
    app.mainloop()