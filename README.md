# COMP3710

## What is the Goal?
We want to use a computer program to help doctors by automatically identifying different parts of the brain in MRI images. This is called segmentation. Think of it like coloring in a coloring book, where we want to color different areas of the brain in different colors.

## What is U-Net?
U-Net is a type of computer program (or model) that helps with this task. It’s called "U-Net" because its shape looks like the letter "U."
* How it Works:
    * It has two main parts:
        1. Encoder: This part looks at the image and tries to understand it. It reduces the size of the image while keeping important information.
        2. Decoder: This part takes that understanding and tries to recreate a new image that shows the different areas of the brain.


## The Data
We use a special dataset called the OASIS dataset, which contains many MRI images of brains. Each image has labels that tell us which parts of the brain are which.

## Steps to Train the U-Net
1. Load the Data:
    * We get the MRI images and their labels from the OASIS dataset.
    * We make sure the images are in a format that the computer can understand. 
2. Preprocess the Data:
    * We normalize the images, which means adjusting them so they are easier for the model to work with.
    * We convert the labels into a format called "one-hot encoding," which is like turning categories into a series of 1s and 0s. 
3. Build the U-Net Model:
    * We create the U-Net architecture using layers of math operations that help the model learn from the data. 
4. Train the Model:
    * We show the model many images and their correct labels.
    * The model tries to guess the labels, and we tell it how well it did. This helps the model learn and improve over time. 
5. Check the Model's Performance:
    * After training, we use a different set of images (test set) to see how well the model can segment the brain.
    * We calculate a score called the Dice Similarity Coefficient (DSC). A score higher than 0.9 means the model is doing a great job! 
6. Visualize Results:
    * We can show the original MRI image, the true labels (what the correct segmentation looks like), and the model's predictions side by side. This helps us see how well the model is performing. 

## Why is This Important?
* Help Doctors: Automating the process of segmenting brain images can save doctors time and help them make better decisions about patient care.
* Learning Tool: This project also helps us understand how machines can learn from data, which is a big part of artificial intelligence (AI).
 Conclusion
In summary, we are training a computer model called U-Net to recognize different parts of the brain in MRI images. By doing this, we can assist doctors in diagnosing and treating brain-related health issues more effectively.

