import cv2 
import numpy as np 
import os  # Dosya işlemleri için

# Kayıt dizini
save_dir = r"C:\OpenCV_Work\src\Example_5\results"

# Dizini oluştur (yoksa)
os.makedirs(save_dir, exist_ok=True)

image = cv2.imread(r"C:\OpenCV_Work\src\Example_5\assets\fruits.jpg")
image = cv2.resize(image, (640, 640))

# Orjinal görüntüyü kaydet
cv2.imwrite(os.path.join(save_dir, "original.jpg"), image)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, threshold1=100, threshold2=200)
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Aşama görüntülerini kaydet
cv2.imwrite(os.path.join(save_dir, "gray.jpg"), gray)
cv2.imwrite(os.path.join(save_dir, "edges.jpg"), edges)
cv2.imwrite(os.path.join(save_dir, "thresh.jpg"), thresh)

contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Tüm konturları tek bir görselde kaydet
all_contours_img = image.copy()
cv2.drawContours(all_contours_img, contours, -1, (0, 255, 0), 2)
cv2.imwrite(os.path.join(save_dir, "all_contours.jpg"), all_contours_img)

# Limit the number of strokes (if there are too many strokes)
if len(contours) > 20:
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:20]

# Calculate and display properties for each contour.
for i, contour in enumerate(contours):
    # Area
    area = cv2.contourArea(contour)
    
    # Sadece belli boyuttaki konturları kaydet (isteğe bağlı)
    if area < 100:  # 100 pikselden küçükse atla
        continue
    
    # Perimeter
    perimeter = cv2.arcLength(contour, True)
    
    # Center
    M = cv2.moments(contour)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        center = (cx, cy)
    else:
        center = (0, 0)
        cx, cy = 0, 0
    
    # LIMITING RECTANGLE
    x, y, w, h = cv2.boundingRect(contour)
    
    # THE SMALLEST RECTANGLE IN TERMS OF AREA
    if len(contour) >= 5:  # minAreaRect requires at least 5 points.
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int32(box) 
    else:
        box = None
    
    # THE SMALLEST CIRCLE
    if len(contour) >= 5:  # minEnclosingCircle requires at least 5 dots.
        (circle_x, circle_y), radius = cv2.minEnclosingCircle(contour)
        circle_center = (int(circle_x), int(circle_y))
        radius = int(radius)
    else:
        circle_center = (0, 0)
        radius = 0
    
    # LENGTH/RATIO
    aspect_ratio = float(w) / h if h != 0 else 0
    
    # OCCUPANCY RATE
    rect_area = w * h
    extent = float(area) / rect_area if rect_area != 0 else 0
    
    # GLOBALIZATION
    if len(contour) >= 3:  # At least 3 points for convexHull
        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)
        solidity = float(area) / hull_area if hull_area != 0 else 0
    else:
        solidity = 0
    
    
    print(f"\nContour {i}:")
    print(f"  Area: {area:.2f} pixels²")
    print(f"  Perimeter: {perimeter:.2f} pixels")
    print(f"  Center: {center}")
    print(f"  Bounding Rectangle: x={x}, y={y}, w={w}, h={h}")
    print(f"  Aspect Ratio: {aspect_ratio:.2f}")
    print(f"  Extent (Fill Ratio): {extent:.2f}")
    print(f"  Solidity: {solidity:.2f}")

    img_copy = image.copy()
    
    # Draw Contours 
    cv2.drawContours(img_copy, [contour], -1, (0, 255, 0), 2)
    
    # Mark the center
    cv2.circle(img_copy, center, 5, (255, 0, 0), -1)
    cv2.putText(img_copy, f"C{i}", (cx+10, cy), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    
    # Draw the bounding rectangle.
    cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 0, 255), 2)
    
    # Draw the rectangle with the smallest area (if it exists).
    if box is not None:
        cv2.drawContours(img_copy, [box], 0, (255, 0, 255), 2)
    
    if radius > 0:
        cv2.circle(img_copy, circle_center, radius, (255, 255, 0), 2)
    
    cv2.putText(img_copy, f"Area: {area:.0f}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(img_copy, f"Perimeter: {perimeter:.0f}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Save a separate image for each contour.
    filename = os.path.join(save_dir, f"contour_{i}.jpg")
    cv2.imwrite(filename, img_copy)
    print(f"  Saved: {filename}")
    
    
    cv2.imshow(f'Contours {i} - Features', img_copy)
    cv2.waitKey(0)

cv2.destroyAllWindows()


print(f"\nAll images saved to: {save_dir}")
print(f"Total {len(contours)} contours processed and saved.")