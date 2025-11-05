"""
MIDI file parsing and data extraction
"""

import pretty_midi
from utils import note_name, duration_to_note_length


class MIDIData:
    """Container for parsed MIDI data"""
    
    def __init__(self):
        self.tempo = None
        self.time_signature = None
        self.total_duration = None
        self.instruments = []
        self.notes = []
    
    def __repr__(self):
        return f"MIDIData(tempo={self.tempo}, instruments={len(self.instruments)}, notes={len(self.notes)})"


class NoteData:
    """Container for individual note information"""
    
    def __init__(self, instrument_idx, instrument_name, pitch, start, end, velocity):
        self.instrument_idx = instrument_idx
        self.instrument_name = instrument_name
        self.pitch = pitch
        self.pitch_name = note_name(pitch)
        self.start = start
        self.end = end
        self.duration = end - start
        self.velocity = velocity
        
        # Will be set after tempo is known
        self.start_beats = None
        self.end_beats = None
        self.duration_beats = None
        self.note_length = None
    
    def set_timing_in_beats(self, seconds_per_beat):
        """Calculate beat-based timing information"""
        self.start_beats = self.start / seconds_per_beat
        self.end_beats = self.end / seconds_per_beat
        self.duration_beats = self.duration / seconds_per_beat
        self.note_length = duration_to_note_length(self.duration_beats)
    
    def __repr__(self):
        return f"Note({self.pitch_name}, dur={self.duration:.3f}s)"


def parse_midi_file(filepath):
    """
    Parse a MIDI file and extract all relevant information
    
    Args:
        filepath: Path to MIDI file
    
    Returns:
        MIDIData object containing all parsed information
    
    Raises:
        FileNotFoundError: If MIDI file doesn't exist
        Exception: If MIDI file is invalid or can't be parsed
    """
    try:
        midi = pretty_midi.PrettyMIDI(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"MIDI file not found: {filepath}")
    except Exception as e:
        raise Exception(f"Error parsing MIDI file: {str(e)}")
    
    data = MIDIData()
    
    # Extract global information
    data.tempo = midi.estimate_tempo()
    data.total_duration = midi.get_end_time()
    
    # Get time signature (first one in the file)
    if midi.time_signature_changes:
        ts = midi.time_signature_changes[0]
        data.time_signature = f"{ts.numerator}/{ts.denominator}"
    else:
        data.time_signature = "4/4"  # Default
    
    # Calculate seconds per beat for duration calculations
    seconds_per_beat = 60.0 / data.tempo
    
    # Extract notes from all instruments
    for idx, instrument in enumerate(midi.instruments):
        data.instruments.append({
            'index': idx,
            'name': instrument.name,
            'program': instrument.program,
            'is_drum': instrument.is_drum,
            'note_count': len(instrument.notes)
        })
        
        for note in instrument.notes:
            note_data = NoteData(
                instrument_idx=idx,
                instrument_name=instrument.name,
                pitch=note.pitch,
                start=note.start,
                end=note.end,
                velocity=note.velocity
            )
            note_data.set_timing_in_beats(seconds_per_beat)
            data.notes.append(note_data)
    
    return data
