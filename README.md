# IP_Project_Movement-Detection
Movement detection from a gray-scale images sequence by computing the optical flow.

git clone https://github.com/SamuelAierizer/IP_Project_Movement-Detection.git

Documentation : https://www.overleaf.com/read/fwkjszqxkzrj


How to run?
For sparse optical flow:

    'py project.py --algorithm lucaskanade --video_path Videos/people.mp4'

For dense optical flow:

    'py project.py --algorithm lucaskanade_dense --video_path Videos/people.mp4'

    'py project.py --algorithm farneback --video_path Videos/people.mp4'

    'py project.py --algorithm rlof --video_path Videos/people.mp4'
    
    'py project.py --algorithm vector --video_path Videos/banana.mp4'