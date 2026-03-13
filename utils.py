"""
Utility functions for MIDI analysis
"""

from collections import Counter
import math

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


def normalized_entropy(values):
    """
    Shannon entropy normalized to [0, 1].
    0  -> all values identical
    1  -> maximal diversity for given set
    """
    if not values:
        return 0.0

    counts = Counter(values)
    total = len(values)
    probs = [count / total for count in counts.values()]

    entropy = -sum(p * math.log2(p) for p in probs if p > 0)
    max_entropy = math.log2(len(counts)) if len(counts) > 1 else 0.0

    if max_entropy == 0.0:
        return 0.0

    return entropy / max_entropy


def quantize(value, step=0.25):
    if step <= 0:
        return value
    return round(value / step) * step


def ngram_unique_ratio(tokens, n):
    if len(tokens) < n:
        return 0.0

    ngrams = [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]
    if not ngrams:
        return 0.0

    return len(set(ngrams)) / len(ngrams)
