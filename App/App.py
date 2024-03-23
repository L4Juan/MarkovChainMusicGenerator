"""In app2, unlike the original, I attempt to change button from keys to be radio buttons allowing for a cleaner code

Returns:
    _type_: _description_
"""
import tkinter
import customtkinter
import MarkovChain
import os
from music21 import metadata, note, stream, midi, converter
#import pdb; pdb.set_trace()

folder_path = "../Train"
#create toplevelwindow with yes and no buttons for queries (take question through string variable)

class MarkovChainGUI:
    def _insert_info(self, info):
        self.infoBox.configure(state="normal")
        self.infoBox.insert("0.0", info + "\n")
        self.infoBox.configure(state="disabled")
    
    def _show_probabilities(self, probabilities):
        for box, p in zip(self.txtBoxes, probabilities):
            box.configure(placeholder_text=str(p))
            
    def _validate_entries(self):
        for txtBox in self.txtBoxes:
            if len(txtBox.get())>0:
                try:
                    float(txtBox.get())
                except ValueError:
                    self._insert_info("value: " + txtBox.get() + " gave an error")
                    return False
        return True

    def _save_values(self):
        #TODO validate model is trained and or has enough values
        #TODO test how model will react to training with one or two midi notes
        
        if not self._validate_entries():
            return

        sumNewProbabilities=0
        if self.radioVar.get() == 12:
            thisProbabilities = self.model.initial_probabilities
        else:
            thisProbabilities = self.model.get_transition_probabilities(self.radioVar.get())
            
        for txtBox in self.txtBoxes:
            if len(txtBox.get()):
                sumNewProbabilities += float(txtBox.get())
        
        if sumNewProbabilities > 1:
            self._insert_info("Error: New probabilities must add up to 1 or less") 
            return

        sumOthers=0
        for i in range(12):
            if len(self.txtBoxes[i].get()):
                thisProbabilities[i] = float(self.txtBoxes[i].get())
            else:
                sumOthers+=thisProbabilities[i]

        for i in range(12):
                if not len(self.txtBoxes[i].get()):
                    thisProbabilities[i] = thisProbabilities[i]*(1-sumNewProbabilities)/sumOthers
        sum2=0
        for p in thisProbabilities:
            sum2+=p
        
        #even out the tini decimal that sometimes doesnt add up
        if sum2 != 0:
            for i in range(12):
                if thisProbabilities[i] > 0:
                    #Sum to first non empty probability so that 0 prob numbers cannot happen
                    thisProbabilities[i] += 1 - sum2
                    break

        #save values
        self.model.saveProbabilities(self.radioVar.get(), thisProbabilities)
        #check values will be used for next generaaation
    
    def _show_initial_probabilities(self):
        self._show_probabilities(self.model.initial_probabilities)
    
    
    def _radio_button_event(self):
        
        otherProbabilities = self.model.get_transition_probabilities(self.radioVar.get())
        self._show_probabilities(otherProbabilities)
        
    def _train(self):
        training_data = self._midi_train_data()
        if len(training_data)>0:
            self.model.train(training_data)
            self._insert_info("Info: model trained")
        
        else:
            self._insert_info("Error: no training data found")
        self._show_initial_probabilities()
        self.radioVar.set(12)
   
        
        
    def _generate(self):
        try:
            generated_melody = self.model.generate(40)
            self._insert_info("Info: melody generated")
            self._save_melody(generated_melody)
            self._insert_info("Info: melody saved to 'Generations' folder")
        except Exception:
            self._insert_info("Error: train model before generating a melody")
            return
            
    def __init__(self):
        
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("green")
        self.offState = "green"
        self.onState = "purple"

        self.app = customtkinter.CTk()
        self.app.geometry("1500x500")
        self.app.title("Markov Chain Generator")

        self.keyboardFrame = customtkinter.CTkFrame(self.app)
        self.keyboardFrame.grid(row=0, column=1)
        self.blackKeysFrame = customtkinter.CTkFrame(self.keyboardFrame)
        self.blackKeysFrame.pack()
        self.whiteKeysFrame = customtkinter.CTkFrame(self.keyboardFrame)
        self.whiteKeysFrame.pack()
        self.functionsFrame = customtkinter.CTkFrame(self.app)
        self.functionsFrame.grid(row=1, column=1)
        
        
        self.radioVar = tkinter.Variable(value=-1)

        self.C5_btn = customtkinter.CTkRadioButton(self.whiteKeysFrame, text="C5", command=self._radio_button_event, variable=self.radioVar, value = 0)
        self.C5_btn.grid(row=0, column = 0)
        self.C5_txt = customtkinter.CTkEntry(self.whiteKeysFrame)
        self.C5_txt.grid(row=1, column = 0)

        self.Csharp5_btn = customtkinter.CTkRadioButton(self.blackKeysFrame, text="C#5", command=self._radio_button_event, variable=self.radioVar, value = 1)
        self.Csharp5_btn.grid(row=0, column = 0, padx=5, pady=5)
        self.Csharp5_txt = customtkinter.CTkEntry(self.blackKeysFrame)
        self.Csharp5_txt.grid(row=1, column = 0, padx=5, pady=5)


        self.D5_btn = customtkinter.CTkRadioButton(self.whiteKeysFrame, text="D5", command=self._radio_button_event, variable=self.radioVar, value = 2)
        self.D5_btn.grid(row=0, column = 1, padx=5, pady=5)
        self.D5_txt = customtkinter.CTkEntry(self.whiteKeysFrame)
        self.D5_txt.grid(row=1, column = 1, padx=5, pady=5)
        
        self.Dsharp5_btn = customtkinter.CTkRadioButton(self.blackKeysFrame, text="D#5", command=self._radio_button_event, variable=self.radioVar, value = 3)
        self.Dsharp5_btn.grid(row=0, column = 1, padx=5, pady=5)
        self.Dsharp5_txt = customtkinter.CTkEntry(self.blackKeysFrame)
        self.Dsharp5_txt.grid(row=1, column = 1, padx=5, pady=5)

        self.E5_btn = customtkinter.CTkRadioButton(self.whiteKeysFrame, text="E5", command=self._radio_button_event, variable=self.radioVar, value = 4)
        self.E5_btn.grid(row=0, column = 2, padx=5, pady=5)
        self.E5_txt = customtkinter.CTkEntry(self.whiteKeysFrame)
        self.E5_txt.grid(row=1, column = 2, padx=5, pady=5)

        self.F5_btn = customtkinter.CTkRadioButton(self.whiteKeysFrame, text="F5", command=self._radio_button_event, variable=self.radioVar, value = 5)
        self.F5_btn.grid(row=0, column = 3, padx=5, pady=5)
        self.F5_txt = customtkinter.CTkEntry(self.whiteKeysFrame)
        self.F5_txt.grid(row=1, column = 3, padx=5, pady=5)

        self.Fsharp5_btn = customtkinter.CTkRadioButton(self.blackKeysFrame, text="F#5", command=self._radio_button_event, variable=self.radioVar, value = 6)
        self.Fsharp5_btn.grid(row=0, column = 3, padx=5, pady=5)
        self.Fsharp5_txt = customtkinter.CTkEntry(self.blackKeysFrame)
        self.Fsharp5_txt.grid(row=1, column = 3, padx=5, pady=5)

        self.G5_btn = customtkinter.CTkRadioButton(self.whiteKeysFrame, text="G5", command=self._radio_button_event, variable=self.radioVar, value = 7)
        self.G5_btn.grid(row=0, column = 4, padx=5, pady=5)
        self.G5_txt = customtkinter.CTkEntry(self.whiteKeysFrame)
        self.G5_txt.grid(row=1, column = 4, padx=5, pady=5)

        self.Gsharp5_btn = customtkinter.CTkRadioButton(self.blackKeysFrame, text="G#5", command=self._radio_button_event, variable=self.radioVar, value = 8)
        self.Gsharp5_btn.grid(row=0, column = 4, padx=5, pady=5)
        self.Gsharp5_txt = customtkinter.CTkEntry(self.blackKeysFrame)
        self.Gsharp5_txt.grid(row=1, column = 4, padx=5, pady=5)

        self.A5_btn = customtkinter.CTkRadioButton(self.whiteKeysFrame, text="A5", command=self._radio_button_event, variable=self.radioVar, value = 9)
        self.A5_btn.grid(row=0, column = 5, padx=5, pady=5)
        self.A5_txt = customtkinter.CTkEntry(self.whiteKeysFrame)
        self.A5_txt.grid(row=1, column = 5, padx=5, pady=5)

        self.Asharp5_btn = customtkinter.CTkRadioButton(self.blackKeysFrame, text="A#5", command=self._radio_button_event, variable=self.radioVar, value = 10)
        self.Asharp5_btn.grid(row=0, column = 5, padx=5, pady=5)
        self.Asharp5_txt = customtkinter.CTkEntry(self.blackKeysFrame)
        self.Asharp5_txt.grid(row=1, column = 5, padx=5, pady=5)

        self.B5_btn = customtkinter.CTkRadioButton(self.whiteKeysFrame, text="B5", command=self._radio_button_event, variable=self.radioVar, value = 11)
        self.B5_btn.grid(row=0, column = 6, padx=5, pady=5)
        self.B5_txt = customtkinter.CTkEntry(self.whiteKeysFrame)
        self.B5_txt.grid(row=1, column = 6, padx=5, pady=5)

        empty = customtkinter.CTkLabel(self.blackKeysFrame, width=80, text="")
        empty.grid(row=0, column=2)
        
        self.save_btn = customtkinter.CTkButton(self.functionsFrame, text="Save Values", command = self._save_values )
        self.save_btn.grid(row=0, column=5, padx=10, pady=10)
        self.generate_btn = customtkinter.CTkButton(self.functionsFrame, text="Generate Melody", command = self._generate )
        self.generate_btn.grid(row=0, column=4, padx=10, pady=10)
        self.train = customtkinter.CTkButton(self.functionsFrame, text="Train Model", command = self._train )
        self.train.grid(row=0, column=3, padx=10, pady=10)
        self.showInitialProbabilities_btn = customtkinter.CTkRadioButton(self.keyboardFrame, text="Initial Probabilities", command=self._show_initial_probabilities, variable=self.radioVar, value = 12)
        self.showInitialProbabilities_btn.pack(padx=10, pady=10)
        
        self.infoBox = customtkinter.CTkTextbox(self.app, width=380)
        self.infoBox.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.infoBox.configure()
    

        
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

    def _midi_train_data(self):
        
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

    def _save_melody(self, melody):

        #print(melody)
        midi_stream = stream.Stream()
        for n, d in melody:
            midi_stream.append(note.Note(n, quarterLength=d))

        midi_stream.write('midi', fp='Generations/output.mid')        
        
    def run(self):
        self.app.mainloop()
        
    
    

        

    
