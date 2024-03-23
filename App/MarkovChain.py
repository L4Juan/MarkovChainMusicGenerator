import numpy as np
import os
from music21 import metadata, note, stream, midi, converter
#this is just a comment

folder_path = "Train/"
class MarkovChainMelodyGenerator:
    """
    Represents a Markov Chain model for melody generation.
    """

    def __init__(self, states):
        """
        Initialize the MarkovChain with a list of states.

        Parameters:
            states (list of tuples): A list of possible (pitch, duration)
                pairs.
        """
        self.states = states
        self.initial_probabilities = np.zeros(len(states))
        self.transition_matrix = np.zeros((len(states), len(states)))
        self._state_indexes = {state: i for (i, state) in enumerate(states)}

    def train(self, notes):
        """
        Train the model based on a list of notes.

        Parameters:
            notes (list): A list of music21.note.Note objects.
        """
        self._calculate_initial_probabilities(notes)
        self._calculate_transition_matrix(notes)

    def generate(self, length):
        """
        Generate a melody of a given length.

        Parameters:
            length (int): The length of the sequence to generate.

        Returns:
            melody (list of tuples): A list of generated states.
        """
        melody = [self._generate_starting_state()]
        for _ in range(1, length):
            melody.append(self._generate_next_state(melody[-1]))
        return melody

    def get_transition_probabilities(self, n):
        return self.transition_matrix[n]

    def _calculate_initial_probabilities(self, notes):
        """
        Calculate the initial probabilities from the provided notes.

        Parameters:
            notes (list): A list of music21.note.Note objects.
        """
        for note in notes:
            if str(note.pitch) == "C0":
                continue
            self._increment_initial_probability_count(note)
        self._normalize_initial_probabilities()
        
    def saveProbabilities(self, n, probabilities):
        if sum(probabilities) != 1:
            #make this a boolean and return false so that application can print a messag
            return
        if n == 12:
            self.initial_probabilities = probabilities
        

    def _increment_initial_probability_count(self, note):
        """
        Increment the probability count for a given note.

        Parameters:
            note (music21.note.Note): A note object.
        """
        state = (note.pitch.nameWithOctave, note.duration.quarterLength)
        self.initial_probabilities[self._state_indexes[state]] += 1

    def _normalize_initial_probabilities(self):
        """
        Normalize the initial probabilities array such that the sum of all
        probabilities equals 1.
        """
        total = np.sum(self.initial_probabilities)
        if total:
            self.initial_probabilities /= total
        self.initial_probabilities = np.nan_to_num(self.initial_probabilities)

    def _calculate_transition_matrix(self, notes):
        """
        Calculate the transition matrix from the provided notes.

        Parameters:
            notes (list): A list of music21.note.Note objects.
        """
        for i in range(len(notes) - 1):
            if str(notes[i+1].pitch) == "C0" or str(notes[i].pitch) == "C0":
                continue
            self._increment_transition_count(notes[i], notes[i + 1])
        self._normalize_transition_matrix()

    def _increment_transition_count(self, current_note, next_note):
        """
        Increment the transition count from current_note to next_note.

        Parameters:
            current_note (music21.note.Note): The current note object.
            next_note (music21.note.Note): The next note object.
        """
        state = (
            current_note.pitch.nameWithOctave,
            current_note.duration.quarterLength,
        )
        next_state = (
            next_note.pitch.nameWithOctave,
            next_note.duration.quarterLength,
        )
        self.transition_matrix[
            self._state_indexes[state], self._state_indexes[next_state]
        ] += 1

    def _normalize_transition_matrix(self):
        """
        This method normalizes each row of the transition matrix so that the
        sum of probabilities in each row equals 1. This is essential for the rows
        of the matrix to represent probability distributions of
        transitioning from one state to the next.
        """

        # Calculate the sum of each row in the transition matrix.
        # These sums represent the total count of transitions from each state
        # to any other state.
        row_sums = self.transition_matrix.sum(axis=1)

        # Use np.errstate to ignore any warnings that arise during division.
        # This is necessary because we might encounter rows with a sum of 0,
        # which would lead to division by zero.
        with np.errstate(divide="ignore", invalid="ignore"):
            # Normalize each row by its sum. np.where is used here to handle
            # rows where the sum is zero.
            # If the sum is zero (no transitions from that state), np.where
            # ensures that the row remains a row of zeros instead of turning
            # into NaNs due to division by zero.
            self.transition_matrix = np.where(
                row_sums[:, None],  # Condition: Check each row's sum.
                # True case: Normalize if sum is not zero.
                self.transition_matrix / row_sums[:, None],
                0,  # False case: Keep as zero if sum is zero.
            )

    def _generate_starting_state(self):
        """
        Generate a starting state based on the initial probabilities.

        Returns:
            A state from the list of states.
        """
        initial_index = np.random.choice(
            list(self._state_indexes.values()), p=self.initial_probabilities
        )
        return self.states[initial_index]

    def _generate_next_state(self, current_state):
        """
        Generate the next state based on the transition matrix and the current
        state.

        Parameters:
            current_state: The current state in the Markov Chain.

        Returns:
            The next state in the Markov Chain.
        """
        if self._does_state_have_subsequent(current_state):
            index = np.random.choice(
                list(self._state_indexes.values()),
                p=self.transition_matrix[self._state_indexes[current_state]],
            )
            return self.states[index]
        return self._generate_starting_state()

    def _does_state_have_subsequent(self, state):
        """
        Check if a given state has a subsequent state in the transition matrix.

        Parameters:
            state: The state to check.

        Returns:
            True if the state has a subsequent state, False otherwise.
        """
        return self.transition_matrix[self._state_indexes[state]].sum() > 0


def create_training_data():
    """
    Creates a list of sample training notes for the melody of "Twinkle
    Twinkle Little Star."

    Returns:
        - list: A list of music21.note.Note objects.
    """
    return [
        note.Note("C5", quarterLength=1),
        note.Note("C5", quarterLength=1),
        note.Note("G5", quarterLength=1),
        note.Note("G5", quarterLength=1),
        note.Note("A5", quarterLength=1),
        note.Note("A5", quarterLength=1),
        note.Note("G5", quarterLength=2),
        note.Note("F5", quarterLength=1),
        note.Note("F5", quarterLength=1),
        note.Note("E5", quarterLength=1),
        note.Note("E5", quarterLength=1),
        note.Note("D5", quarterLength=1),
        note.Note("D5", quarterLength=1),
        note.Note("C5", quarterLength=2),
    ]
    
def midi_train_data():
    
    all_files = os.listdir(folder_path)

    # Filter out only MIDI files (assuming they have the .mid extension)
    midi_files = [file for file in all_files if file.lower().endswith(".mid")]
    
    if not midi_files:
        print(f"No MIDI files found in '{folder_path}'.")
        return
    
    notes = []
    for filename in midi_files:
        #TODO Decide if you wana be able to train from multiple files or just one
        #if able to use multiple files probably have to modify notes format and train method to recognise when one stops and one endsolys
        
        stream = converter.parse(folder_path+filename)
    
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
