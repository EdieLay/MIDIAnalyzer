"""
CSV output formatting and generation
"""

import csv


def write_csv_output(filepath, data, statistics):
    """
    Write analysis results to CSV file
    
    Format:
    1. General statistics section
    2. Blank line separator
    3. Individual notes section
    
    Args:
        filepath: Output CSV file path
        data: MIDIData object
        statistics: Dictionary of computed statistics
    """
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        
        # Write header
        writer.writerow(['MIDI ANALYSIS RESULTS'])
        writer.writerow([])
        
        # Write file information
        writer.writerow(['FILE INFORMATION'])
        writer.writerow(['Tempo (BPM)', f"{data.tempo:.2f}"])
        writer.writerow(['Time Signature', f"'{data.time_signature}"])  # Prefix with ' to prevent Excel date formatting
        writer.writerow(['Total Duration (seconds)', f"{data.total_duration:.3f}"])
        writer.writerow(['Number of Instruments', len(data.instruments)])
        writer.writerow([])
        
        # Write instrument information
        writer.writerow(['INSTRUMENTS'])
        writer.writerow(['Index', 'Name', 'Program', 'Is Drum', 'Note Count'])
        for inst in data.instruments:
            writer.writerow([
                inst['index'],
                inst['name'],
                inst['program'],
                'Yes' if inst['is_drum'] else 'No',
                inst['note_count']
            ])
        writer.writerow([])
        
        # Write general statistics
        writer.writerow(['GENERAL STATISTICS'])
        writer.writerow(['Statistic', 'Value'])
        
        for name, value in statistics.items():
            if isinstance(value, dict):
                # Skip dict statistics for now, we'll handle them separately
                continue
            elif isinstance(value, float):
                writer.writerow([name, f"{value:.4f}"])
            else:
                writer.writerow([name, value])
        
        writer.writerow([])
        
        # Write pitch distribution
        writer.writerow(['PITCH DISTRIBUTION'])
        writer.writerow(['Pitch', 'Count'])
        pitch_dist = statistics.get('Pitch Distribution', {})
        for pitch in sorted(pitch_dist.keys()):
            writer.writerow([pitch, pitch_dist[pitch]])
        writer.writerow([])
        
        # Write interval distribution
        writer.writerow(['INTERVAL DISTRIBUTION (semitones mod 12)'])
        writer.writerow(['Interval', 'Count'])
        interval_dist = statistics.get('Interval Distribution', {})
        for interval in sorted(interval_dist.keys()):
            writer.writerow([interval, interval_dist[interval]])
        writer.writerow([])
        
        # Write consonance by instrument
        writer.writerow(['CONSONANCE BY INSTRUMENT'])
        writer.writerow(['Instrument', 'Consonance Coefficient'])
        cons_by_inst = statistics.get('Consonance by Instrument', {})
        for inst_name, coef in cons_by_inst.items():
            writer.writerow([inst_name, f"{coef:.4f}"])
        writer.writerow([])
        
        # Write individual notes
        writer.writerow(['INDIVIDUAL NOTES'])
        writer.writerow([
            'Instrument Index',
            'Instrument Name',
            'Pitch Number',
            'Pitch Name',
            'Start (seconds)',
            'End (seconds)',
            'Duration (seconds)',
            'Start (beats)',
            'End (beats)',
            'Duration (beats)',
            'Note Length',
            'Velocity'
        ])
        
        # Sort notes by start time
        sorted_notes = sorted(data.notes, key=lambda n: n.start)
        
        for note in sorted_notes:
            writer.writerow([
                note.instrument_idx,
                note.instrument_name,
                note.pitch,
                note.pitch_name,
                f"{note.start:.3f}",
                f"{note.end:.3f}",
                f"{note.duration:.3f}",
                f"{note.start_beats:.3f}",
                f"{note.end_beats:.3f}",
                f"{note.duration_beats:.3f}",
                note.note_length,
                note.velocity
            ])


def print_summary(data, statistics):
    """
    Print a brief summary to console
    
    Args:
        data: MIDIData object
        statistics: Dictionary of computed statistics
    """
    print(f"\n{'='*60}")
    print(f"MIDI Analysis Summary")
    print(f"{'='*60}")
    print(f"Tempo: {data.tempo:.2f} BPM")
    print(f"Time Signature: {data.time_signature}")
    print(f"Total Duration: {data.total_duration:.2f} seconds")
    print(f"Number of Instruments: {len(data.instruments)}")
    print(f"Total Notes: {statistics['Total Notes']}")
    print(f"\nPitch Statistics:")
    print(f"  Average: {statistics['Average Pitch']:.2f}")
    print(f"  Median: {statistics['Median Pitch']:.2f}")
    print(f"  Range: {statistics['Min Pitch']}-{statistics['Max Pitch']} (span: {statistics['Pitch Range']})")
    print(f"\nDuration Statistics:")
    print(f"  Average: {statistics['Average Duration (seconds)']:.3f} seconds ({statistics['Average Duration (beats)']:.3f} beats)")
    print(f"  Median: {statistics['Median Duration (seconds)']:.3f} seconds ({statistics['Median Duration (beats)']:.3f} beats)")
    print(f"\nConsonance Coefficient: {statistics['Consonance Coefficient']:.4f}")
    print(f"\nDiversity score: {statistics['Track Diversity']:.4f}")
    print(f"{'='*60}\n")
