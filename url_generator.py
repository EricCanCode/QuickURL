#!/usr/bin/env python3
"""
QuickURL - URL Template Generator
A simple GUI tool to generate multiple URLs from a template with variable substitution.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys
import json
import os

try:
    import pyperclip
except ImportError:
    pyperclip = None

class URLTemplateRow:
    """Represents a single URL template row with function name and template."""
    
    def __init__(self, parent, on_remove=None):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.X, padx=5, pady=3)
        
        # Function name
        ttk.Label(self.frame, text="Function:", width=10).pack(side=tk.LEFT, padx=(0, 5))
        self.function_entry = ttk.Entry(self.frame, width=20)
        self.function_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # URL template
        ttk.Label(self.frame, text="URL Template:", width=12).pack(side=tk.LEFT, padx=(0, 5))
        self.template_entry = ttk.Entry(self.frame, width=60)
        self.template_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        # Remove button
        if on_remove:
            self.remove_btn = ttk.Button(self.frame, text="−", width=3, 
                                        command=lambda: on_remove(self))
            self.remove_btn.pack(side=tk.LEFT)
    
    def get_data(self):
        """Returns tuple of (function_name, template)."""
        return self.function_entry.get().strip(), self.template_entry.get().strip()
    
    def set_data(self, function_name, template):
        """Sets the function name and template."""
        self.function_entry.delete(0, tk.END)
        self.function_entry.insert(0, function_name)
        self.template_entry.delete(0, tk.END)
        self.template_entry.insert(0, template)
    
    def destroy(self):
        """Removes this row from the UI."""
        self.frame.destroy()


class QuickURLApp:
    """Main application class for URL Template Generator."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("QuickURL - URL Template Generator")
        self.root.geometry("900x700")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('default')
        
        # Template rows list
        self.template_rows = []
        
        # Default templates file path
        self.config_dir = os.path.expanduser("~/Desktop/Development/QuickURL")
        self.templates_file = os.path.join(self.config_dir, "templates.json")
        
        # Setup UI
        self.setup_ui()
        
        # Load saved templates or add defaults
        self.load_templates()
    
    def setup_ui(self):
        """Creates the main UI layout."""
        
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_frame, text="QuickURL Generator", 
                         font=('Helvetica', 18, 'bold'))
        title.pack(pady=(0, 10))
        
        # Source URL Section
        source_frame = ttk.LabelFrame(main_frame, text="Source URL", padding="10")
        source_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(source_frame, 
                 text="Enter your base URL with variable placeholder (e.g., [your-tunnel-url]):",
                 font=('Helvetica', 10)).pack(anchor=tk.W, pady=(0, 5))
        
        self.source_url_entry = ttk.Entry(source_frame, font=('Courier', 11))
        self.source_url_entry.pack(fill=tk.X, pady=(0, 5))
        self.source_url_entry.insert(0, "[your-tunnel-url]")
        
        # Add example label
        ttk.Label(source_frame, 
                 text="Example: https://my-tunnel.trycloudflare.com",
                 font=('Helvetica', 9), foreground='gray').pack(anchor=tk.W)
        
        # URL Templates Section
        templates_frame = ttk.LabelFrame(main_frame, text="URL Templates", padding="10")
        templates_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Buttons above template area (horizontal, right-aligned)
        button_frame = ttk.Frame(templates_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.load_templates_btn = ttk.Button(button_frame, text="📂 Load Templates", 
                                            command=self.load_templates_dialog)
        self.load_templates_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        self.save_templates_btn = ttk.Button(button_frame, text="💾 Save Templates", 
                                            command=self.save_templates)
        self.save_templates_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        self.add_btn = ttk.Button(button_frame, text="+ Add Function", 
                                  command=self.add_template_row)
        self.add_btn.pack(side=tk.RIGHT)
        
        # Scrollable container for template rows
        canvas = tk.Canvas(templates_frame, height=200)
        scrollbar = ttk.Scrollbar(templates_frame, orient="vertical", command=canvas.yview)
        self.templates_container = ttk.Frame(canvas)
        
        self.templates_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.templates_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Generate button
        generate_frame = ttk.Frame(main_frame)
        generate_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.generate_btn = ttk.Button(generate_frame, text="🔗 Generate URLs", 
                                       command=self.generate_urls,
                                       style='Accent.TButton')
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        self.copy_all_btn = ttk.Button(generate_frame, text="📋 Copy All", 
                                       command=self.copy_all_results,
                                       state=tk.DISABLED)
        self.copy_all_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(generate_frame, text="Clear Results", 
                                    command=self.clear_results)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Results Section
        results_frame = ttk.LabelFrame(main_frame, text="Generated URLs", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, 
                                                      font=('Courier', 10),
                                                      height=15,
                                                      wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)
    
    def add_template_row(self):
        """Adds a new template row."""
        row = URLTemplateRow(self.templates_container, on_remove=self.remove_template_row)
        self.template_rows.append(row)
    
    def remove_template_row(self, row):
        """Removes a template row."""
        if len(self.template_rows) <= 1:
            messagebox.showwarning("Warning", "You must have at least one template!")
            return
        
        row.destroy()
        self.template_rows.remove(row)
    
    def add_default_templates(self):
        """Adds default template rows."""
        defaults = [
            ("Health Check", "[your-tunnel-url]/health"),
            ("Run Preview", "[your-tunnel-url]/preview?code=import%20SwiftUI%0A%0Astruct%20ContentView%3A%20View%20%7B%0A%20%20%20%20var%20body%3A%20some%20View%20%7B%0A%20%20%20%20%20%20%20%20Text(%22Hello!%22)%0A%20%20%20%20%7D%0A%7D&device=iPhone%2016%20Pro"),
        ]
        
        for function_name, template in defaults:
            row = URLTemplateRow(self.templates_container, on_remove=self.remove_template_row)
            row.set_data(function_name, template)
            self.template_rows.append(row)
    
    def save_templates(self):
        """Saves current templates to JSON file with custom name."""
        templates_data = []
        for row in self.template_rows:
            function_name, template = row.get_data()
            if function_name and template:
                templates_data.append({
                    "function_name": function_name,
                    "template": template
                })
        
        if not templates_data:
            messagebox.showwarning("Warning", "No templates to save!")
            return
        
        # Open save dialog with default filename
        filename = filedialog.asksaveasfilename(
            title="Save Templates",
            initialdir=self.config_dir,
            initialfile="templates.json",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filename:
            return  # User cancelled
        
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as f:
                json.dump(templates_data, f, indent=2)
            messagebox.showinfo("Success", f"Saved {len(templates_data)} templates to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save templates: {str(e)}")
    
    def load_templates(self, filename=None):
        """Loads templates from JSON file or uses defaults."""
        # Clear existing templates
        for row in self.template_rows[:]:
            row.destroy()
        self.template_rows.clear()
        
        # Try to load from file
        load_file = filename or self.templates_file
        
        if os.path.exists(load_file):
            try:
                with open(load_file, 'r') as f:
                    templates_data = json.load(f)
                
                for item in templates_data:
                    row = URLTemplateRow(self.templates_container, on_remove=self.remove_template_row)
                    row.set_data(item["function_name"], item["template"])
                    self.template_rows.append(row)
                
                if filename:  # Only show message if explicitly loaded
                    messagebox.showinfo("Success", f"Loaded {len(templates_data)} templates")
                return
            except Exception as e:
                if filename:  # Only show error if user explicitly tried to load
                    messagebox.showerror("Error", f"Failed to load templates: {str(e)}")
        
        # If no saved templates, use defaults
        if not self.template_rows:
            self.add_default_templates()
    
    def load_templates_dialog(self):
        """Opens file dialog to load templates from a specific file."""
        filename = filedialog.askopenfilename(
            title="Load Templates",
            initialdir=self.config_dir,
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            self.load_templates(filename)
    
    def generate_urls(self):
        """Generates URLs by substituting the source URL into templates."""
        source_url = self.source_url_entry.get().strip()
        
        if not source_url:
            messagebox.showerror("Error", "Please enter a source URL!")
            return
        
        # Find the variable placeholder in source URL
        if '[' in source_url and ']' in source_url:
            # User entered placeholder, use it as is
            variable = source_url
        else:
            # User entered actual URL
            variable = "[your-tunnel-url]"
        
        results = []
        results.append("=" * 80)
        results.append("GENERATED URLs")
        results.append("=" * 80)
        results.append("")
        results.append(f"Source URL: {source_url}")
        results.append("")
        results.append("-" * 80)
        results.append("")
        
        for row in self.template_rows:
            function_name, template = row.get_data()
            
            if not function_name or not template:
                continue
            
            # Replace the variable placeholder with the source URL
            generated_url = template.replace(variable, source_url)
            
            results.append(f"[{function_name}]")
            results.append(generated_url)
            results.append("")
        
        results.append("-" * 80)
        results.append(f"Total URLs generated: {len([r for r in self.template_rows if r.get_data()[0]])}")
        results.append("=" * 80)
        
        # Display results
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, "\n".join(results))
        
        # Enable copy button
        self.copy_all_btn.config(state=tk.NORMAL)
        
        messagebox.showinfo("Success", f"Generated {len([r for r in self.template_rows if r.get_data()[0]])} URLs!")
    
    def copy_all_results(self):
        """Copies all generated URLs to clipboard."""
        results = self.results_text.get(1.0, tk.END).strip()
        
        if not results:
            messagebox.showwarning("Warning", "No results to copy!")
            return
        
        try:
            if pyperclip:
                pyperclip.copy(results)
                messagebox.showinfo("Success", "All URLs copied to clipboard!")
            else:
                # Fallback: copy to system clipboard using tkinter
                self.root.clipboard_clear()
                self.root.clipboard_append(results)
                self.root.update()
                messagebox.showinfo("Success", "All URLs copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")
    
    def clear_results(self):
        """Clears the results text area."""
        self.results_text.delete(1.0, tk.END)
        self.copy_all_btn.config(state=tk.DISABLED)


def main():
    """Main entry point."""
    root = tk.Tk()
    app = QuickURLApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
