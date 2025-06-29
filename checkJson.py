import json
import sys
import re

def check_json_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # First, try to parse the JSON
        try:
            json.loads(content)
            print("✅ JSON is valid.")
            return
        except json.JSONDecodeError as e:
            print("❌ JSON is invalid!")
            print(f"Error: {e.msg}")
            print(f"Line: {e.lineno}, Column: {e.colno}")
            
            # Get the lines of the file
            lines = content.splitlines()
            
            if 1 <= e.lineno <= len(lines):
                problematic_line = lines[e.lineno - 1]
                print(f"Problematic line: {problematic_line}")
                
                # Highlight the error position
                if e.colno > 0:
                    pointer = ' ' * (e.colno - 1) + '^'
                    print(f"Error position:   {pointer}")
                
                # Additional analysis for common issues
                analyze_common_issues(lines, e.lineno - 1, e.colno)
            else:
                print("Could not determine the problematic line.")
    
    except FileNotFoundError:
        print(f"❌ Error: File '{filepath}' not found.")
    except Exception as e:
        print(f"❌ Error reading file: {e}")

def analyze_common_issues(lines, line_index, col_index):
    """Analyze common JSON syntax issues"""
    if line_index < 0 or line_index >= len(lines):
        return
    
    current_line = lines[line_index]
    
    print("\n🔍 Additional Analysis:")
    
    # Check for invalid characters at the beginning of lines
    invalid_chars = re.findall(r'^[\s]*[+\-*/@#$%^&()=<>!]', current_line)
    if invalid_chars:
        print(f"   • Found invalid character '{invalid_chars[0].strip()}' at the beginning of the line")
        print("   • This character is not valid in JSON format")
    
    # Check for missing quotes around property names
    unquoted_props = re.findall(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', current_line)
    if unquoted_props:
        print(f"   • Property name '{unquoted_props[0]}' should be quoted: \"{unquoted_props[0]}\"")
    
    # Check for trailing commas
    if re.search(r',\s*[}\]]', current_line):
        print("   • Found trailing comma before closing bracket/brace")
    
    # Check for missing commas
    if line_index < len(lines) - 1:
        next_line = lines[line_index + 1].strip()
        if (current_line.strip().endswith('}') or current_line.strip().endswith(']') or 
            current_line.strip().endswith('"') or current_line.strip().endswith('true') or
            current_line.strip().endswith('false') or current_line.strip().endswith('null') or
            re.search(r'\d$', current_line.strip())):
            if next_line.startswith('"') or next_line.startswith('{') or next_line.startswith('['):
                if not current_line.strip().endswith(','):
                    print("   • Missing comma at the end of this line")
    
    # Check for single quotes instead of double quotes
    if "'" in current_line:
        print("   • JSON requires double quotes (\"), not single quotes (')")
    
    # Check for comments (not allowed in JSON)
    if '//' in current_line or '/*' in current_line:
        print("   • Comments are not allowed in JSON format")
    
    # Suggest fixes for common issues
    print("\n💡 Suggested fixes:")
    
    # Fix for the + sign issue
    if '+' in current_line and not current_line.strip().startswith('"'):
        fixed_line = re.sub(r'^\s*\+\s*', '', current_line)
        print(f"   • Remove the '+' character:")
        print(f"     Before: {current_line}")
        print(f"     After:  {fixed_line}")
    
    # Fix for unquoted property names
    if unquoted_props:
        fixed_line = re.sub(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'"\1":', current_line)
        print(f"   • Quote the property name:")
        print(f"     Before: {current_line}")
        print(f"     After:  {fixed_line}")

def validate_json_structure(filepath):
    """Additional validation for JSON structure"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"\n📊 File Analysis:")
        print(f"   • Total lines: {len(lines)}")
        
        bracket_stack = []
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            for char in line:
                if char in '{[':
                    bracket_stack.append((char, i))
                elif char in '}]':
                    if not bracket_stack:
                        print(f"   • Unmatched closing bracket '{char}' at line {i}")
                        return False
                    opening, _ = bracket_stack.pop()
                    if (char == '}' and opening != '{') or (char == ']' and opening != '['):
                        print(f"   • Mismatched brackets at line {i}")
                        return False
        
        if bracket_stack:
            unclosed = bracket_stack[-1]
            print(f"   • Unclosed bracket '{unclosed[0]}' from line {unclosed[1]}")
            return False
        
        print("   • Bracket structure appears correct")
        return True
        
    except Exception as e:
        print(f"   • Could not analyze structure: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python checkJson.py <json_file>")
        print("Example: python checkJson.py test.json")
    else:
        filepath = sys.argv[1]
        print(f"🔍 Checking JSON file: {filepath}")
        print("=" * 40)
        
        check_json_file(filepath)
        validate_json_structure(filepath)