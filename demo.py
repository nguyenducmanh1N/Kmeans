import numpy as np
import cv2
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Label, Button, Entry

def kmeans_segmentation(image, num_clusters, max_iterations=100):
    # Chuyển đổi ảnh thành mảng NumPy
    h, w, _ = image.shape
    pixels = image.reshape(-1, 3)

    # Khởi tạo các centroids ngẫu nhiên
    centroids = pixels[np.random.choice(pixels.shape[0], num_clusters, replace=False)]

    for _ in range(max_iterations):
        # Tính toán khoảng cách giữa mỗi pixel và centroids
        distances = np.linalg.norm(pixels[:, np.newaxis] - centroids, axis=2)

        # Gán mỗi pixel vào cluster có centroids gần nhất
        labels = np.argmin(distances, axis=1)

        # Cập nhật centroids bằng cách tính trung bình của các pixel trong cùng một cluster
        new_centroids = np.array([pixels[labels == i].mean(axis=0) for i in range(num_clusters)])

        # Kiểm tra điều kiện dừng
        if np.all(centroids == new_centroids):
            break

        centroids = new_centroids

    # Tạo ảnh kết quả với màu từ centroids
    segmented_image = centroids[labels].reshape((h, w, 3)).astype(np.uint8)

    return segmented_image

def save_segmented_image(segmented_image):
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        cv2.imwrite(file_path, cv2.cvtColor(segmented_image, cv2.COLOR_RGB2BGR))

def open_image_and_segment():
    global segmented_image  # Đặt biến toàn cục để truy cập từ chức năng lưu
    file_path = filedialog.askopenfilename(title="Chọn hình ảnh", filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if file_path:
        # Đọc ảnh được chọn
        image = cv2.imread(file_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Phân đoạn ảnh bằng K-means
        segmented_image = kmeans_segmentation(image, num_clusters)

        # Hiển thị hình ảnh gốc và hình ảnh đã phân đoạn
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.imshow(image)
        plt.title("Original Image")

        plt.subplot(1, 2, 2)
        plt.imshow(segmented_image)
        plt.title("Segmented Image")

        plt.show()

        # Kích hoạt nút Lưu ảnh sau phân đoạn
        save_button['state'] = 'normal'

def update_num_clusters_and_segment():
    update_num_clusters()
    open_image_and_segment()

def update_num_clusters():
    global num_clusters
    num_clusters = int(num_clusters_entry.get())

# Tạo cửa sổ giao diện người dùng
root = Tk()
root.title("Phân vùng ảnh bằng K-Means")

# Định nghĩa số lượng cụm mặc định
num_clusters = 5  # Số lượng cụm mặc định

# Button để mở ảnh và phân đoạn
open_button = Button(root, text="Mở và Phân vùng ảnh", command=open_image_and_segment)
open_button.pack()

# Nhập số lượng cụm
num_clusters_label = Label(root, text="Số lượng cụm:")
num_clusters_label.pack()
num_clusters_entry = Entry(root)
num_clusters_entry.insert(0, str(num_clusters))  # Hiển thị giá trị mặc định
num_clusters_entry.pack()

# Button để cập nhật số lượng cụm và phân đoạn ảnh
update_button = Button(root, text="Cập nhật và Phân vùng", command=update_num_clusters_and_segment)
update_button.pack()

# Button để lưu hình ảnh sau phân đoạn (mặc định bị vô hiệu hóa)
save_button = Button(root, text="Lưu ảnh sau phân vùng", command=lambda: save_segmented_image(segmented_image))
save_button.pack()
save_button['state'] = 'disabled'  # Vô hiệu hóa nút lưu ban đầu

root.mainloop()
