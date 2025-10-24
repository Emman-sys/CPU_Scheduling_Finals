#!/usr/bin/env python3
"""
Script to convert dynamic algorithm card insertion to static HTML
for all CPU scheduling algorithm pages.
"""

import re

files_to_fix = [
    'srtf.html',
    'priority.html',
    'priority-preemptive.html',
    'hrrn.html',
    'round-robin.html',
    'multilevel.html'
]

for filename in files_to_fix:
    print(f"Processing {filename}...")
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # Find the closing </div> before </div>\n    </div>\n\n    <script>
    # This is where the results card ends
    pattern = r'(</div>\s+</div>\s+</div>\s+</div>\s+)(\s+<script>)'
    
    # Check if algorithm card HTML is already present
    if '<!-- Card 3: Algorithm Explanation -->' in content:
        print(f"  {filename} already has static algorithm card, skipping HTML insertion")
    else:
        print(f"  ERROR: Need to manually add algorithm card HTML to {filename}")
        continue
    
    # Remove the dynamic insertion code
    # Pattern to match the insertAlgorithmCard function
    dynamic_pattern = r'\s*/\*.*?Algorithm.*?displayed for reference.*?\*/\s*\(function insertAlgorithmCard\(\).*?\}\)\(\);\s*'
    
    if re.search(dynamic_pattern, content, re.DOTALL):
        content = re.sub(dynamic_pattern, '\n        ', content, flags=re.DOTALL)
        print(f"  Removed dynamic insertion code from {filename}")
    else:
        print(f"  No dynamic insertion code found in {filename}")
    
    # Write back
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"  ✓ {filename} updated")

print("\nAll files processed!")
