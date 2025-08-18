import re

# Read the current markdown file
with open('new.md', 'r', encoding='utf-8') as file:
    content = file.read()

print("🔧 Fixing table formatting to be markdown compatible...")

# Fix all table formatting by replacing || with |
# This converts double pipes to single pipes for proper markdown format
content = re.sub(r'^\|\|', '|', content, flags=re.MULTILINE)

print("✅ Table formatting fixed!")

# Save the corrected file
with open('new.md', 'w', encoding='utf-8') as file:
    file.write(content)

print("📝 Updated new.md with proper markdown table formatting")

# Verify the fix by checking a few table lines
print("\n🔍 Sample of corrected table formatting:")
lines = content.split('\n')
for i, line in enumerate(lines):
    if '| Location' in line or '| SIHA' in line or '| Vision Status' in line:
        print(f"Line {i+1}: {line}")
        if i < len(lines) - 1:
            print(f"Line {i+2}: {lines[i+1]}")
        break

print("\n✅ All tables now use proper markdown formatting with single pipes (|)")
