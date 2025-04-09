#text_extractor.py

import os
import fitz

class TextExtractor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.text = None
        self.__extract_text()

    def __extract_text(self):
        """Extracts text from the PDF file."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"The file {self.file_path} does not exist.")

        with fitz.open(self.file_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            self.text = text

    def write_to_path(self, file_path: str):
        """Write the extracted text to the specified file path."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.text)
        print(f"Text written to {file_path}")

    def to_lower(self):
        """Converts the extracted text to lowercase."""
        self.text = self.text.lower()

    def to_upper(self):
        """Converts the extracted text to uppercase."""
        self.text = self.text.upper()

    def append_front(self, txt: str):
        """Prepends the provided text to the extracted text."""
        self.text = txt + self.text

    def append_back(self, txt: str):
        """Appends the provided text to the extracted text."""
        self.text = self.text + txt

    def __getitem__(self, index: int) -> str:
        """Return the character at the given index in the extracted text."""
        try:
            return self.text[index]
        except IndexError:
            raise IndexError("Index out of range")

    def __str__(self):
        return self.text


def debug():
    sample_pdf_path = "sample.pdf"
    
    if not os.path.exists(sample_pdf_path):
        print(f"Sample PDF file '{sample_pdf_path}' not found. Please provide a valid PDF file for debugging.")
        return

    # Instantiate the TextExtractor and extract text from the PDF
    extractor = TextExtractor(sample_pdf_path)
    
    # Print a snippet of the extracted text
    print("Extracted Text (first 500 characters):")
    print(extractor.text[:500])
    print("\n")

    # Demonstrate __getitem__ by printing the character at a specific index
    try:
        index_to_test = 10  
        print(f"Character at index {index_to_test}: {extractor[index_to_test]}")
    except IndexError as e:
        print(e)

    # Manipulate text: convert to uppercase and append text
    extractor.to_upper()
    print("\nText after converting to uppercase (first 500 characters):")
    print(extractor.text[:500])
    
    # Append text to the front and back
    extractor.append_front("=== START OF DOCUMENT ===\n")
    extractor.append_back("\n=== END OF DOCUMENT ===")
    
    # Write the manipulated text to an output file
    output_file = "debug_output.txt"
    extractor.write_to_path(output_file)
    print(f"Debug complete. Check '{output_file}' for the full manipulated text.")


if __name__ == '__main__':
    debug()
