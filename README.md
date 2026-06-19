# BOB - The Bot 

BOB - The bot is a fully offline, privacy-first desktop AI assistant driven by a local `llama3:8b` instance running through Ollama. Built using Python and `CustomTkinter`, it utilizes asynchronous background threading to ensure the interface remains completely fluid and lag-free during local speech recognition and system automation tasks.

### 🌴 Trivandrum Slang Integration
What sets BOB apart is his unique regional personality layer. Modeled with native **Thiruvananthapuram (Trivandrum) dialect and local slang mechanics**, BOB interacts like a true local:
* **Visual Layer:** The GUI displays crisp, casual **Manglish layout** text using classic regional expressions like *Entheru, Aliya, Dei makkale, Scene aanu,* and *Set aanu*.
* **Vocal Layer:** To prevent broken, robotic pronunciation, the code dynamically maps matching **native Malayalam script** directly to the text-to-speech driver. 
* **Cinematic Delivery:** Audio segments are processed with a deep-bass pitch modulation filter to give BOB a commanding, heavy movie-star tone.

### 🚀 Key Features
* **100% Local Inference:** Runs completely offline with zero dependency on external cloud APIs or data tracking.
* **Asynchronous Threading:** Heavy AI processing pipelines and microphone recognition are offloaded to background threads to eliminate window freezing.
* **System Automation:** Built-in shortcut macros to seamlessly automate launching tools like Google and YouTube via system controls.

### 🛠️ Quick Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Start your background model: `ollama run llama3:8b`
3. Launch the app: `python bob_face.py`
