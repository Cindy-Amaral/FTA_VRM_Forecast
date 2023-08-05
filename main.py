import tkinter as tk
import customtkinter
from settings import Settings
from data import Data
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import numpy as np

class Demo1:
    def __init__(self, master):
        #settings
        self.settings = Settings()
        customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.master = master
        self.master.geometry(f"{self.settings.width}x{self.settings.height}")
        #self.master.configure(bg=self.settings.main_color)
        self.master.title('App Form')

        # grid layout 1x2
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        #main body frame
        self.frame = customtkinter.CTkFrame(self.master)
        self.frame.grid(row=0, column=1, padx=20, pady=20)
        self.frame.grid_rowconfigure(4, weight=1)
        #self.frame.configure(bg_color=self.settings.main_color)

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self.master,width=400)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew", columnspan=1)
        self.navigation_frame.grid_rowconfigure(7, weight=1)
        #self.navigation_frame.configure(bg_color=self.settings.secondary_color)
        self.navigation_frame.grid_propagate(False)

        #navigation label
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, 
                                                             text="Vehicle Revenue\nMiles Report",
                                                             compound="left", 
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
        #agency list
        self.ex = Data()
        self.df = self.ex.get_data()
        self.agencies = self.ex.agency_list(self.df)


        #agency option menu
        self.agency_label = customtkinter.CTkLabel(self.navigation_frame, 
                                                             text="Select Agency:",
                                                             compound="left", 
                                                             font=customtkinter.CTkFont(size=9))
        self.agency_label.grid(row=1, column=0, padx=10, pady=0, sticky='w')

        self.optionmenu_var = customtkinter.StringVar(value=self.agencies[0])
        self.optionmenu_var.trace("w", self.update_mode_options)
        self.optionmenu_var.trace("w", self.plot_graph)
        self.optionmenu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                      values=self.agencies,
                                                      command=self.optionmenu_callback,
                                                      variable=self.optionmenu_var,
                                                      width=375)
        self.optionmenu.grid(row=2, column=0, padx=10, pady=0)



        #mode option menu
        self.mode_label = customtkinter.CTkLabel(self.navigation_frame, 
                                                             text="Select Mode:",
                                                             compound="left", 
                                                             font=customtkinter.CTkFont(size=9))
        self.mode_label.grid(row=3, column=0, padx=10, pady=0, sticky='w')

        self.mode_optionmenu_var = customtkinter.StringVar()
        self.mode_optionmenu_var.trace("w", self.plot_graph)
        self.mode_optionmenu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                      values=[],
                                                      command=self.mode_optionmenu_callback,
                                                      variable=self.mode_optionmenu_var,
                                                      width=175)
        self.mode_optionmenu.grid(row=4, column=0, padx=10, pady=0, sticky='w')


        #title label
        self.title_frame = customtkinter.CTkFrame(self.master)
        self.title_frame.grid(row=0, column=1, sticky="n", columnspan=4, pady=10)
        self.title_frame.grid_rowconfigure(8, weight=1)
        text_title='Vehicle Revenue Miles to May 2023\n12 Month Forecast\nAgency: N/A, Mode: N/A'
        self.title_label = customtkinter.CTkLabel(self.title_frame, 
                                                             text=text_title,
                                                             compound="left", 
                                                             font=customtkinter.CTkFont(size=20))
        self.title_label.grid(row=0, column=0, columnspan=4, pady=10, padx=20)


        #update modes and graph
        self.update_mode_options()



        #input field
        self.entry_label = customtkinter.CTkLabel(self.navigation_frame, 
                                                             text="Email:",
                                                             compound="left", 
                                                             font=customtkinter.CTkFont(size=9))
        self.entry_label.grid(row=5, column=0, padx=10, pady=0, sticky='w')
        
        
        self.entry = customtkinter.CTkEntry(master=self.navigation_frame,
                               width=350,
                               height=35,
                               corner_radius=10)


        text = self.entry.get()
        self.entry.grid(row=6, column=0, padx=10, sticky='w')

        
        #button
        self.button1 = customtkinter.CTkButton(self.navigation_frame, 
                                               text='Submit', 
                                               command=self.new_window, 
                                               fg_color=self.settings.button_color, 
                                               text_color=self.settings.text_color, 
                                               hover_color=self.settings.secondary_color)
        self.button1.grid(row=7, column=0, pady=20)

        

    def plot_graph(self, *args):
        # Assuming the initial values are selected from the option menus
        selected_value1 = self.optionmenu_var.get()
        selected_value2 = self.mode_optionmenu_var.get()

        # Assuming the self.ex.forecast method returns a valid Figure object
        plot_fig = self.ex.forecast(self.df, selected_value1, selected_value2)

        # Create a canvas to display the graph in tkinter
        canvas = FigureCanvasTkAgg(plot_fig, master=self.frame)
        canvas.draw()

        # Place the canvas in the tkinter frame
        canvas.get_tk_widget().grid(row=2, column=2, padx=10, pady=10)

        # Update the label text with the currently selected agency and mode
        selected_agency = self.optionmenu_var.get()
        selected_mode = self.mode_optionmenu_var.get()
        label_text = f'Vehicle Revenue Miles to May 2023\n12 Month Forecast\nAgency: {selected_agency}, Mode: {selected_mode}'
        self.title_label.configure(text=label_text)

    def update_graph(self):
        # Clear the previous graph from the frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Plot the updated graph
        self.plot_graph()



    def update_mode_options(self, *args):
        selected_agency = self.optionmenu_var.get()
        self.modes = self.ex.mode_list(self.df, selected_agency)
        if self.modes:
            # Update the mode_optionmenu options
            self.mode_optionmenu.configure(values=self.modes)
            self.mode_optionmenu_var.set(self.modes[0])  # Reset the mode_optionmenu_var to the first mode
        # Update the graph after mode options have been updated
        self.update_graph()
       






    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)

    def optionmenu_callback(self, choice):
            print("agencymenu dropdown clicked:", choice)
    
    def mode_optionmenu_callback(self, choice):
            print("modemenu dropdown clicked:", choice)

                    

class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()
    def close_windows(self):
        self.master.destroy()

def main(): 
    root = customtkinter.CTk()
    app = Demo1(root)
    root.mainloop()

if __name__ == '__main__':
    main()




# class AutoReport:
#     def __init__(self):
#         pass
    
#     def create_report(self):
#         pass

    
#     def send_report(self):
#         pass
   