#!/usr/bin/env python3
import re

# Algorithm card content for each file
cards = {
    'priority.html': {
        'title': 'Priority Scheduling Algorithm (Non-preemptive)',
        'desc': 'Priority Scheduling (non-preemptive) - select the available process with the highest priority (lowest priority number).',
        'code': '''/* Priority (Non-preemptive) pseudocode */
function calculatePriority(processes) {
  let pending = processes.slice();
  let currentTime = 0;
  let completed = [];
  let gantt = [];

  while (pending.length > 0) {
    // find available processes
    let available = pending.filter(p => p.at <= currentTime);

    if (available.length === 0) {
      currentTime = Math.min(...pending.map(p => p.at));
      continue;
    }

    // pick highest priority (lowest number)
    available.sort((a,b) => a.priority - b.priority);
    let p = available[0];

    // execute to completion
    const start = currentTime;
    currentTime += p.bt;
    p.ct = currentTime;
    p.tat = p.ct - p.at;
    p.wt = p.tat - p.bt;
    gantt.push({ pid: p.pid, start, end: currentTime });

    pending.splice(pending.indexOf(p), 1);
    completed.push(p);
  }

  return { results: completed, gantt };
}'''
    },
    'priority-preemptive.html': {
        'title': 'Priority Scheduling Algorithm (Preemptive)',
        'desc': 'Priority Scheduling (preemptive) - at each time unit, select the available process with the highest priority.',
        'code': '''/* Priority (Preemptive) pseudocode */
function calculatePriorityPreemptive(processes) {
  let proc = processes.map(p => ({...p, remainingTime: p.bt}));
  let currentTime = 0;
  let completed = 0;
  let results = [];
  let gantt = [];

  while (completed < proc.length) {
    let available = proc.filter(p => p.at <= currentTime && p.remainingTime > 0);

    if (available.length === 0) {
      currentTime++;
      continue;
    }

    // pick highest priority (lowest number)
    available.sort((a,b) => a.priority - b.priority);
    let p = available[0];

    const start = currentTime;
    p.remainingTime--;
    currentTime++;

    // merge consecutive Gantt blocks
    if (gantt.length > 0 && gantt[gantt.length - 1].pid === p.pid) {
      gantt[gantt.length - 1].end = currentTime;
    } else {
      gantt.push({ pid: p.pid, start, end: currentTime });
    }

    if (p.remainingTime === 0) {
      completed++;
      results.push({ ...p, ct: currentTime, tat: currentTime - p.at, wt: currentTime - p.at - p.bt });
    }
  }

  return { results, gantt };
}'''
    }
}

def add_static_card(filename, card_info):
    """Add static algorithm card HTML before the <script> tag"""
    with open(filename, 'r') as f:
        content = f.read()
    
    # Check if already has static card
    if '<!-- Card 3: Algorithm Explanation -->' in content:
        print(f"  {filename} already has static card")
        return False
    
    # Find the closing divs before <script>
    pattern = r'(</div>\s+</div>\s+</div>)(\s+<script>)'
    
    card_html = f'''</div>
        </div>

        <!-- Card 3: Algorithm Explanation -->
        <div class="bg-white/90 backdrop-blur-sm rounded-lg shadow-lg p-6 mb-6">
            <h2 class="text-2xl font-bold mb-4">{card_info['title']}</h2>
            <p class="text-sm text-gray-700 mb-3">{card_info['desc']}</p>
            <pre class="whitespace-pre-wrap bg-gray-100 p-4 rounded text-sm overflow-auto"><code>{card_info['code']}</code></pre>
        </div>
    </div>

    <script>'''
    
    replacement = r'\1' + '\n' + card_html.replace('\\', r'\\')
    new_content = re.sub(pattern, card_html, content, count=1)
    
    if new_content == content:
        print(f"  ERROR: Could not find insertion point in {filename}")
        return False
    
    with open(filename, 'w') as f:
        f.write(new_content)
    
    print(f"  ✓ Added static card to {filename}")
    return True

def remove_dynamic_insertion(filename):
    """Remove the dynamic insertAlgorithmCard function"""
    with open(filename, 'r') as f:
        content = f.read()
    
    # Pattern to match the entire dynamic insertion block
    pattern = r'\s*/\*[^*]*Algorithm[^*]*\*/\s*\(function insertAlgorithmCard\(\)[^}]*\{[^}]*\}[^}]*\}\)\(\);\s*'
    
    new_content = re.sub(pattern, '\n        ', content, flags=re.DOTALL)
    
    if new_content == content:
        print(f"  No dynamic insertion found in {filename}")
        return False
    
    with open(filename, 'w') as f:
        f.write(new_content)
    
    print(f"  ✓ Removed dynamic insertion from {filename}")
    return True

# Process priority files
for filename, card_info in cards.items():
    print(f"Processing {filename}...")
    add_static_card(filename, card_info)
    remove_dynamic_insertion(filename)

print("\nDone!")
