# MIDI Parser and Statistical Analysis Tool

A modular Python tool for parsing MIDI files and computing comprehensive statistical analyses. The tool is designed to be easily extensible, allowing you to add new analysis methods with minimal effort.

## Features

- **Comprehensive MIDI Parsing**: Extracts all note information including pitch, timing, velocity, and instrument details
- **Rich Statistical Analysis**: Calculates various statistics including:
  - Note count, pitch distribution
  - Average/median/min/max pitch
  - Average/median note duration (in seconds and beats)
  - Average/median velocity
  - Interval distribution
  - Consonance coefficients (overall and per-instrument)
- **Modular Architecture**: Clean separation of concerns with dedicated modules for parsing, analysis, and output
- **Easy Extensibility**: Simple mechanism to add new statistical analyses
- **Detailed CSV Output**: All statistics and individual note data in a single, well-structured CSV file

## Installation

Ensure you have Python 3.6+ installed, then install the required dependency:

```bash
pip install pretty_midi
```

## Usage

Run the tool from the command line:

```bash
python main.py <path_to_midi_file>
```

Example:
```bash
python main.py file.mid
```

The tool will:
1. Create an `output` folder if it doesn't exist
2. Parse the MIDI file
3. Compute all statistics
4. Generate a CSV file named `output/<filename>_analysis.csv`
5. Display a summary in the console

## Project Structure

```
midi_parser/
├── main.py              # Entry point and CLI interface
├── parser.py            # MIDI file parsing
├── midi_statistics.py   # Statistical analysis functions
├── utils.py             # Helper utilities
├── output.py            # CSV output generation
└── README.md            # This file
```

## Adding New Statistical Analyses

The tool is designed to make adding new statistics straightforward. Here's how:

### 1. Add a New Statistic Function

Open `midi_statistics.py` and add your function. Each function should:
- Take a `MIDIData` object as input
- Return a single value (number, string, or dict)

Example:
```python
def calculate_your_new_statistic(data):
    """
    Description of what this calculates
    """
    if not data.notes:
        return 0
    
    # Your calculation logic here
    result = sum(note.pitch for note in data.notes) / len(data.notes)
    
    return result
```

### 2. Register the Function

Add your function to the `STATISTICS` list in `midi_statistics.py`:

```python
STATISTICS = [
    ('Total Notes', calculate_total_notes),
    ('Average Pitch', calculate_average_pitch),
    # ... existing statistics ...
    ('Your New Statistic', calculate_your_new_statistic),  # Add here
]
```

That's it! Your new statistic will automatically be:
- Computed during analysis
- Included in the CSV output
- Displayed in the console summary (if it's a simple value)

### Available Data Structures

When writing your analysis function, you have access to:

**MIDIData object attributes:**
- `data.tempo` - Tempo in BPM
- `data.time_signature` - Time signature (e.g., "4/4")
- `data.total_duration` - Total duration in seconds
- `data.instruments` - List of instrument dictionaries
- `data.notes` - List of NoteData objects

**NoteData object attributes (for each note):**
- `note.instrument_idx` - Instrument index
- `note.instrument_name` - Instrument name
- `note.pitch` - MIDI pitch number (0-127)
- `note.pitch_name` - Note name (e.g., "C4", "A#5")
- `note.start` - Start time in seconds
- `note.end` - End time in seconds
- `note.duration` - Duration in seconds
- `note.start_beats` - Start time in beats
- `note.end_beats` - End time in beats
- `note.duration_beats` - Duration in beats
- `note.note_length` - Fractional note length (e.g., "0.25")
- `note.velocity` - MIDI velocity (0-127)

### Examples of Custom Statistics

**Example 1: Calculate average pitch for a specific instrument**
```python
def calculate_piano_average_pitch(data):
    """Calculate average pitch for piano instrument"""
    piano_notes = [n for n in data.notes if 'Piano' in n.instrument_name]
    if not piano_notes:
        return 0
    return sum(n.pitch for n in piano_notes) / len(piano_notes)
```

**Example 2: Count notes in a specific pitch range**
```python
def calculate_high_notes_count(data):
    """Count notes above C5 (pitch 72)"""
    return sum(1 for n in data.notes if n.pitch > 72)
```

**Example 3: Calculate timing variance**
```python
def calculate_duration_variance(data):
    """Calculate variance in note durations"""
    if len(data.notes) < 2:
        return 0
    
    durations = [n.duration for n in data.notes]
    mean = sum(durations) / len(durations)
    variance = sum((d - mean) ** 2 for d in durations) / len(durations)
    
    return variance
```

## CSV Output Format

The generated CSV file contains:

1. **File Information**: Tempo, time signature, duration, instrument count
2. **Instrument Details**: Index, name, program number, drum flag, note count
3. **General Statistics**: All computed statistics
4. **Pitch Distribution**: Count of each pitch used
5. **Interval Distribution**: Count of each interval type
6. **Consonance by Instrument**: Consonance coefficient for each instrument
7. **Individual Notes**: Complete data for every note

All sections are clearly labeled and separated for easy analysis.

## Notes

- The tool uses the `pretty_midi` library for MIDI parsing
- Consonance is determined by interval type (minor 2nd, major 2nd, tritone, minor 7th, and major 7th are considered dissonant)
- All timing information is provided in both seconds and beats
- The CSV delimiter is semicolon (`;`) to accommodate commas in data

## Future Enhancement Ideas

Some ideas for additional statistics you might want to implement:
- Note density over time
- Chord identification and progression analysis
- Rhythm pattern detection
- Harmonic analysis
- Melodic contour analysis
- Polyphony analysis (number of simultaneous notes)
- Dynamic range analysis (velocity patterns)
- Tempo variation detection

## License

This project is open source and available for educational and research purposes.
