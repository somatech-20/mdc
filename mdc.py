import argparse
import re
import sys

def clean_markdown(text):
    # Remove headers (#, ##, ###, etc.)
    text = re.sub(r'^#{1,6}\s*(.*?)\s*$', r'\1', text, flags=re.MULTILINE)
    
    # Remove bold (**text** or __text__)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    
    # Remove italic (*text* or _text_)
    text = re.sub(r'(?<!\*)(\*|_)(.*?)(?<!\*)(\*|_)(?!\w)', r'\2', text)
    
    # Remove links [text](url) -> text
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    
    # Remove images ![alt](url) -> alt
    text = re.sub(r'!\[(.*?)\]\(.*?\)', r'\1', text)
    
    # Remove inline code (`code`)
    text = re.sub(r'`(.*?)`', r'\1', text)
    
    # Remove code blocks (``` or ~~~)
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'~~~.*?~~~', '', text, flags=re.DOTALL)
    
    # Remove blockquotes (lines starting with >)
    text = re.sub(r'^>\s*(.*)', r'\1', text, flags=re.MULTILINE)
    
    # Remove unordered list items (-, *, +, including nested lists with spaces)
    text = re.sub(r'^(\s*[-*+])\s+(.*)', r'\2', text, flags=re.MULTILINE)
    
    # Remove ordered list items (1., 2., etc., including nested lists with spaces)
    text = re.sub(r'^(\s*\d+\.)\s*(.*)', r'\2', text, flags=re.MULTILINE)
    
    # Remove horizontal rules (---, ***, ___)
    text = re.sub(r'^[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)
    
    # Remove strikethrough (~~text~~)
    text = re.sub(r'~~(.*?)~~', r'\1', text)
    
    # Remove tables (| col | col | etc.)
    text = re.sub(r'^\|.*\|\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*[-:|\s]+\s*$', '', text, flags=re.MULTILINE)
    
    # Remove escaped characters (e.g., \*, \#)
    text = re.sub(r'\\([*#_|])', r'\1', text)
    
    # Try handling stray asterisks (e.g., * *text.*)
    text = re.sub(r'^\s*\*\s*(.*?)\s*\*(?=\s|$)', r'\1', text, flags=re.MULTILINE)

    # Remove extra blank lines
    text = re.sub(r'\n\s*\n', '\n', text)
    
    # Strip leading/trailing whitespace
    return text.strip()

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown file to plain text")
    parser.add_argument('input_file', help="Input Markdown file")
    parser.add_argument('output_file', nargs='?', help="Output text file (optional, defaults to stdout)")
    
    args = parser.parse_args()
    
    try:
        # Read input file
        with open(args.input_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
        
        # Clean the Markdown
        cleaned_text = clean_markdown(markdown_text)
        
        # Write output
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)
        else:
            sys.stdout.write(cleaned_text + '\n')
            
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
