from p5 import *

# Sample data
data = [50, 75, 100, 125, 150]
labels = ['A', 'B', 'C', 'D', 'E']
marker_value = 100  # Value for the line marker

def setup():
    size(800, 600)
    background(255)
    text_size(16)
    no_loop()

def draw():
    bar_width = width / (len(data) * 2)
    max_value = max(data)
    
    for i, value in enumerate(data):
        # Calculate bar height
        bar_height = (value / max_value) * (height - 100)
        
        # Draw bar
        fill(100, 150, 200)
        rect((i * 2 * bar_width) + bar_width / 2, height - bar_height - 50, bar_width, bar_height)
        
        # Draw label
        fill(0)
        text(labels[i], (i * 2 * bar_width) + bar_width, height - 30)
    
    # Draw marker line
    marker_y = height - ((marker_value / max_value) * (height - 100)) - 50
    stroke(255, 0, 0)
    stroke_weight(2)
    line(0, marker_y, width, marker_y)
    
    # Draw marker text
    fill(255, 0, 0)
    text(f'Marker: {marker_value}', 10, marker_y - 10)

run()
