import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
import random
import numpy as np

class ContainerXRayScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Maritime Container X-ray Fraud Detection")
        self.root.geometry("900x700")
        
        # Container contents types (normal vs fraudulent)
        self.normal_items = [
            "electronics", "clothing", "furniture", 
            "toys", "machinery", "food"
        ]
        
        self.fraud_items = [
            ("weapons", (255, 0, 0)),    # Red
            ("drugs", (0, 255, 255)),    # Yellow
            ("explosives", (0, 0, 255))  # Blue
        ]
        
        # GUI Setup
        self.create_widgets()
        self.scan_new_container()
    
    def create_widgets(self):
        """Create all GUI components"""
        # Control Panel
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(fill=tk.X)
        
        ttk.Button(control_frame, text="Scan New Container", 
                  command=self.scan_new_container).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Run Deep Scan", 
                  command=self.run_deep_scan).pack(side=tk.LEFT, padx=10)
        ttk.Button(control_frame, text="Check for Fraud", 
                  command=self.detect_fraud).pack(side=tk.LEFT)
        
        # Image Display
        self.image_frame = ttk.Frame(self.root)
        self.image_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.canvas = tk.Canvas(self.image_frame, width=800, height=400, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Analysis Results
        result_frame = ttk.LabelFrame(self.root, text="Scan Results", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.result_text = tk.Text(result_frame, height=8, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Threat indicators
        self.threat_vars = {
            "weapons": tk.BooleanVar(),
            "drugs": tk.BooleanVar(),
            "explosives": tk.BooleanVar()
        }
        
        indicator_frame = ttk.Frame(result_frame)
        indicator_frame.pack(fill=tk.X, pady=5)
        
        for threat, var in self.threat_vars.items():
            ttk.Checkbutton(indicator_frame, text=threat.capitalize(), 
                          variable=var, state='disabled').pack(side=tk.LEFT, padx=10)
    
    def generate_container_image(self):
        """Create a synthetic X-ray image of a container"""
        width, height = 800, 400
        image = Image.new("RGB", (width, height), "black")
        draw = ImageDraw.Draw(image)
        
        # Draw container outline
        draw.rectangle([50, 50, width-50, height-50], outline="gray", width=3)
        
        # Add normal items
        for _ in range(random.randint(8, 15)):
            x1 = random.randint(60, width-100)
            y1 = random.randint(60, height-100)
            x2 = x1 + random.randint(40, 200)
            y2 = y1 + random.randint(40, 120)
            
            item_type = random.choice(self.normal_items)
            color = self.get_item_color(item_type)
            draw.rectangle([x1, y1, x2, y2], fill=color)
        
        # Randomly add fraudulent items (30% chance)
        self.fraud_detected = []
        if random.random() < 0.3:
            num_frauds = random.randint(1, 3)
            for _ in range(num_frauds):
                x1 = random.randint(60, width-100)
                y1 = random.randint(60, height-100)
                x2 = x1 + random.randint(30, 80)
                y2 = y1 + random.randint(30, 80)
                
                fraud_type, color = random.choice(self.fraud_items)
                self.fraud_detected.append((fraud_type, (x1, y1, x2, y2)))
                draw.rectangle([x1, y1, x2, y2], fill=color)
                
                # Add threat markers
                if fraud_type == "weapons":
                    draw.line([x1+10, y1+10, x2-10, y2-10], fill="white", width=3)
                    draw.line([x2-10, y1+10, x1+10, y2-10], fill="white", width=3)
                elif fraud_type == "drugs":
                    draw.ellipse([x1+10, y1+10, x2-10, y2-10], outline="white", width=2)
                else:  # explosives
                    draw.rectangle([x1+5, y1+5, x2-5, y2-5], outline="white", width=2)
        
        return image
    
    def get_item_color(self, item_type):
        """Get X-ray color based on material density"""
        colors = {
            "electronics": (200, 150, 150),  # Light red (medium density)
            "clothing": (150, 200, 150),     # Light green (low density)
            "furniture": (150, 150, 200),    # Light blue
            "toys": (200, 200, 150),
            "machinery": (200, 180, 100),
            "food": (150, 200, 200)
        }
        return colors.get(item_type, (200, 200, 200))
    
    def scan_new_container(self):
        """Generate and display a new container scan"""
        self.container_image = self.generate_container_image()
        self.tk_image = ImageTk.PhotoImage(self.container_image)
        
        self.canvas.delete("all")
        self.canvas.create_image(400, 200, image=self.tk_image)
        
        # Reset results
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "New container scanned. Ready for analysis.")
        
        for var in self.threat_vars.values():
            var.set(False)
    
    def run_deep_scan(self):
        """Simulate a more thorough scanning process"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Running deep scan...\n")
        
        # Simulate scanning progress
        for i in range(1, 6):
            self.root.after(500 * i, lambda x=i: 
                self.result_text.insert(tk.END, f"Layer {x}/5 scanned...\n"))
        
        self.root.after(3000, lambda: 
            self.result_text.insert(tk.END, "\nDeep scan complete. Check for fraud."))
    
    def detect_fraud(self):
        """Analyze the image for fraudulent items"""
        self.result_text.delete(1.0, tk.END)
        
        if not hasattr(self, 'fraud_detected'):
            self.result_text.insert(tk.END, "No scan available. Please scan a container first.")
            return
        
        # Reset threat indicators
        for var in self.threat_vars.values():
            var.set(False)
        
        if not self.fraud_detected:
            self.result_text.insert(tk.END, "✅ No fraudulent items detected\n\n")
            self.result_text.insert(tk.END, "Container appears to contain only legitimate goods.")
            return
        
        self.result_text.insert(tk.END, "🚨 POTENTIAL FRAUD DETECTED 🚨\n\n")
        
        # Draw red boxes around fraud items
        draw = ImageDraw.Draw(self.container_image)
        
        for fraud_type, coords in self.fraud_detected:
            x1, y1, x2, y2 = coords
            draw.rectangle([x1-5, y1-5, x2+5, y2+5], outline="red", width=3)
            
            # Update threat indicators
            self.threat_vars[fraud_type].set(True)
            
            self.result_text.insert(tk.END, 
                f"- {fraud_type.upper()} detected at position ({x1}, {y1})\n")
        
        # Update image with bounding boxes
        self.tk_image = ImageTk.PhotoImage(self.container_image)
        self.canvas.create_image(400, 200, image=self.tk_image)
        
        self.result_text.insert(tk.END, "\nRecommendation: Hold container for manual inspection.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContainerXRayScanner(root)
    root.mainloop()