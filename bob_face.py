import datetime
import os
import sys
import threading
import webbrowser
import random
import ollama
import customtkinter as ctk
from gtts import gTTS         
import pygame                 
from pydub import AudioSegment  

# Audio system initialization
pygame.mixer.init()

# Dark theme layout setup
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class BobApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Settings with Humorous Title Acronym
        self.title("Bob - The Bot")
        self.geometry("600x700")
        self.resizable(False, False)

        # UI Grid Layout Configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 1. Main Chat Log Frame Display
        self.chat_display = ctk.CTkTextbox(self, state="disabled", corner_radius=10, font=("Helvetica", 14))
        self.chat_display.grid(row=0, column=0, padx=20, pady=(20, 10), columnspan=2, sticky="nsew")

        # 2. User Entry Bar Text Input
        self.entry_field = ctk.CTkEntry(self, placeholder_text="Enthu venelichum chodicho...", font=("Helvetica", 14))
        self.entry_field.grid(row=1, column=0, padx=(20, 10), pady=20, sticky="ew")
        self.entry_field.bind("<Return>", lambda event: self.send_text_message())

        # 3. Control Buttons Panel Frame
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=1, column=1, padx=(10, 20), pady=20, sticky="ne")

        self.send_btn = ctk.CTkButton(self.button_frame, text="Send Text", width=100, command=self.send_text_message)
        self.send_btn.pack(side="left", padx=5)

        self.mic_btn = ctk.CTkButton(self.button_frame, text="🎤 Speak", width=90, fg_color="#2c7a7b", hover_color="#236162", command=self.start_voice_thread)
        self.mic_btn.pack(side="left", padx=5)

        # Session Logging and Authentic Initial Wakeup Slang Display
        self.init_log_file()
        self.append_chat("Bob", "Bob vannittundu! Entheru appi vendethu?")
        
        # Initial greeting using pure native script for flawless pronunciation out loud
        threading.Thread(target=self.speak_native_malayalam, args=("ബോബ് വന്നിട്ടുണ്ട് എന്തര് അപ്പി വേണ്ടത്",), daemon=True).start()

    def init_log_file(self):
        with open("bob_conversation_log.txt", "a", encoding="utf-8") as f:
            f.write(f"\n--- GUI SESSION STARTED AT {datetime.datetime.now()} ---\n")

    def log_conversation(self, sender, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("bob_conversation_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {sender}: {message}\n")

    def append_chat(self, sender, message):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"{sender}: {message}\n\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
        self.log_conversation(sender, message)

    def speak_native_malayalam(self, text):
        """Generates flawless native Malayalam pronunciation and applies deep pitch modulation filters"""
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()

            temp_raw = "bob_native_temp.mp3"
            temp_pitched = "bob_dramatic_temp.mp3"

            # Setting lang='ml' forces gTTS to process script using its native engine mappings
            tts = gTTS(text=text, lang='ml') 
            tts.save(temp_raw)

            try:
                # Lower pitch slightly to provide a heavy, commanding cinema delivery layout
                sound = AudioSegment.from_file(temp_raw, format="mp3")
                new_sample_rate = int(sound.frame_rate * 0.90) 
                deep_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
                deep_sound = deep_sound.set_frame_rate(sound.frame_rate)
                
                loud_deep_sound = deep_sound + 3 
                loud_deep_sound.export(temp_pitched, format="mp3")
                play_target = temp_pitched
            except Exception:
                play_target = temp_raw

            pygame.mixer.music.load(play_target)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            pygame.mixer.music.unload()

            # Clean cache items
            for file in [temp_raw, temp_pitched]:
                if os.path.exists(file):
                    try:
                        os.remove(file)
                    except Exception:
                        pass
        except Exception as e:
            print(f"[Audio Error Exception Trace]: {e}")

    def send_text_message(self):
        user_text = self.entry_field.get().strip()
        if not user_text:
            return
        
        self.entry_field.delete(0, "end")
        self.append_chat("You", user_text)
        
        threading.Thread(target=self.process_ai_pipeline, args=(user_text,), daemon=True).start()

    def start_voice_thread(self):
        self.mic_btn.configure(text="🎙️ Kelkkunnu...", state="disabled")
        threading.Thread(target=self.process_voice_input, daemon=True).start()

    def process_voice_input(self):
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = recognizer.listen(source, timeout=4, phrase_time_limit=7)
                user_text = recognizer.recognize_google(audio)
                
                self.after(0, lambda: self.append_chat("You (Voice)", user_text))
                self.process_ai_pipeline(user_text)
            except Exception:
                self.after(0, lambda: self.append_chat("Bob", "Entheru appi ithu, paranjath tharimpum manasilaayilla!"))
                threading.Thread(target=self.speak_native_malayalam, args=("എന്തര് ഇത് പറഞ്ഞത് തരിമ്പും മനസ്സിലായില്ല",), daemon=True).start()
            finally:
                self.after(0, lambda: self.mic_btn.configure(text="🎤 Speak", state="normal"))

    def process_ai_pipeline(self, user_input):
        query = user_input.lower().strip()

        # Browser Automation Shortcuts
        if "open youtube" in query:
            self.after(0, lambda: self.append_chat("Bob", "YouTube thurakkanuvaa makkale..."))
            webbrowser.open("https://www.youtube.com")
            threading.Thread(target=self.speak_native_malayalam, args=("യൂട്യൂബ് തുറക്കുകയാണ് മക്കളെ",), daemon=True).start()
            return
            
        if "open google" in query:
            self.after(0, lambda: self.append_chat("Bob", "Google set aakkaam de ippo thurakkaam..."))
            webbrowser.open("https://www.google.com")
            threading.Thread(target=self.speak_native_malayalam, args=("ഗൂഗിൾ ഇപ്പോൾ തുറക്കാം",), daemon=True).start()
            return

        # Local LLM Processing Core (Llama3 handles facts in English flawlessly)
        try:
            response = ollama.chat(
                model='llama3:8b',
                messages=[
                    {
                        'role': 'system', 
                        'content': 'Your name is Bob. You are a helpful assistant. Keep your answer strictly limited to exactly one short, clean sentence.'
                    },
                    {'role': 'user', 'content': user_input}
                ]
            )
            ai_reply = response['message']['content'].strip()
            
            # 1. VISUAL LAYER: Formulate custom Manglish text strings for presentation display output window
            prefixes_eng = ["Entheru pfrene! ", "Dei makkale, ", "Aliya, ", "Entheru machaa, "]
            suffixes_eng = ["... Scene aanu!", "... Kidu saanam!", "... Set aanu!"]
            
            chosen_prefix_idx = random.randint(0, len(prefixes_eng) - 1)
            chosen_suffix_idx = random.randint(0, len(suffixes_eng) - 1)
            
            slang_display_text = f"{prefixes_eng[chosen_prefix_idx]}{ai_reply}{suffixes_eng[chosen_suffix_idx]}"
            self.after(0, lambda: self.append_chat("Bob", slang_display_text))
            
            # 2. AUDIO LAYER: Send structural equivalent script mapping down speech channel vector
            # The Malayalam audio tags decode naturally, bypassing robotic articulation blocks
            prefixes_ml = ["എന്തര് ഫ്രണ്ടേ! ", "ഡേയ് മക്കളേ, ", "അളിയാ, ", "എന്തര് മച്ചാ, "]
            suffixes_ml = ["... സീൻ ആണ്!", "... കിടു സാധനം!", "... സെറ്റ് ആണ്!"]
            
            slang_audio_script = f"{prefixes_ml[chosen_prefix_idx]}{ai_reply}{suffixes_ml[chosen_suffix_idx]}"
            threading.Thread(target=self.speak_native_malayalam, args=(slang_audio_script,), daemon=True).start()
            
        except Exception as e:
            err_msg = "Alley aliya, Ollama background-il on aakkiyittuntoonnu onnu nokke..."
            self.after(0, lambda: self.append_chat("System Scene Aanu", err_msg))
            threading.Thread(target=self.speak_native_malayalam, args=("അല്ലേ അളിയാ ഒല്ലാമ ബാക്ക്ഗ്രൗണ്ടിൽ ഓൺ ആക്കിയിട്ടുണ്ടോ എന്ന് ഒന്ന് നോക്കേ",), daemon=True).start()


if __name__ == "__main__":
    app = BobApp()
    app.mainloop()