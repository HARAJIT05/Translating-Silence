# Translating-Silence

Translating-Silence is a computer vision-powered system designed to translate Indian Sign Language (ISL) into text in real-time. The aim is to enhance accessibility and bridge communication gaps for the deaf and hard-of-hearing communities using machine learning.

## 🚀 Features

- 🎥 Real-time sign language detection using a webcam
- 🧠 ISL gesture recognition using machine learning
- 🖥️ Live text output of detected gestures
- 🔧 Easy to modify and expand for more gestures/languages

## 🛠️ Installation

👉 [Download Dataset and Extract to the directory](https://gofile.io/d/B4DvFG)

```bash
git clone https://github.com/HARAJIT05/Translating-Silence.git
cd Translating-Silence
pip install -r requirements.txt
```

Make sure Python and OpenCV are installed on your machine.

## ▶️ Usage

To start the application:

```bash
Change the directory PATH on line 10 at main.py

python main.py
```

- Sign using ISL in front of your webcam.
- The model will recognize gestures and display corresponding text on the interface.

## 🗂️ Project Structure

```plaintext
Translating-Silence/
│
├── main.py                 # Main script to run the application
├── DenseNet121_Final.keras     #Trained AI model
├── templates/              # HTML templates if using web-based output
├── requirements.txt        #Required libreries for the python file.
└── README.md               # Project documentation
```

## 📷 Demo

<img src="https://files.catbox.moe/3b7e7g.jpg" />

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repo
2. Create your branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Open a Pull Request

## 👤 Contributors

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/HARAJIT05">
        <img src="https://avatars.githubusercontent.com/u/110291590?v=4" width="100px;" alt="Harajit Das"/><br />
        <sub><b>Harajit Das</b></sub>
      </a>
    </td>
        <td align="center">
      <a href="https://github.com/Senapati5">
        <img src="https://avatars.githubusercontent.com/u/158562332?v=4" width="100px;" alt="Arpan Senapati"/><br />
        <sub><b>Arpan Senapati</b></sub>
      </a>
    </td>
          <td align="center">
      <a href="https://github.com/SulagnaMahato">
        <img src="https://avatars.githubusercontent.com/u/162031954?v=4" width="100px;" alt="Sulagna Mahato"/><br />
        <sub><b>Sulagna Mahato</b></sub>
      </a>
    </td>
     <td align="center">
      <a href="https://github.com/naiyapriya">
        <img src="https://avatars.githubusercontent.com/u/152768148?v=4" width="100px;" alt="Priya Naiya"/><br />
        <sub><b>Priya Naiya</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/sagarmazumder">
        <img src="https://avatars.githubusercontent.com/u/182473947?v=4" width="100px;" alt="Sagar Mazumdar"/><br />
        <sub><b>Sagar Mazumdar</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/sahidabu">
        <img src="https://avatars.githubusercontent.com/u/177731431?v=4" width="100px;" alt="Abu Sahid Mistri"/><br />
        <sub><b>Abu Sahid Mistri</b></sub>
      </a>
    </td>
  </tr>
</table>

## 📄 License

This project is licensed under the [MIT License](LICENSE).
