"""
Extract high-quality files (70%+ accuracy) for Phase 2 demo
Based on Phase 1 evaluation results
"""

import csv

# Files with 70%+ accuracy from Phase 1 results
good_files = {
    # Perfect matches (100%)
    "NP_001.wav": {"transcript": "नमस्कार", "romanized": "Namaskar"},
    "NP_002.wav": {"transcript": "नमस्ते", "romanized": "Namaste"},
    "NP_011.wav": {"transcript": "शुभ प्रभात", "romanized": "subha prabhat"},
    "NP_107.wav": {"transcript": "बीस", "romanized": "bis"},
    "NP_122.wav": {"transcript": "आमा", "romanized": "aama"},
    "NP_123.wav": {"transcript": "दिदी", "romanized": "didi"},
    "NP_129.wav": {"transcript": "अस्पताल", "romanized": "aspataal"},
    "NP_137.wav": {"transcript": "नमस्कार", "romanized": "Namaskar"},
    
    # High quality (80%+)
    "NP_012.wav": {"transcript": "शुभ बिहानी", "romanized": "subha bihani"},
    "NP_013.wav": {"transcript": "शुभ दिन", "romanized": "subha din"},
    "NP_016.wav": {"transcript": "शुभ रात्रि", "romanized": "subha ratri"},
    "NP_018.wav": {"transcript": "शुभ बिहानी होस्", "romanized": "subha bihani hos"},
    "NP_112.wav": {"transcript": "सोमबार", "romanized": "sombar"},
    "NP_113.wav": {"transcript": "बुधबार", "romanized": "budhbar"},
    "NP_118.wav": {"transcript": "मार्च", "romanized": "march"},
    "NP_119.wav": {"transcript": "अप्रिल", "romanized": "april"},
    "NP_121.wav": {"transcript": "बुबा", "romanized": "buba"},
    "NP_126.wav": {"transcript": "बहिनी", "romanized": "bahini"},
    "NP_133.wav": {"transcript": "विमान", "romanized": "biman"},
    
    # Good quality (70-80%)
    "NP_102.wav": {"transcript": "दुई", "romanized": "dui"},
    "NP_150.wav": {"transcript": "शुभरात्रि", "romanized": "shubharatri"},
}

output_file = "data/metadata_curated.csv"

print(f"Creating curated dataset with {len(good_files)} high-quality files...")
print()

with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['filename', 'transcript', 'romanized'])
    writer.writeheader()
    
    for filename, data in sorted(good_files.items()):
        writer.writerow({
            'filename': filename,
            'transcript': data['transcript'],
            'romanized': data['romanized']
        })
        print(f"✓ {filename}: {data['transcript']}")

print()
print(f"✓ Created: {output_file}")
print(f"  Total: {len(good_files)} files")
print()
print("These files will be used for Phase 2 demo!")