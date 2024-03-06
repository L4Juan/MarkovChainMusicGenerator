import tkinter
import customtkinter
import MarkovChain
import numpy as np
import os
from music21 import metadata, note, stream, midi, converter
#import pdb; pdb.set_trace()

class MarkovChainInterface:
    state=12
    
    def _reset_button_colors(self):
        for b in self.buttons:
            b.configure(fg_color=self.offState)
            
    def C5_btn_click(self):
        self.state=0
        self._reset_button_colors()
        self.C5_btn.configure(fg_color=self.onState)
        
        otherProbabilities = self.model.get_transition_probabilities(self.state)
        self._show_probabilities(otherProbabilities)
        #TODO should recieve a list of the probabilities by order
        
    def Csharp5_btn_click(self):
        self.state=1
        self._reset_button_colors()
        self.Csharp5_btn.configure(fg_color=self.onState)
        
        otherProbabilities = self.model.get_transition_probabilities(self.state)
        self._show_probabilities(otherProbabilities)

    def D5_btn_click(self):
        self.state=2
        self._reset_button_colors()
        self.D5_btn.configure(fg_color=self.onState)
        
        otherProbabilities = self.model.get_transition_probabilities(self.state)
        self._show_probabilities(otherProbabilities)

    def Dsharp5_btn_click(self):
        self.state=3
        self._reset_button_colors()
        self.Dsharp5_btn.configure(fg_color=self.onState)
        
        otherProbabilities = self.model.get_transition_probabilities(self.state)
        self._show_probabilities(otherProbabilities)

    def E5_btn_click(self):
        self.state=4
        self._reset_button_colors()
        self.E5_btn.configure(fg_color=self.onState)
        
        otherProbabilities = self.model.get_transition_probabilities(self.state)
        self._show_probabilities(otherProbabilities)

    def F5_btn_click(self):
        self.state=5
        self._reset_button_colors()
        self.F5_btn.configure(fg_color=self.onState)
        
        otherProbabilities = self.model.get_transition_probabilities(self.state)
        self._show_probabilities(otherProbabilities)

    def Fsharp5_btn_click(self):
        self.state=6
        self._reset_button_colors()
        self.Fsharp5_btn.configure(fg_color=self.onState)
        
        otherProbabilities = self.model.get_transition_probabilities(self.state)
        self._show_probabilities(otherProbabilities)

    def G5_btn_click(self):
        self.state=7
        self._reset_button_colors()
        self.G5_btn.configure(fg_color=self.onState)
        
        otherProbabilities = self.model.get_transition_probabilities(self.state)
        self._show_probabilities(otherProbabilities)

    def Gsharp5_btn_click(self):
        self.state=8
        self._reset_button_colors()
        self.Gsharp5_btn.configure(fg_color=self.onState)
        
        otherProbabilities = self.model.get_transition_probabilities(self.state)
        self._show_probabilities(otherProbabilities)

    def A5_btn_click(self):
        self.state=9
        self._reset_button_colors()
        self.A5_btn.configure(fg_color=self.onState)
        
        otherProbabilities = self.model.get_transition_probabilities(self.state)
        self._show_probabilities(otherProbabilities)

    def Asharp5_btn_click(self):
        self.state=10
        self._reset_button_colors()
        self.Asharp5_btn.configure(fg_color=self.onState)
        
        otherProbabilities = self.model.get_transition_probabilities(self.state)
        self._show_probabilities(otherProbabilities)

    def B5_btn_click(self):
        self.state=11
        self._reset_button_colors()
        self.B5_btn.configure(fg_color=self.onState)
        
        otherProbabilities = self.model.get_transition_probabilities(self.state)
        self._show_probabilities(otherProbabilities)

    #? def SelectFiles_btn_click(self):

    def _show_probabilities(self, probabilities):
        for box, p in zip(self.txtBoxes, probabilities):
            box.configure(placeholder_text=str(p))
            
    def _save_values(self):
        if self.state == 0:
            print("use states like this")
    
    def _show_initial_probabilities(self):
        self.state = 12
        self._reset_button_colors()
        self._show_probabilities(self.model.initial_probabilities)
    
    def __init__(self):
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("green")
        self.offState = "green"
        self.onState = "purple"

        self.app = customtkinter.CTk()
        self.app.geometry("1500x500")
        self.app.title("Markov Chain Generator")

        self.keyboardFrame = customtkinter.CTkFrame(self.app)
        self.keyboardFrame.pack()
        self.blackKeysFrame = customtkinter.CTkFrame(self.keyboardFrame)
        self.blackKeysFrame.pack()
        self.whiteKeysFrame = customtkinter.CTkFrame(self.keyboardFrame)
        self.whiteKeysFrame.pack()
        self.functionsFrame = customtkinter.CTkFrame(self.app)
        self.functionsFrame.pack()

        self.C5_btn = customtkinter.CTkButton(self.whiteKeysFrame, text="C5", command=self.C5_btn_click, hover = False)
        self.C5_btn.grid(row=0, column = 0)
        self.C5_txt = customtkinter.CTkEntry(self.whiteKeysFrame)
        self.C5_txt.grid(row=1, column = 0)

        self.Csharp5_btn = customtkinter.CTkButton(self.blackKeysFrame, text="C#5", command=self.Csharp5_btn_click, hover = False)
        self.Csharp5_btn.grid(row=0, column = 0, padx=5, pady=5)
        self.Csharp5_txt = customtkinter.CTkEntry(self.blackKeysFrame)
        self.Csharp5_txt.grid(row=1, column = 0, padx=5, pady=5)


        self.D5_btn = customtkinter.CTkButton(self.whiteKeysFrame, text="D5", command=self.D5_btn_click, hover = False)
        self.D5_btn.grid(row=0, column = 1, padx=5, pady=5)
        self.D5_txt = customtkinter.CTkEntry(self.whiteKeysFrame)
        self.D5_txt.grid(row=1, column = 1, padx=5, pady=5)
        
        self.Dsharp5_btn = customtkinter.CTkButton(self.blackKeysFrame, text="D#5", command=self.Dsharp5_btn_click, hover = False)
        self.Dsharp5_btn.grid(row=0, column = 1, padx=5, pady=5)
        self.Dsharp5_txt = customtkinter.CTkEntry(self.blackKeysFrame)
        self.Dsharp5_txt.grid(row=1, column = 1, padx=5, pady=5)

        self.E5_btn = customtkinter.CTkButton(self.whiteKeysFrame, text="E5", command=self.E5_btn_click, hover = False)
        self.E5_btn.grid(row=0, column = 2, padx=5, pady=5)
        self.E5_txt = customtkinter.CTkEntry(self.whiteKeysFrame)
        self.E5_txt.grid(row=1, column = 2, padx=5, pady=5)

        self.F5_btn = customtkinter.CTkButton(self.whiteKeysFrame, text="F5", command=self.F5_btn_click, hover = False)
        self.F5_btn.grid(row=0, column = 3, padx=5, pady=5)
        self.F5_txt = customtkinter.CTkEntry(self.whiteKeysFrame)
        self.F5_txt.grid(row=1, column = 3, padx=5, pady=5)

        self.Fsharp5_btn = customtkinter.CTkButton(self.blackKeysFrame, text="F#5", command=self.Fsharp5_btn_click, hover = False)
        self.Fsharp5_btn.grid(row=0, column = 3, padx=5, pady=5)
        self.Fsharp5_txt = customtkinter.CTkEntry(self.blackKeysFrame)
        self.Fsharp5_txt.grid(row=1, column = 3, padx=5, pady=5)

        self.G5_btn = customtkinter.CTkButton(self.whiteKeysFrame, text="G5", command=self.G5_btn_click, hover = False)
        self.G5_btn.grid(row=0, column = 4, padx=5, pady=5)
        self.G5_txt = customtkinter.CTkEntry(self.whiteKeysFrame)
        self.G5_txt.grid(row=1, column = 4, padx=5, pady=5)

        self.Gsharp5_btn = customtkinter.CTkButton(self.blackKeysFrame, text="G#5", command=self.Gsharp5_btn_click, hover = False)
        self.Gsharp5_btn.grid(row=0, column = 4, padx=5, pady=5)
        self.Gsharp5_txt = customtkinter.CTkEntry(self.blackKeysFrame)
        self.Gsharp5_txt.grid(row=1, column = 4, padx=5, pady=5)

        self.A5_btn = customtkinter.CTkButton(self.whiteKeysFrame, text="A5", command=self.A5_btn_click, hover = False)
        self.A5_btn.grid(row=0, column = 5, padx=5, pady=5)
        self.A5_txt = customtkinter.CTkEntry(self.whiteKeysFrame)
        self.A5_txt.grid(row=1, column = 5, padx=5, pady=5)

        self.Asharp5_btn = customtkinter.CTkButton(self.blackKeysFrame, text="A#5", command=self.Asharp5_btn_click, hover = False)
        self.Asharp5_btn.grid(row=0, column = 5, padx=5, pady=5)
        self.Asharp5_txt = customtkinter.CTkEntry(self.blackKeysFrame)
        self.Asharp5_txt.grid(row=1, column = 5, padx=5, pady=5)

        self.B5_btn = customtkinter.CTkButton(self.whiteKeysFrame, text="B5", command=self.B5_btn_click, hover = False)
        self.B5_btn.grid(row=0, column = 6, padx=5, pady=5)
        self.B5_txt = customtkinter.CTkEntry(self.whiteKeysFrame)
        self.B5_txt.grid(row=1, column = 6, padx=5, pady=5)

        empty = customtkinter.CTkLabel(self.blackKeysFrame, width=80, text="")
        empty.grid(row=0, column=2)
        
        self.save_btn = customtkinter.CTkButton(self.functionsFrame, text="Save Values", command = self._save_values )
        self.save_btn.grid(row=0, column=5, padx=10, pady=10)
        self.showInitialProbabilities_btn = customtkinter.CTkButton(self.functionsFrame, text="Initial Probabilities", command = self._show_initial_probabilities, )
        self.showInitialProbabilities_btn.grid(row=0, column=0, padx=10, pady=10)
    

        
        self.buttons = [
            self.C5_btn,
            self.Csharp5_btn,
            self.D5_btn,
            self.Dsharp5_btn,
            self.E5_btn,
            self.F5_btn,
            self.Fsharp5_btn,
            self.G5_btn,
            self.Gsharp5_btn,
            self.A5_btn,
            self.Asharp5_btn,
            self.B5_btn]
        
        self.txtBoxes = [
            self.C5_txt,
            self.Csharp5_txt,
            self.D5_txt,
            self.Dsharp5_txt,
            self.E5_txt,
            self.F5_txt,
            self.Fsharp5_txt,
            self.G5_txt,
            self.Gsharp5_txt,
            self.A5_txt,
            self.Asharp5_txt,
            self.B5_txt]
        
        self._reset_button_colors()
        training_data = midi_train_data()
        states = [
            ("C5", 1),
            ("C#5", 1),
            ("D5", 1),
            ("D#5", 1),
            ("E5", 1),
            ("F5", 1),
            ("F#5", 1),
            ("G5", 1),
            ("G#5", 1),
            ("A5", 1),
            ("A#5", 1),
            ("B5", 1)
        ]
        self.model = MarkovChain.MarkovChainMelodyGenerator(states)
        #todo add button to train with wanted midi file
        self.model.train(training_data)
        
        self._show_initial_probabilities()


        generated_melody = self.model.generate(40)
        save_melody(generated_melody)
        
        
            
        
        
    def run(self):
        self.app.mainloop()
        
        
folder_path = "Train"


def midi_train_data():
    
    if not os.path.isdir(folder_path):
        print("Make sure to create  Train forlder in the program folder")
        return 
    all_files = os.listdir(folder_path)

    # Filter out only MIDI files (assuming they have the .mid extension)
    midi_files = [file for file in all_files if file.lower().endswith(".mid")]
    
    if not midi_files:
        print(f"No MIDI files found in '{folder_path}'.")
        return 
    
    notes = []
    for filename in midi_files:
        
        stream = converter.parse(folder_path+"/"+filename)
    
        if len(notes) > 1:
            #adds a separator between files to adjust starting matrix
            notes.append(note.Note("C0", quarterLength=2))
        
        for n in stream.flat.notes:
            if n.isChord:
                note_pitch = str(n[0].pitch)[:-1] + "5"
            else:
                note_pitch = str(n.pitch)[:-1] + "5"
            
            notes.append(note.Note(note_pitch, quarterLength=1))
            
    return notes

def save_melody(melody):

    #print(melody)
    midi_stream = stream.Stream()
    for n, d in melody:
        midi_stream.append(note.Note(n, quarterLength=d))

    midi_stream.write('midi', fp='Generations/output.mid')


def main():
    app = MarkovChainInterface()
    app.run()
    
    
    
if __name__ == "__main__":
    main()
        
        

    
