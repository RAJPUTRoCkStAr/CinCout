# C-In-C-Out

# 1  Introduction
    This project employs advanced facial recognition algorithms to identify and verify individuals based on their facial features

    The system is designed with a focus on four key types of institutions: schools, universities, offices, and hospitals. Each institution has unique attendance requirements and regulations, and the system is designed to meet these specific needs.

    Schools/Universities: The system can manage student attendance, and generate reports for academic performance evaluations.
    Offices: The system supports employee attendance tracking, shift management, and integration with payroll systems.
    Hospitals: The system can be used to monitor the attendance of medical staff, including doctors, nurses, ensuring that shifts are adequately covered

    Admin-Only Access: To ensure data security and maintain the integrity.also Add the Employees of the attendance records, only authorized administrators can log in and access the system. 

#  project Images
1 ![Screenshot 2024-08-30 111023](https://github.com/user-attachments/assets/7a6fa99c-4236-49b0-950d-20137556e782)

2 ![Screenshot 2024-08-30 111103](https://github.com/user-attachments/assets/c34aa0c7-9c17-4e88-99f6-b8fa3545d197)

3 ![Screenshot 2024-08-30 111400](https://github.com/user-attachments/assets/92269665-9656-46b0-a139-4e8f2d1ea39d)

4 ![Screenshot 2024-08-30 111439](https://github.com/user-attachments/assets/e9b1c103-aaf0-4762-9ff9-07be7b954faf)

5 ![Screenshot 2024-08-30 111452](https://github.com/user-attachments/assets/de0dc683-b3c5-467c-ba38-fe1bd57d0691)

6 ![Screenshot 2024-09-02 103922](https://github.com/user-attachments/assets/f372ea54-7c55-4c54-b3a2-e7465c52feb9)

7 ![Screenshot 2024-09-02 104540](https://github.com/user-attachments/assets/39d1c50e-f1f9-4f0f-94d7-c7d5f82fac05)
 
8 ![Screenshot 2024-09-02 104604](https://github.com/user-attachments/assets/685acd8c-91bf-4791-b971-09312fc79999)





# 2  People Entering and exit 
    This repository contains the code for a real-time people-counting system using YOLOv8 and OpenCV. The system utilizes YOLOv8, a state-of-the-art object detection algorithm, to detect people in images and videos. Additionally, it includes a custom class that can be used for detecting people without relying on YOLOv8.





# Clone the repository
    git clone https://github.com/RAJPUTRoCkStAr/Human-activity.git


# Navigate into the project directory
    cd Human-Activity
    
## Install dependencies
    pip install -r requirements.txt

# Run Cmd
    cd face     
    python -m streamlit run main.py
    
# Project Structure
.
├── Human-Activity/                     
├── docs/                           
    └── HRM.pdf
    └── Human-Activity-Detection-Project.pptx                    
    └── ABC.Docs                    
├── face                           
    └── .streamlit/
        └── config.toml
    └── data/
        └── database.db
    └── media/
        └── Images
    └── resources/                        
        └── anti_spoof_models/                        
            └── 2.7_80x80_MiniFASNetV2.pth                        
            └── 4_0_0_80x80_MiniFASNetV1SE.pth 
        └── detection_model
            └── deploy.prototxt
            └── Widerface-RetinaFace.caffemodel
    └── src/
        └── data_io/
            └── dataset_folder.py
            └── dataset_loader.py
            └── functional.py
            └── transform.py
        └── model_lib
            └── MiniFASNet.py
            └── MultiFTNet.py
            └── anti_spoof_predict.py
            └── default_config.py
            └── generate_patches.py
            └── tracker.py
            └── train_main.py
            └── utility.py
    └── testing/                 
        └── videos                 
    └──visitor_database/
        └──visitor Images
    └── Visitor_history/
        └── Visitor history Images
    └── attendaminaprac.py
    └── Attendan.py
    └── Attendmain.py
    └── class.py
    └── coco.txt
    └── dash.py
    └── data.yaml
    └── main.py
    └── Manageatten.py
    └── test.py
    └── train.py
    └── utils.py
    └── yolov10n.pt              
├──.gitattributes
├──.gitignore
├──note.md
├──README.md
└──requirements.txt 


       
# conclusion

In a face detection-based attendance system, the concepts of "Check-In" (C In) and "Check-Out" (C Out) are crucial for tracking when an individual starts and ends their presence within a particular environment, such as a workplace or classroom.

 