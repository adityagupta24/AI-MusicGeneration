from music21 import converter, note, chord, stream, instrument
import tensorflow as tf
from tensorflow import keras
import numpy as np
import pickle
import music21
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


with open('./home/notes', 'rb') as f:
    notes = pickle.load(f)
f.close()

snotes = sorted(set(notes))
n_vocab = len(snotes)
ele_int = dict((ele, idx) for idx, ele in enumerate(snotes))

session = tf.Session()
keras.backend.set_session(session)


model = keras.models.load_model("./home/final_model.hdf5")
model._make_predict_function()


def generate_music():

    sequence_length = 50
    network_input = []
    for i in range(len(notes) - sequence_length):
        seq_in = notes[i:i+sequence_length]  # in the string format
        network_input.append([ele_int[ch] for ch in seq_in])

    # Taking a random start sequence to generate the next sequence
    start = np.random.randint(len(network_input))
    pattern = network_input[start]
    prediction_output = []
    int_to_ele = dict((idx, ele)for idx, ele in enumerate(snotes))

    with session.as_default():
        with session.graph.as_default():
            for i in range(120):
                prediction_input = np.reshape(pattern, (1, sequence_length, 1))
                prediction_input = prediction_input/float(n_vocab)
                prediction = model.predict(prediction_input)
                idx = np.argmax(prediction)
                prediction_output.append(int_to_ele[idx])
                pattern.append(idx)
                pattern = pattern[1:]

        output_notes = []
    offset = 0

    for pattern in prediction_output:
        # if the pattern is a chord, then
        if ('+' in pattern) or pattern.isdigit():
            all_notes = pattern.split("+")
            temp_notes = []
            # print(all_notes)
            for current_note in all_notes:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()
                temp_notes.append(new_note)
            # It creates a chord with the help of the list of the notes
            new_chord = chord.Chord(temp_notes)
            new_chord.storedInstrument = instrument.Piano()
            output_notes.append(new_chord)

        else:
            # if the pattern is a note,then
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)
        offset += 0.5

    midi_stream = stream.Stream(output_notes)
    midi_stream.write("midi", "./static/songs/newPianoSong.mid")
