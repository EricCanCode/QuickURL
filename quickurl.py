#!/usr/bin/env python3
"""
QuickURL - CLI URL Template Generator
Simple command-line tool to generate test URLs from templates.
"""

import sys
import json
import os

class QuickURL:
    def __init__(self):
        self.config_file = os.path.expanduser("~/.quickurl_config.json")
        self.templates = self.load_templates()
    
    def load_templates(self):
        """Load templates from config file or use defaults."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default templates
        return {
            "Health Check": "[url]/health",
            "Run Preview": "[url]/preview?code=import%20SwiftUI%0A%0Astruct%20ContentView%3A%20View%20%7B%0A%20%20%20%20var%20body%3A%20some%20View%20%7B%0A%20%20%20%20%20%20%20%20Text(%22Hello!%22)%0A%20%20%20%20%7D%0A%7D&device=iPhone%2016%20Pro"
        }
    
    def save_templates(self):
        """Save current templates to config file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.templates, f, indent=2)
            print(f"✓ Templates saved to {self.config_file}")
        except Exception as e:
            print(f"✗ Error saving templates: {e}")
    
    def generate(self, source_url):
        """Generate all URLs with the given source URL."""
        if not source_url:
            print("✗ Error: No source URL provided")
            return
        
        print("\n" + "=" * 80)
        print("GENERATED URLs".center(80))
        print("=" * 80)
        print(f"\nSource URL: {source_url}\n")
        print("-" * 80 + "\n")
        
        for name, template in self.templates.items():
            url = template.replace("[url]", source_url)
            print(f"[{name}]")
            print(url)
            print()
        
        print("-" * 80)
        print(f"Total: {len(self.templates)} URLs generated")
        print("=" * 80 + "\n")
    
    def list_templates(self):
        """List all current templates."""
        print("\nCurrent Templates:")
        print("-" * 80)
        for i, (name, template) in enumerate(self.templates.items(), 1):
            print(f"{i}. {name}")
            print(f"   {template}")
            print()
    
    def add_template(self, name, template):
        """Add a new template."""
        self.templates[name] = template
        self.save_templates()
        print(f"✓ Added template: {name}")
    
    def remove_template(self, name):
        """Remove a template by name."""
        if name in self.templates:
            del self.templates[name]
            self.save_templates()
            print(f"✓ Removed template: {name}")
        else:
            print(f"✗ Template not found: {name}")
    
    def interactive_mode(self):
        """Interactive mode for generating URLs."""
        print("\n" + "=" * 80)
        print("QuickURL - URL Template Generator".center(80))
        print("=" * 80 + "\n")
        
        source_url = input("Enter source URL: ").strip()
        
        if source_url:
            self.generate(source_url)
            
            # Copy to clipboard if possible
            try:
                import subprocess
                result = []
                for name, template in self.templates.items():
                    url = template.replace("[url]", source_url)
                    result.append(f"[{name}]\n{url}\n")
                
                text = "\n".join(result)
                subprocess.run('pbcopy', text=True, input=text, check=True)
                print("📋 All URLs copied to clipboard!\n")
            except:
                pass

def main():
    """Main entry point."""
    app = QuickURL()
    
    if len(sys.argv) == 1:
        # No arguments - run interactive mode
        app.interactive_mode()
    
    elif len(sys.argv) == 2:
        # One argument - generate URLs with this source
        app.generate(sys.argv[1])
    
    elif sys.argv[1] == "list":
        # List templates
        app.list_templates()
    
    elif sys.argv[1] == "add" and len(sys.argv) == 4:
        # Add template: quickurl.py add "name" "template"
        app.add_template(sys.argv[2], sys.argv[3])
    
    elif sys.argv[1] == "remove" and len(sys.argv) == 3:
        # Remove template: quickurl.py remove "name"
        app.remove_template(sys.argv[2])
    
    else:
        print("Usage:")
        print("  python3 quickurl.py                          # Interactive mode")
        print("  python3 quickurl.py <url>                    # Generate URLs")
        print("  python3 quickurl.py list                     # List templates")
        print("  python3 quickurl.py add <name> <template>    # Add template")
        print("  python3 quickurl.py remove <name>            # Remove template")
        print("\nExample:")
        print('  python3 quickurl.py https://my-tunnel.trycloudflare.com')

if __name__ == "__main__":
    main()
