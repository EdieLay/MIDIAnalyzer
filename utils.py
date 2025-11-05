"""
Utility functions for MIDI analysis
"""


def note_name(midi_number):
    """
    Convert MIDI note number to note name with octave
    
    Args:
        midi_number: MIDI note number (0-127)
    
    Returns:
        String representation of note (e.g., "C4", "A#5")
    """
    note_names = ["C", "C#", "D", "D#", "E", "F",
                  "F#", "G", "G#", "A", "A#", "B"]
    name = note_names[midi_number % 12]
    octave = (midi_number // 12) - 1
    return f"{name}{octave}"


def duration_to_note_length(duration_beats):
    """
    Map duration in beats to fractional note length
    
    Args:
        duration_beats: Duration in beats
    
    Returns:
        String representation of note length
    """
    note_lengths = {
        4.0: "1",
        2.0: "0.5",
        1.0: "0.25",
        0.5: "0.125",
        0.25: "0.063",
        0.125: "0.032"
    }
    # Find closest value
    closest = min(note_lengths.keys(), key=lambda x: abs(x - duration_beats))
    return note_lengths[closest]


def is_consonant_interval(interval):
    """
    Determine if an interval (in semitones, mod 12) is consonant
    
    Args:
        interval: Interval in semitones (mod 12)
    
    Returns:
        True if consonant, False if dissonant
    """
    # Dissonant intervals: minor 2nd, major 2nd, tritone, minor 7th, major 7th
    dissonant = [1, 2, 6, 10, 11]
    return interval not in dissonant

def find_repeating_patterns(notes, min_length=2):
    """
    Find all maximal-length repeating patterns in a note sequence.
    Returns list of tuples: (pattern, count, positions)
    """
    patterns = []
    n = len(notes)
    used_positions = set()
    
    # Check patterns from longest to shortest
    for length in range(min(n//2, 40), min_length-1, -1):
        i = 0
        while i <= n - length:
            if i in used_positions:
                i += 1
                continue
                
            pattern = tuple(notes[i:i+length])
            matches = [i]
            
            # Find all subsequent matches not overlapping with used positions
            j = i + length
            while j <= n - length:
                if all(j+k not in used_positions for k in range(length)):
                    if tuple(notes[j:j+length]) == pattern:
                        matches.append(j)
                        j += length
                    else:
                        j += 1
                else:
                    j += length
            
            if len(matches) > 1:
                # Record pattern and mark positions
                patterns.append((pattern, len(matches), matches))
                for pos in matches:
                    used_positions.update(range(pos, pos+length))
                i += length * len(matches)
            else:
                i += 1
    
    return patterns
