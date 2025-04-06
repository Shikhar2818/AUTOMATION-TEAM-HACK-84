# 🚆 Train Ticket Booking Automation

This project automates train ticket booking on **IRCTC** and **Goibibo** platforms using **Python**, **Selenium**, and **PyAutoGUI**. It is designed to simplify and speed up the booking process, especially during Tatkal hours when every second matters.

---

## 📌 Features

### 🔹 IRCTC Automation (using Selenium)
- Automated login (automatd CAPTCHA entry)
- Source and destination station selection
- Date and train number input
- Travel class selection (e.g., Sleeper, 3AC)
- Passenger details form fill-up
- UPI payment option
- Option to skip travel insurance

### 🔹 Goibibo Automation (using PyAutoGUI)
- GUI-based automation via image recognition
- Simulates mouse clicks and keyboard input
- Works with screen elements that are hard to access through HTML or DOM
- Automates the train booking flow from search to confirmation

---

## 🛠️ Tech Stack

- Python 3
- Selenium WebDriver
- PyAutoGUI
- Pyscreeze & OpenCV (for image matching)
- ChromeDriver
- Tesseract OCR

---



### 1. Clone the Repo
```bash
git clone https://github.com/your-username/train-booking-automation.git
cd train-booking-automation
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Setup ChromeDriver
Download ChromeDriver matching your Chrome version

Place it in the project folder or system PATH

4 run the script


🧑‍💻 Author
Shikhar , Amaan 
GitHub • LinkedIn

📄 License
This project is licensed under the MIT License.


