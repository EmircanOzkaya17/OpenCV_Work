import cv2
import numpy as np
import matplotlib.pyplot as plt
import os 

results_folder = r"C:\OpenCV_Work\src\Example_6\results"
if not os.path.exists(results_folder):
    os.makedirs(results_folder)
    print(f"'{results_folder}' folder created.") 
img=cv2.imread(r"C:\OpenCV_Work\assets\petersburg.jpg", cv2.IMREAD_GRAYSCALE)

# hist = cv2.calcHist(images, channels, mask, histSize, ranges, accumulate=False)
# channels--> (0=Grayscale, 1, 2, 3 for BGR or RGB), ranges--> Pixel value range (example: [0.256]) 
hist = cv2.calcHist([img], [0], None, [256], [0,256])

plt.figure(figsize=(10, 6))
plt.title('Gray Level Histogram')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')
plt.plot(hist, color='black')
plt.xlim([0, 256])
plt.grid(True, alpha=0.3)

line_plot_path = os.path.join(results_folder, 'Gray Level Histogram.png')
plt.savefig(line_plot_path, dpi=300, bbox_inches='tight')
print(f"Line chart saved: {line_plot_path}")

plt.show()

plt.figure(figsize=(12, 6))
plt.title('Gray Level Histogram (Bar)')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')
plt.bar(range(256), hist.flatten(), color='gray', width=1.0, edgecolor='black', linewidth=0.5)
plt.xlim([0, 256])
plt.grid(True, alpha=0.3)


bar_plot_path = os.path.join(results_folder, 'Gray Level Histogram (Bar).png')
plt.savefig(bar_plot_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Bar chart saved: {bar_plot_path}")

plt.show()