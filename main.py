"""
Main entry point for MIDI analysis tool
"""

import sys
import os
from parser import parse_midi_file
from midi_statistics import compute_all_statistics
from output import write_csv_output, print_summary


def main():
    """Main function to orchestrate MIDI analysis"""
    
    # Check if filename is provided
    if len(sys.argv) < 2:
        print("Usage: python main.py <midi_file>")
        print("Example: python main.py file.mid")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # Determine output filename (same name as input with _analysis suffix in output folder)
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_dir, f"{base_name}_analysis.csv")
    
    try:
        print(f"{'-'*60}")
        print(f"Parsing MIDI file: {input_file}")
        
        # Parse MIDI file
        data = parse_midi_file(input_file)
        print(f"Successfully parsed: {len(data.notes)} notes from {len(data.instruments)} instrument(s)")
        
        # Compute statistics
        print("Computing statistics...")
        statistics = compute_all_statistics(data)
        
        # Write output
        print(f"Writing results to: {output_file}")
        write_csv_output(output_file, data, statistics)
        
        # Print summary to console
        print_summary(data, statistics)
        
        print(f"Analysis complete! Results saved to '{output_file}'")
        print(f"{'-'*60}\n")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
