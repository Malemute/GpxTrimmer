#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
from typing import Optional

import gpxpy
import gpxpy.gpx
from geopy.distance import geodesic
from tqdm import tqdm

from utils import calculate_speed, format_speed
from validators import validate_gpx_file, validate_speed_threshold

class GPXCleaner:
    def __init__(self, speed_threshold: float):
        """
        Initialize GPX cleaner with speed threshold in km/h
        """
        self.speed_threshold = speed_threshold
        self.stats = {
            'total_points': 0,
            'filtered_points': 0
        }

    def process_file(self, input_path: Path, output_path: Path) -> None:
        """
        Process GPX file and save corrected version
        """
        # Parse input file
        with open(input_path, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                valid_points = self._filter_segment(segment.points)
                # Replace original points with filtered ones
                segment.points = valid_points

        # Save corrected file
        with open(output_path, 'w') as output_file:
            output_file.write(gpx.to_xml())

    def _filter_segment(self, points):
        """
        Filter segment points based on speed threshold
        """
        self.stats['total_points'] = len(points)
        valid_points = []
        
        if len(points) < 2:
            return points

        # Always keep first point
        valid_points.append(points[0])
        
        for i in tqdm(range(1, len(points)), desc="Processing points"):
            prev_point = valid_points[-1]
            current_point = points[i]
            
            # Calculate speed between points
            speed = calculate_speed(
                prev_point.latitude,
                prev_point.longitude,
                current_point.latitude,
                current_point.longitude,
                prev_point.time,
                current_point.time
            )
            
            # If speed is below threshold, keep the point
            if speed <= self.speed_threshold:
                valid_points.append(current_point)
            else:
                self.stats['filtered_points'] += 1
                
        return valid_points

    def print_stats(self):
        """
        Print processing statistics
        """
        print("\nProcessing Statistics:")
        print(f"Total points processed: {self.stats['total_points']}")
        print(f"Points filtered out: {self.stats['filtered_points']}")
        print(f"Remaining points: {self.stats['total_points'] - self.stats['filtered_points']}")
        
def main():
    parser = argparse.ArgumentParser(
        description="Clean GPX files by removing points with unrealistic speeds"
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Input GPX file path"
    )
    parser.add_argument(
        "output_file",
        type=str,
        help="Output GPX file path"
    )
    parser.add_argument(
        "--speed-threshold",
        type=float,
        default=25.0,
        help="Speed threshold in km/h (default: 25.0)"
    )

    args = parser.parse_args()

    # Validate input parameters
    try:
        input_path = Path(args.input_file)
        output_path = Path(args.output_file)
        
        validate_gpx_file(input_path)
        validate_speed_threshold(args.speed_threshold)
        
        # Process the file
        cleaner = GPXCleaner(args.speed_threshold)
        cleaner.process_file(input_path, output_path)
        cleaner.print_stats()
        
        print(f"\nCleaned GPX file saved to: {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
