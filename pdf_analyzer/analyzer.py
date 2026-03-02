import re

class HeapSprayAnalyzer:
    def __init__(self):
        # Patterns commonly found in heap-spraying attacks
        self.patterns = {
            "NOP Sled": [
                r"%u9090",
                r"\\x90",     # matches \x90 as it appears in JS string literals
                r"%u0C0C",
                r"%u4141"    # 'AAAA' sled
            ],
            "Massive String Concatenation": [
                r"while\s*\(.*\.length\s*<\s*\d{5,}\)",  # while loop with large length threshold
                r"for\s*\(.*\w+\s*<\s*\d{5,}",            # for loop with large iteration count
                r"\.repeat\(\d{5,}\)"                       # very large .repeat() call
            ],
            "Memory Allocation Vectors": [
                r"new\s+Array\(\d{5,}\)", 
                r"\[\]\s*;\s*for\(", # filling an array in a loop
                r"\w+\[\w+\]\s*=\s*\w+\s*\+\s*\w+"
            ],
            "Suspicious Functions": [
                r"unescape\(",
                r"eval\(",
                r"String\.fromCharCode\(",
                r"document\.write\("
            ]
        }

    def analyze(self, js_code):
        results = {
            "findings": [],
            "score": 0,
            "confidence": "CLEAN"
        }

        if not js_code:
            return results

        total_matches = 0
        for category, regex_list in self.patterns.items():
            category_matches = 0
            for pattern in regex_list:
                matches = re.findall(pattern, js_code, re.IGNORECASE)
                if matches:
                    category_matches += len(matches)
            
            if category_matches > 0:
                results["findings"].append({
                    "category": category,
                    "count": category_matches
                })
                # Weighting: Sleds and Loops are higher signals
                if category in ["NOP Sled", "Massive String Concatenation"]:
                    results["score"] += 10 * min(category_matches, 5)
                else:
                    results["score"] += 5 * min(category_matches, 5)
                total_matches += category_matches

        # Determine confidence level
        if results["score"] >= 40:
            results["confidence"] = "HIGH"
        elif results["score"] >= 20:
            results["confidence"] = "MEDIUM"
        elif results["score"] > 0:
            results["confidence"] = "LOW"

        return results
