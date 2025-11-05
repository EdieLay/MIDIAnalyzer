"""
Statistical analysis functions for MIDI data
"""
# Словарь функций в самом конце файла. При создании функции её нужно добавлять в этот словарь.

from collections import Counter
from utils import is_consonant_interval, find_repeating_patterns


def calculate_total_notes(data):
    """Calculate total number of notes"""
    return len(data.notes)


def calculate_average_pitch(data):
    """Calculate average pitch across all notes"""
    if not data.notes:
        return 0
    return sum(note.pitch for note in data.notes) / len(data.notes)


def calculate_median_pitch(data):
    """Calculate median pitch"""
    if not data.notes:
        return 0
    pitches = sorted(note.pitch for note in data.notes)
    n = len(pitches)
    if n % 2 == 0:
        return (pitches[n//2 - 1] + pitches[n//2]) / 2
    else:
        return pitches[n//2]


def calculate_min_pitch(data):
    """Calculate minimum pitch"""
    if not data.notes:
        return 0
    return min(note.pitch for note in data.notes)


def calculate_max_pitch(data):
    """Calculate maximum pitch"""
    if not data.notes:
        return 0
    return max(note.pitch for note in data.notes)


def calculate_pitch_range(data):
    """Calculate pitch range (max - min)"""
    if not data.notes:
        return 0
    return calculate_max_pitch(data) - calculate_min_pitch(data)


def calculate_average_duration(data):
    """Calculate average note duration in seconds"""
    if not data.notes:
        return 0
    return sum(note.duration for note in data.notes) / len(data.notes)


def calculate_median_duration(data):
    """Calculate median note duration in seconds"""
    if not data.notes:
        return 0
    durations = sorted(note.duration for note in data.notes)
    n = len(durations)
    if n % 2 == 0:
        return (durations[n//2 - 1] + durations[n//2]) / 2
    else:
        return durations[n//2]


def calculate_average_duration_beats(data):
    """Calculate average note duration in beats"""
    if not data.notes:
        return 0
    return sum(note.duration_beats for note in data.notes) / len(data.notes)


def calculate_median_duration_beats(data):
    """Calculate median note duration in beats"""
    if not data.notes:
        return 0
    durations = sorted(note.duration_beats for note in data.notes)
    n = len(durations)
    if n % 2 == 0:
        return (durations[n//2 - 1] + durations[n//2]) / 2
    else:
        return durations[n//2]


def calculate_average_velocity(data):
    """Calculate average note velocity"""
    if not data.notes:
        return 0
    return sum(note.velocity for note in data.notes) / len(data.notes)


def calculate_median_velocity(data):
    """Calculate median note velocity"""
    if not data.notes:
        return 0
    velocities = sorted(note.velocity for note in data.notes)
    n = len(velocities)
    if n % 2 == 0:
        return (velocities[n//2 - 1] + velocities[n//2]) / 2
    else:
        return velocities[n//2]


def calculate_pitch_distribution(data):
    """
    Calculate pitch distribution (count of each pitch)
    Returns dict of pitch -> count
    """
    return dict(Counter(note.pitch for note in data.notes))


def calculate_interval_distribution(data):
    """
    Calculate interval distribution between consecutive notes
    Returns dict of interval -> count
    """
    if len(data.notes) < 2:
        return {}
    
    # Sort notes by start time to get chronological order
    sorted_notes = sorted(data.notes, key=lambda n: n.start)
    
    intervals = []
    for i in range(1, len(sorted_notes)):
        interval = abs(sorted_notes[i].pitch - sorted_notes[i-1].pitch) % 12
        intervals.append(interval)
    
    return dict(Counter(intervals))


def calculate_consonance_coefficient(data):
    """
    Calculate overall consonance coefficient
    Ratio of consonant intervals to total intervals
    """
    if len(data.notes) < 2:
        return 0
    
    # Sort notes by start time
    sorted_notes = sorted(data.notes, key=lambda n: n.start)
    
    consonant_count = 0
    total_intervals = 0
    
    for i in range(1, len(sorted_notes)):
        interval = abs(sorted_notes[i].pitch - sorted_notes[i-1].pitch) % 12
        if is_consonant_interval(interval):
            consonant_count += 1
        total_intervals += 1
    
    return consonant_count / total_intervals if total_intervals > 0 else 0


def calculate_consonance_by_instrument(data):
    """
    Calculate consonance coefficient for each instrument
    Returns dict of instrument_name -> consonance_coefficient
    """
    result = {}
    
    for instrument in data.instruments:
        inst_idx = instrument['index']
        inst_name = instrument['name']
        
        # Get notes for this instrument, sorted by time
        inst_notes = sorted(
            [n for n in data.notes if n.instrument_idx == inst_idx],
            key=lambda n: n.start
        )
        
        if len(inst_notes) < 2:
            result[inst_name] = 0
            continue
        
        consonant_count = 0
        total_intervals = 0
        
        for i in range(1, len(inst_notes)):
            interval = abs(inst_notes[i].pitch - inst_notes[i-1].pitch) % 12
            if is_consonant_interval(interval):
                consonant_count += 1
            total_intervals += 1
        
        result[inst_name] = consonant_count / total_intervals if total_intervals > 0 else 0
    
    return result

def calculate_track_diversity(data):
    """Calculate track diversity score based on repeating patterns"""
    if not data.notes:
        return 0.0
        
    total_notes = len(data.notes)
    if total_notes == 0:
        return 0.0
    if total_notes == 1:
        return 1.0
        
    sorted_notes = sorted(data.notes, key=lambda n: n.start)
    pitches = [n.pitch for n in sorted_notes]
    
    # Find all repeating patterns
    patterns = find_repeating_patterns(pitches)
    
    diversity_score = 1.0
    total_penalty = 0.0
    
    # Apply penalties for single-note repeats
    pitch_counts = Counter(pitches)
    for count in pitch_counts.values():
        if count > 1:
            total_penalty += 0.01 * (count - 1) / total_notes
    
    # Apply penalties for pattern repeats
    for pattern, count, _ in patterns:
        pattern_len = len(pattern)
        if pattern_len >= 2:
            penalty = 1.5 * (pattern_len) * (count - 1) / total_notes
            total_penalty += penalty
    
    diversity_score = max(0.0, diversity_score - total_penalty)
    return round(diversity_score, 4)


# Registry of all statistics functions
# Each function takes MIDIData as input and returns a single value or dict
STATISTICS = [
    ('Total Notes', calculate_total_notes),
    ('Average Pitch', calculate_average_pitch),
    ('Median Pitch', calculate_median_pitch),
    ('Min Pitch', calculate_min_pitch),
    ('Max Pitch', calculate_max_pitch),
    ('Pitch Range', calculate_pitch_range),
    ('Average Duration (seconds)', calculate_average_duration),
    ('Median Duration (seconds)', calculate_median_duration),
    ('Average Duration (beats)', calculate_average_duration_beats),
    ('Median Duration (beats)', calculate_median_duration_beats),
    ('Average Velocity', calculate_average_velocity),
    ('Median Velocity', calculate_median_velocity),
    ('Consonance Coefficient', calculate_consonance_coefficient),
    ('Track Diversity', calculate_track_diversity),
]


def compute_all_statistics(data):
    """
    Compute all registered statistics
    
    Args:
        data: MIDIData object
    
    Returns:
        Dictionary of statistic_name -> value
    """
    results = {}
    
    # Basic statistics
    for name, func in STATISTICS:
        results[name] = func(data)
    
    # Complex statistics that return dicts
    results['Pitch Distribution'] = calculate_pitch_distribution(data)
    results['Interval Distribution'] = calculate_interval_distribution(data)
    results['Consonance by Instrument'] = calculate_consonance_by_instrument(data)
    
    return results
