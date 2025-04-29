"""
input_handler.py - Enhanced module for reading and processing input data files

This module provides functions to read data from Excel and CSV files with multiple
options for file selection, validates file existence and format, and prepares 
the data for further processing.
"""

import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import argparse
from typing import Optional, Union, Dict, List, Tuple


class InputHandler:
    """
    A class to handle data input from Excel and CSV files with multiple
    input methods for file selection.
    """
    
    def __init__(self):
        """Initialize the InputHandler class."""
        self.supported_extensions = ['.csv', '.xlsx', '.xls']
        self.loaded_files = {}  # Dictionary to store loaded DataFrames
    
    def validate_file(self, file_path: str) -> bool:
        """
        Validate if the file exists and has a supported extension.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            bool: True if file is valid, False otherwise
        """
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            return False
        
        # Check if file has a supported extension
        _, extension = os.path.splitext(file_path)
        if extension.lower() not in self.supported_extensions:
            print(f"Error: Unsupported file format '{extension}'. Supported formats are: {', '.join(self.supported_extensions)}")
            return False
            
        return True
    
    def read_file(self, file_path: str, sheet_name: Optional[Union[str, int, List[Union[int, str]]]] = 0,
                  **kwargs) -> Optional[pd.DataFrame]:
        """
        Read data from a file into a pandas DataFrame.
        
        Args:
            file_path (str): Path to the file
            sheet_name: Sheet name or index for Excel files (default: 0)
            **kwargs: Additional arguments to pass to pandas read functions
            
        Returns:
            Optional[pd.DataFrame]: DataFrame containing the data, or None if reading failed
        """
        if not self.validate_file(file_path):
            return None
            
        try:
            _, extension = os.path.splitext(file_path)
            
            if extension.lower() in ['.xlsx', '.xls']:
                data = pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
                print(f"Successfully read Excel file: {file_path}")
            elif extension.lower() == '.csv':
                data = pd.read_csv(file_path, **kwargs)
                print(f"Successfully read CSV file: {file_path}")
            else:
                # This shouldn't happen due to validate_file, but just in case
                print(f"Unsupported file format: {extension}")
                return None
                
            # Store the DataFrame with the file_path as key
            self.loaded_files[file_path] = data
            return data
            
        except Exception as e:
            print(f"Error reading file '{file_path}': {str(e)}")
            return None
    
    def select_file_gui(self, title: str = "Select a data file", 
                      filetypes: List[Tuple[str, str]] = None) -> Optional[str]:
        """
        Open a file dialog for the user to select a file.
        
        Args:
            title (str): Title of the file dialog
            filetypes (List[Tuple[str, str]]): List of file types to show
            
        Returns:
            Optional[str]: Selected file path or None if canceled
        """
        # Hide the main tkinter window
        root = tk.Tk()
        root.withdraw()
        
        # Set default filetypes if not provided
        if filetypes is None:
            filetypes = [
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx;*.xls"),
                ("All files", "*.*")
            ]
        
        # Open the file dialog
        file_path = filedialog.askopenfilename(
            title=title,
            filetypes=filetypes
        )
        
        # Destroy the tkinter instance
        root.destroy()
        
        if file_path:
            return file_path
        return None
    
    def read_file_gui(self, **kwargs) -> Optional[pd.DataFrame]:
        """
        Open a file dialog and read the selected file.
        
        Args:
            **kwargs: Additional arguments to pass to the read_file function
            
        Returns:
            Optional[pd.DataFrame]: DataFrame containing the data, or None if reading failed or canceled
        """
        file_path = self.select_file_gui()
        if file_path:
            return self.read_file(file_path, **kwargs)
        return None
    
    def select_files_gui(self, title: str = "Select data files", 
                       filetypes: List[Tuple[str, str]] = None) -> List[str]:
        """
        Open a file dialog for the user to select multiple files.
        
        Args:
            title (str): Title of the file dialog
            filetypes (List[Tuple[str, str]]): List of file types to show
            
        Returns:
            List[str]: List of selected file paths (empty if canceled)
        """
        # Hide the main tkinter window
        root = tk.Tk()
        root.withdraw()
        
        # Set default filetypes if not provided
        if filetypes is None:
            filetypes = [
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx;*.xls"),
                ("All files", "*.*")
            ]
        
        # Open the file dialog
        file_paths = filedialog.askopenfilenames(
            title=title,
            filetypes=filetypes
        )
        
        # Destroy the tkinter instance
        root.destroy()
        
        return list(file_paths)  # Convert tuple to list
    
    def read_multiple_files_gui(self, **kwargs) -> Dict[str, pd.DataFrame]:
        """
        Open a file dialog to select multiple files and read them.
        
        Args:
            **kwargs: Additional arguments to pass to the read_file function
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary with file paths as keys and DataFrames as values
        """
        file_paths = self.select_files_gui()
        return self.read_multiple_files(file_paths, **kwargs)
    
    def prompt_for_file_path(self) -> Optional[str]:
        """
        Prompt the user to enter a file path.
        
        Returns:
            Optional[str]: File path entered by the user, or None if empty
        """
        file_path = input("Enter the path to the data file: ").strip()
        if file_path:
            return file_path
        return None
    
    def read_file_prompt(self, **kwargs) -> Optional[pd.DataFrame]:
        """
        Prompt the user for a file path and read the file.
        
        Args:
            **kwargs: Additional arguments to pass to the read_file function
            
        Returns:
            Optional[pd.DataFrame]: DataFrame containing the data, or None if reading failed or empty path
        """
        file_path = self.prompt_for_file_path()
        if file_path:
            return self.read_file(file_path, **kwargs)
        return None
    
    def read_multiple_files(self, file_paths: List[str], **kwargs) -> Dict[str, pd.DataFrame]:
        """
        Read multiple files into a dictionary of DataFrames.
        
        Args:
            file_paths (List[str]): List of file paths
            **kwargs: Additional arguments to pass to the read_file function
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary with file paths as keys and DataFrames as values
        """
        results = {}
        for file_path in file_paths:
            df = self.read_file(file_path, **kwargs)
            if df is not None:
                results[file_path] = df
        return results
    
    def get_file_info(self, file_path: str) -> Dict:
        """
        Get information about a loaded file.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            Dict: Dictionary containing information about the file
        """
        if file_path not in self.loaded_files:
            print(f"File '{file_path}' not loaded. Please load it first using read_file().")
            return {}
            
        df = self.loaded_files[file_path]
        
        # Get file information
        info = {
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'file_size': os.path.getsize(file_path),
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict()
        }
        
        return info
    
    def get_loaded_files(self) -> List[str]:
        """
        Get a list of currently loaded files.
        
        Returns:
            List[str]: List of file paths that have been loaded
        """
        return list(self.loaded_files.keys())
    
    def get_dataframe(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        Get a loaded DataFrame by file path.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            Optional[pd.DataFrame]: DataFrame if loaded, None otherwise
        """
        return self.loaded_files.get(file_path)
    
    def preview_data(self, file_path: str, rows: int = 5) -> Optional[pd.DataFrame]:
        """
        Preview the first few rows of a loaded DataFrame.
        
        Args:
            file_path (str): Path to the file
            rows (int): Number of rows to preview (default: 5)
            
        Returns:
            Optional[pd.DataFrame]: Preview DataFrame if loaded, None otherwise
        """
        df = self.get_dataframe(file_path)
        if df is not None:
            return df.head(rows)
        return None
    
    def sample_data(self, file_path: str, n: int = 5, random_state: int = 42) -> Optional[pd.DataFrame]:
        """
        Get a random sample of rows from a loaded DataFrame.
        
        Args:
            file_path (str): Path to the file
            n (int): Number of rows to sample (default: 5)
            random_state (int): Random seed for reproducibility (default: 42)
            
        Returns:
            Optional[pd.DataFrame]: Sampled DataFrame if loaded, None otherwise
        """
        df = self.get_dataframe(file_path)
        if df is not None:
            return df.sample(n=min(n, len(df)), random_state=random_state)
        return None
    
    def merge_files(self, file_paths: List[str], merge_on: str, 
                   how: str = 'inner') -> Optional[pd.DataFrame]:
        """
        Merge multiple loaded files on a common column.
        
        Args:
            file_paths (List[str]): List of file paths to merge
            merge_on (str): Column name to merge on
            how (str): Type of merge to perform ('inner', 'outer', 'left', 'right')
            
        Returns:
            Optional[pd.DataFrame]: Merged DataFrame, or None if merge failed
        """
        if len(file_paths) < 2:
            print("Error: At least two files are required for merging.")
            return None
            
        # Check if all files are loaded
        for file_path in file_paths:
            if file_path not in self.loaded_files:
                print(f"Error: File '{file_path}' not loaded. Please load it first using read_file().")
                return None
        
        # Start with the first DataFrame
        result = self.loaded_files[file_paths[0]].copy()
        
        # Merge with the rest of the DataFrames
        for i in range(1, len(file_paths)):
            try:
                result = pd.merge(result, self.loaded_files[file_paths[i]], 
                                 on=merge_on, how=how)
            except Exception as e:
                print(f"Error merging files: {str(e)}")
                return None
                
        return result
    
    def concat_files(self, file_paths: List[str], axis: int = 0) -> Optional[pd.DataFrame]:
        """
        Concatenate multiple loaded files.
        
        Args:
            file_paths (List[str]): List of file paths to concatenate
            axis (int): Axis along which to concatenate (0 for rows, 1 for columns)
            
        Returns:
            Optional[pd.DataFrame]: Concatenated DataFrame, or None if concatenation failed
        """
        if len(file_paths) < 2:
            print("Error: At least two files are required for concatenation.")
            return None
            
        # Check if all files are loaded
        dfs = []
        for file_path in file_paths:
            if file_path not in self.loaded_files:
                print(f"Error: File '{file_path}' not loaded. Please load it first using read_file().")
                return None
            dfs.append(self.loaded_files[file_path])
        
        try:
            result = pd.concat(dfs, axis=axis)
            return result
        except Exception as e:
            print(f"Error concatenating files: {str(e)}")
            return None


def parse_command_line_args():
    """
    Parse command line arguments for file input.
    
    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(description="Process data files")
    parser.add_argument("--file", "-f", help="Path to input file")
    parser.add_argument("--files", "-m", nargs="+", help="Paths to multiple input files")
    parser.add_argument("--gui", "-g", action="store_true", help="Use GUI to select file(s)")
    parser.add_argument("--sheet", "-s", default=0, help="Sheet name/index for Excel files")
    parser.add_argument("--output", "-o", help="Output file path")
    
    return parser.parse_args()


# Example usage with different input methods:
if __name__ == "__main__":
    # Create an instance of InputHandler
    handler = InputHandler()
    
    # Parse command line arguments
    args = parse_command_line_args()
    
    # Example 1: Read file from command line argument
    if args.file:
        df = handler.read_file(args.file, sheet_name=args.sheet)
        if df is not None:
            print(f"File loaded successfully. Preview:")
            print(df.head())
        
    # Example 2: Read multiple files from command line arguments
    elif args.files:
        dfs = handler.read_multiple_files(args.files)
        print(f"Loaded {len(dfs)} files successfully.")
        
    # Example 3: Use GUI to select files if specified or no files provided
    elif args.gui:
        print("Opening file selection dialog...")
        df = handler.read_file_gui()
        if df is not None:
            print(f"File loaded successfully. Preview:")
            print(df.head())
            
    # Example 4: Prompt user for file path if no other method specified
    else:
        print("No input method specified. Using interactive prompt.")
        df = handler.read_file_prompt()
        if df is not None:
            print(f"File loaded successfully. Preview:")
            print(df.head())
