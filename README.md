# **C-In-C-Out Attendance System**

This project leverages advanced facial recognition algorithms to efficiently track and verify individuals using their facial features. The system is tailored for different institutional environments, ensuring precise attendance management while enhancing security and workflow automation.

---

## **1. Introduction**

The C-In-C-Out system focuses on real-time attendance tracking across various types of institutions, each with distinct requirements:

- **Schools & Universities**: Manages student attendance with report generation for academic performance evaluations.
- **Offices**: Tracks employee attendance, integrates with payroll systems, and supports shift management.
- **Hospitals**: Monitors attendance for medical staff like doctors and nurses, ensuring proper shift coverage.

### **Admin-Only Access**

To maintain data security, only authorized administrators can log in to access, manage, and add employee attendance records.

---

## **2. System Overview: People Entering and Exiting**

This repository features code for a real-time people-counting system utilizing YOLOv10 and OpenCV for object detection. The system can detect individuals in images or videos using YOLOv8 or a custom class that bypasses YOLOv10.

### **Screenshots**
1. ![Screenshot 2024-08-30 111023](https://github.com/user-attachments/assets/7a6fa99c-4236-49b0-950d-20137556e782)
2. ![Screenshot 2024-08-30 111103](https://github.com/user-attachments/assets/c34aa0c7-9c17-4e88-99f6-b8fa3545d197)
3. ![Screenshot 2024-08-30 111400](https://github.com/user-attachments/assets/92269665-9656-46b0-a139-4e8f2d1ea39d)
4. ![Screenshot 2024-08-30 111439](https://github.com/user-attachments/assets/e9b1c103-aaf0-4762-9ff9-07be7b954faf)
5. ![Screenshot 2024-08-30 111452](https://github.com/user-attachments/assets/de0dc683-b3c5-467c-ba38-fe1bd57d0691)
6. ![Screenshot 2024-09-02 103922](https://github.com/user-attachments/assets/f372ea54-7c55-4c54-b3a2-e7465c52feb9)
7. ![Screenshot 2024-09-02 104540](https://github.com/user-attachments/assets/39d1c50e-f1f9-4f0f-94d7-c7d5f82fac05)
8. ![Screenshot 2024-09-02 104604](https://github.com/user-attachments/assets/685acd8c-91bf-4791-b971-09312fc79999)

---

## **3. Getting Started**

Follow the steps below to set up the project on your local machine:

### **3.1 Clone the Repository**

To get started, clone the repository to your local machine by running:

```bash
git clone https://github.com/RAJPUTRoCkStAr/Human-activity.git
```
### 3.2 Navigate into the project directory 
Once the repository is cloned, move into the project directory:
```bash
cd Human-Activity
```    
### 3.3 Install dependencies
Install all the required dependencies using the following command:
```bash
pip install -r requirements.txt
```
### 3.4 Run the Application
Finally, to start the application, navigate to the face directory and run the Streamlit application:
```bash
cd face     
python -m streamlit run main.py
```
    
## **4. Project Structure**
The project structure is designed to facilitate easy navigation and organization of the codebase.
```bash
├── Human-Activity/
├── docs/
│   ├── HRM.pdf
│   ├── Human-Activity-Detection-Project.pptx
│   └── ABC.Docs
├── face/
│   ├── .streamlit/
│   │   └── config.toml
│   ├── data/
│   │   └── database.db
│   ├── media/
│   │   └── Images/
│   ├── resources/
│   │   ├── anti_spoof_models/
│   │   │   ├── 2.7_80x80_MiniFASNetV2.pth
│   │   │   └── 4_0_0_80x80_MiniFASNetV1SE.pth
│   │   └── detection_model/
│   │       ├── deploy.prototxt
│   │       └── Widerface-RetinaFace.caffemodel
│   ├── src/
│   │   ├── data_io/
│   │   │   ├── dataset_folder.py
│   │   │   ├── dataset_loader.py
│   │   │   ├── functional.py
│   │   │   └── transform.py
│   │   └── model_lib/
│   │       ├── MiniFASNet.py
│   │       ├── MultiFTNet.py
│   │       ├── anti_spoof_predict.py
│   │       ├── default_config.py
│   │       ├── generate_patches.py
│   │       ├── tracker.py
│   │       ├── train_main.py
│   │       └── utility.py
│   ├── testing/
│   │   └── videos/
│   ├── visitor_database/
│   │   └── visitor Images/
│   ├── Visitor_history/
│   │   └── Visitor history Images/
│   ├── attendaminaprac.py
│   ├── Attendan.py
│   ├── Attendmain.py
│   ├── class.py
│   ├── coco.txt
│   ├── dash.py
│   ├── data.yaml
│   ├── main.py
│   ├── Manageatten.py
│   ├── test.py
│   ├── train.py
│   └── utils.py
│   └── yolov10n.pt
├── .gitattributes
├── .gitignore
├── note.md
├── README.md
└── requirements.txt

```
## **5. Conclusion**       
In a face detection-based attendance system, the concepts of "Check-In" (C In) and "Check-Out" (C Out) are crucial for tracking when an individual starts and ends their presence within a particular environment, such as a workplace or classroom.

## **6. License**

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for detailed information.

### **MIT License Summary**

The MIT License is a permissive free software license originating from the Massachusetts Institute of Technology (MIT). It is one of the most commonly used open-source licenses. 

#### **Key Points:**
- **Permission:** Allows users to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.
- **Attribution:** The above copyright notice and this permission notice must be included in all copies or substantial portions of the Software.
- **Warranty Disclaimer:** The Software is provided "as is", without warranty of any kind.

For full details, please refer to the [LICENSE](LICENSE) file included in this repository.
---

