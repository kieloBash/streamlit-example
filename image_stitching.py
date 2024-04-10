import numpy as np
import cv2
import random
import streamlit as st
import tempfile

def initial_alignment(img1, img2):
    # Detect SIFT keypoints and descriptors
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    
    # Match descriptors using FLANN
    flann = cv2.FlannBasedMatcher(dict(algorithm=0, trees=5), dict(checks=50))
    matches = flann.knnMatch(des1, des2, k=2)
    
    # Filter good matches using Lowe's ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)
            
    # Draw feature points on images
    img1_kp = cv2.drawKeypoints(img1, kp1, None, color=(0, 0, 255))
    img2_kp = cv2.drawKeypoints(img2, kp2, None, color=(0, 255, 0))
    
    return img1_kp, img2_kp, kp1, kp2, good_matches

def homography_estimation(kp1, kp2, matches, img1, img2):
    # Randomly select seed feature points
    seed_matches = random.sample(matches, 4)
    
    # Estimate homography
    src_pts = np.float32([kp1[m.queryIdx].pt for m in seed_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in seed_matches]).reshape(-1, 1, 2)
    M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    
    return M

def alignment_quality_evaluation(img1, img2):
    # Compute edge maps
    edge_map1 = cv2.Canny(img1, 100, 200)
    edge_map2 = cv2.Canny(img2, 100, 200)
    
    # Calculate difference map
    diff_map = cv2.absdiff(edge_map1, edge_map2)
    
    # Calculate seam cost
    seam_cost = np.sum(diff_map)
    
    return seam_cost

def refinement(img1, img2):
    # Content-preserving warping
    # Not implemented for this example
    
    # Down-sampling of input images
    img1_downsampled = cv2.resize(img1, (0, 0), fx=0.5, fy=0.5)
    img2_downsampled = cv2.resize(img2, (0, 0), fx=0.5, fy=0.5)
    
    # Plausible seam estimation
    # Not implemented for this example
    
    return img1_downsampled, img2_downsampled

def stitching(img1, img2):
    # Stitch images using OpenCV's stitching module without converting to grayscale
    stitcher = cv2.Stitcher.create()
    status, stitched_image = stitcher.stitch([img1, img2])  # No need to convert to grayscale
    
    if status != cv2.Stitcher_OK:
        print("Stitching failed!")
        return None

    return stitched_image

def stitch_images(uploaded_files):
    # Load input images
    temp_files = []
    for uploaded_file in uploaded_files:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())
        temp_file.close()
        temp_files.append(temp_file.name)
    
    # Read the temporary files using OpenCV
    img1 = cv2.imread(temp_files[0])
    img2 = cv2.imread(temp_files[1])
    
    # Step 1: Initial Alignment
    img1_kp, img2_kp, kp1, kp2, good_matches = initial_alignment(img1, img2)
    
    # Step 2: Homography Estimation
    homography_matrix = homography_estimation(kp1, kp2, good_matches, img1, img2)
    
    # Step 3: Alignment Quality Evaluation
    seam_cost = alignment_quality_evaluation(img1, img2)
    
    # Step 4: Refinement
    img1_refined, img2_refined = refinement(img1, img2)
    
    # Step 5: Stitching
    stitched_image = stitching(img1_refined, img2_refined)
    
    if stitched_image is not None:
        st.image(stitched_image, caption='Stitched Image')