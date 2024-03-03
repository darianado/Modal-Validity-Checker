import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

import tableau_procedure
from parse import Parser
import modelGraph


DARK_MODE = "dark"
ctk.set_appearance_mode(DARK_MODE)
ctk.set_default_color_theme("green")


class App(ctk.CTk):
    """
    This is the main window of the application.

    Attributes
    ----------
    parser: Parser
        It is the Parser object which is used to parse the formula.
    formulas: list
        It is the list of example formulas.
    selected_option: tk.StringVar
        It is the variable which holds the selected option from the dropdown menu.
    combobox: ctk.CTkOptionMenu
        It is the dropdown menu from which the user can select a formula.
    entry: ctk.CTkEntry
        It is the entry box in which the user can type the formula.
    button: ctk.CTkButton
        It is the button which checks the validity of the formula.
    footer: ctk.CTkTextbox
        It is the footer of the application which contains the copyright information.
    left_frame: ctk.CTkFrame
        It is the left frame of the application.
    right_frame: ctk.CTkFrame
        It is the right frame of the application.

    Methods
    -------
    update_entry(self, option)
        It updates the entry with the selected formula.
    check_validity(self)
        It checks the validity of the formula and shows the result.
    show_about(self)
        It shows the about information.

    """
    def __init__(self):
        """
        Initializes the main window of the application.

        """
        super().__init__()

        self.parser= Parser()
        
        self.title("Modal Validity Checker")
        self.geometry("1200x700+100+100")
        self.minsize(1200, 700)

        # contains everything
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.left_frame = ctk.CTkFrame(main_container)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.right_frame = ctk.CTkFrame(main_container)
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        
        self.footer = ctk.CTkTextbox(main_container,wrap="word",height=35)
        self.footer.insert(tk.END, "Modal Validity Checker v1.0 \nCopyright © 2023 All rights reserved worldwide. ","footer")
        self.footer.tag_add("footer", tk.END + "-1c", tk.END)
        self.footer.tag_config("footer", justify='center')
        self.footer.tag_lower("footer")
        self.footer.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.footer.configure(font=("Arial", 7))

        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(0, weight=1)

        # left frame
        label = ctk.CTkLabel(master=self.left_frame, text="Enter modal logic formula:")
        label.grid(row=0, column=0, padx=20, pady=40)
        label.configure(font=("Arial", 16))

        self.formulas = [ "◊p → ¬□¬p","◊p → □p","□(p → q) ∧ ◊r","◻◻◻◻(a->b)|◻◻◻◻◻b"]
        self.selected_option = tk.StringVar(self.left_frame)
        self.selected_option.set("Examples")
        self.combobox = ctk.CTkOptionMenu(master=self.left_frame,variable=self.selected_option,width=20,
                                     values=self.formulas,command=lambda option: self.update_entry(option),
                                     fg_color= "#555555" ,button_color= "#555555" ,button_hover_color= "#c9c9c9")
        
        self.combobox.grid(row=2, column=0, padx=40, pady=10)

        self.entry =ctk.CTkEntry(master=self.left_frame,placeholder_text="Type here...")
        self.entry.grid(row=3, column=0, padx=20, pady=10)

        self.button = ctk.CTkButton(master=self.left_frame, text="Check Validity",font=('Arial', 14, 'bold'),
                                    command=self.check_validity)
        self.button.grid(row=4, column=0, padx=20, pady=40)

        help_button = ctk.CTkButton(master=self.left_frame, text="Help", font=('Arial', 12),
                            fg_color='#555555', hover_color='#00A550', 
                            command=self.show_about)
        help_button.grid(row=6, column=0, padx=20, pady=10,sticky="s")
        self.left_frame.rowconfigure(5, weight=10)
        self.left_frame.rowconfigure(1, weight=1)

        # right frame
        self.about = ctk.CTkTextbox(self.right_frame,wrap="word")
        self.about.insert(tk.END, "To use the Modal Logic Validity Checker, follow these steps:\n\n")
        self.about.insert(tk.END, "* Type your modal logic formula into the text box on the left using any combination of the following symbols:\n\n")
        self.about.insert(tk.END, "Negation: '~', '¬', or '!'\nConjunction: '^', '∧', or '&'\nDisjunction: '|', '∨', 'v', or 'V'\nImplication: '->', '→', or '⇒'\nNecessity: '□', '◻', or '[]'\nPossibility: '◇', '◊', or '<>'\nYou can also use any combination of letters to represent variables.\n\n")
        self.about.insert(tk.END, "* Click the \"Check validity\" button to initiate the validity check.\n\n")
        self.about.insert(tk.END, "* The Modal Logic Validity Checker app will use the tableau algorithm to analyze your formula and determine whether it is valid or not. The results of the check will be displayed on the right.\n\n")
        self.about.insert(tk.END, "The algorithm uses a proof by contradiction method, so for any invalid formula expect a graphical representation of the Kripke model where the formula is not valid. If the formula is valid in all frames, just a positive result will be given.\n\n")
        self.about.insert(tk.END, "Examples explained:\n\n")
        self.about.insert(tk.END, "Valid: ◊p → ¬□¬p\nThis formula expresses the idea that if something is possibly true, then it is not necessarily false. In other words, if there is a possible world in which p is true, then it cannot be the case that in all possible worlds, p is necessarily false.\n\n")
        self.about.insert(tk.END, "Invalid: ◊p → □p\nThis formula says that if p is possibly true, then it is necessarily true. This is an invalid formula because it is not true in all possible worlds or situations.")
        
        self.about.configure(font=("Arial", 16),border_spacing=30)
        self.about.pack(fill=tk.BOTH,  expand=True, padx=20)

        self.disclaimer = ctk.CTkLabel(self.right_frame, pady=25,wraplength=800,font=("Arial", 10),anchor='center',text=" Disclaimer: This app is intended for educational purposes only and should not be relied upon for legal or professional advice. The creators of this app are not liable for any damages or losses resulting from the use of this app.")
        self.disclaimer.pack(side="bottom")
        
        self.output_text = ctk.CTkTextbox(self.right_frame,wrap="word")
        self.output_result = ctk.CTkFrame(self.right_frame,corner_radius=20)


    
    def update_entry(self, selected_option: str) -> None:
        """
        Update the entry textbox with the selected formula.

        Parameters
        ----------
        selected_option: str
            Formula selected from the combobox.

        Returns
        -------
        None

        """
        self.entry.delete(0, "end")
        self.entry.insert(0, selected_option)
        self.combobox.set("Examples")
        
    
    def show_about(self) -> None:
        """
        Show the about section.

        Returns
        -------
        None

        """
        self.output_result.pack_forget()
        self.output_text.pack_forget()
        self.about.pack(fill=tk.BOTH,  expand=True, padx=20)
        self.disclaimer.pack(side="bottom")


    def check_validity(self) -> None:
        """
        Checks and show the validity of the formula.

        Returns
        -------
        None

        """
        text = self.entry.get()
        if not text:
            messagebox.showerror("Error", "Please enter some text")
            return
        try:
            formula = self.parser.parse_text(text)
        except SyntaxError as e:
             messagebox.showerror("Error:", e)
             return

        self.about.pack_forget()
        self.disclaimer.pack_forget()
        self.output_text.delete("0.0", "end")
        for widget in self.output_result.winfo_children():
            widget.destroy()
        
        self.output_text.insert("0.0", f"Input: {text}\n\n")
        self.output_text.configure(font=("Arial", 20),border_spacing=30,corner_radius=0)
        self.output_text.pack(fill=tk.BOTH,  expand=True, padx=10)
        
        valid, model = tableau_procedure.check_validity_of(formula)
        
        if valid: 
            output = "VALID"
            
            r=ctk.CTkTextbox(self.output_result)
            r.insert("0.0",f"Result:\n{output}")
            r.configure(font=("Arial", 20),border_spacing=30)
            r.pack(fill=tk.X, expand=True)
           
            self.output_result.pack(fill=tk.X,  expand=True, padx=10, pady=20)
        else:
            output="INVALID"
            self.output_text.insert("4.0", f"Result: {output}\n\n")

            r=ctk.CTkTextbox(self.output_result, height=60,wrap="word")
            r.insert("1.0","In the model below, the light green node is a world where the formula is not valid. Therefore, the formula is not valid in all frames. Note that a node with the label [] means a world where none of the variables is true. The directed edges represent the accessibility between different words.")
            r.configure(font=("Arial", 14),corner_radius=0,border_spacing=10)
            r.pack(fill=tk.X)
            
            graph = modelGraph.GraphVisualization(self.output_result,model)
            graph.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            self.output_result.pack(fill=tk.BOTH,  expand=True, pady=20)
        
        if text not in self.formulas:
            self.formulas.append(text)
            self.combobox.configure(values=self.formulas)
        self.entry.delete(0, "end")

if __name__ == '__main__':
    app = App()

    app.protocol("WM_DELETE_WINDOW", app.quit)

    app.mainloop()


