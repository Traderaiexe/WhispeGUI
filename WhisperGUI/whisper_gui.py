import tkinter as tk
from tkinter import ttk # Using themed widgets for a slightly nicer look
from tkinter import filedialog, scrolledtext, messagebox
import whisper
import threading
import os
import time
import psutil # Import psutil to check system resources

# Import translations
from translations import get_text, AVAILABLE_LANGUAGES

# --- Model RAM Requirements (Approximate Guide) ---
# These are rough estimates, actual usage can vary.
# We leave some headroom for the OS and other apps.
MODEL_RAM_REQUIREMENTS = {
    # model_name: min_system_ram_gb_required
    "tiny": 2,
    "base": 2.5,
    "small": 4,
    "medium": 8,
    "large": 12, # large-v2/v3 might need slightly more
    # Add .en models if desired, they often use slightly less RAM
    "tiny.en": 1.8,
    "base.en": 2.2,
    "small.en": 3.5,
    "medium.en": 7,
}
# Get all available models from Whisper itself
ALL_AVAILABLE_MODELS = whisper.available_models()
# Prioritize standard models in the dropdown list if they exist
PRIORITY_MODELS = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]
SORTED_MODELS = sorted(
    ALL_AVAILABLE_MODELS,
    key=lambda x: (PRIORITY_MODELS.index(x) if x in PRIORITY_MODELS else float('inf'), x)
)


class WhisperGUI:
    def __init__(self, root):
        self.root = root
        self.language = tk.StringVar(root, value="en") # Default language is English
        self.root.title(get_text(self.language.get(), "app_title"))
        self.root.geometry("650x550") # Adjusted size slightly

        self.model = None
        self.selected_file_path = None
        self.is_transcribing = False
        self.is_loading_model = False

        # --- System Info & Model Recommendation ---
        self.system_ram_gb = self.get_system_ram_gb()
        self.recommended_model = self.recommend_model(self.system_ram_gb)
        self.selected_model_var = tk.StringVar(root)

        # --- GUI Elements ---
        # Language Selection Frame
        self.lang_frame = ttk.Frame(root, padding="5")
        self.lang_frame.pack(fill=tk.X)
        
        ttk.Label(self.lang_frame, text=get_text(self.language.get(), "select_language")).pack(side=tk.LEFT, padx=(0, 5))
        
        # Create language dropdown
        self.lang_menu = ttk.OptionMenu(
            self.lang_frame,
            self.language,
            self.language.get(),
            *AVAILABLE_LANGUAGES.keys(),
            command=self.on_language_change
        )
        self.lang_menu.pack(side=tk.LEFT, padx=5)
        
        # Display language names instead of codes
        self.lang_menu.config(width=10)
        
        # Model Selection Frame
        self.model_frame = ttk.Frame(root, padding="10")
        self.model_frame.pack(fill=tk.X)

        ttk.Label(self.model_frame, text=get_text(self.language.get(), "select_model")).pack(side=tk.LEFT, padx=(0, 5))

        self.model_option_menu = ttk.OptionMenu(
            self.model_frame,
            self.selected_model_var,
            self.recommended_model, # Default selection
            *SORTED_MODELS,         # Populate with available models
            command=self.on_model_selection_change # Trigger reload on change
        )
        self.model_option_menu.pack(side=tk.LEFT, padx=5)
        self.model_option_menu.config(width=15)

        # Display system RAM and recommendation
        if self.recommended_model:
            ram_info_text = get_text(self.language.get(), "ram_info_with_recommendation", ram_gb=self.system_ram_gb, model=self.recommended_model)
        else:
            ram_info_text = get_text(self.language.get(), "ram_info_no_recommendation", ram_gb=self.system_ram_gb)

        self.ram_label = ttk.Label(self.model_frame, text=ram_info_text, foreground="gray")
        self.ram_label.pack(side=tk.LEFT, padx=10)


        # File Selection Frame
        self.file_frame = ttk.Frame(root, padding="5 10 5 10") # top right bottom left
        self.file_frame.pack(fill=tk.X)

        self.select_button = ttk.Button(self.file_frame, text=get_text(self.language.get(), "select_audio_file"), command=self.select_file, width=18)
        self.select_button.pack(side=tk.LEFT, padx=(0, 10))

        self.file_label = ttk.Label(self.file_frame, text=get_text(self.language.get(), "no_file_selected"), foreground="grey", anchor="w", width=40, wraplength=350) # Limit width
        self.file_label.pack(side=tk.LEFT, fill=tk.X, expand=True)


        # Action Buttons Frame
        self.action_frame = ttk.Frame(root, padding="5 10")
        self.action_frame.pack(fill=tk.X)

        self.load_button = ttk.Button(self.action_frame, text=get_text(self.language.get(), "load_reload_model"), command=self.load_model, width=18)
        self.load_button.pack(side=tk.LEFT, padx=(0,10))

        self.transcribe_button = ttk.Button(self.action_frame, text=get_text(self.language.get(), "transcribe"), command=self.start_transcription_thread, state=tk.DISABLED, width=18)
        self.transcribe_button.pack(side=tk.LEFT)

        # Status Label
        self.status_label = ttk.Label(root, text=get_text(self.language.get(), "status_select_model"), foreground="blue", padding="0 5 0 10", anchor='w') # Pad left
        self.status_label.pack(fill=tk.X)

        # Output Text Area
        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, width=75)
        self.output_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.output_text.configure(state='disabled') # Make it read-only initially

        # --- Initial State ---
        self.update_widget_states() # Set initial button states
        if self.recommended_model:
            self.status_label.config(text=get_text(self.language.get(), "status_recommended_model", model=self.recommended_model))
        else:
            self.status_label.config(text=get_text(self.language.get(), "status_ram_detection_failed"), foreground="orange")


    def on_language_change(self, *args):
        """Called when the user changes the language."""
        # Update all UI text elements with the new language
        self.update_ui_texts()
    
    def update_ui_texts(self):
        """Updates all UI text elements with the current language."""
        lang = self.language.get()
        
        # Update window title
        if self.model:
            self.root.title(get_text(lang, "app_title_with_model", model_name=self.selected_model_var.get()))
        else:
            self.root.title(get_text(lang, "app_title"))
        
        # Update labels and buttons
        self.lang_frame.winfo_children()[0].config(text=get_text(lang, "select_language"))
        self.model_frame.winfo_children()[0].config(text=get_text(lang, "select_model"))
        
        # Update RAM info text
        if self.recommended_model:
            ram_info_text = get_text(lang, "ram_info_with_recommendation", ram_gb=self.system_ram_gb, model=self.recommended_model)
        else:
            ram_info_text = get_text(lang, "ram_info_no_recommendation", ram_gb=self.system_ram_gb)
        self.ram_label.config(text=ram_info_text)
        
        # Update file selection elements
        self.select_button.config(text=get_text(lang, "select_audio_file"))
        if not self.selected_file_path:
            self.file_label.config(text=get_text(lang, "no_file_selected"))
        
        # Update action buttons
        if self.is_loading_model:
            self.load_button.config(text=get_text(lang, "loading"))
        else:
            self.load_button.config(text=get_text(lang, "load_reload_model"))
            
        if self.is_transcribing:
            self.transcribe_button.config(text=get_text(lang, "transcribing"))
        else:
            self.transcribe_button.config(text=get_text(lang, "transcribe"))
        
        # Update status label - preserve the current status message by reconstructing it
        current_text = self.status_label.cget("text")
        if "Recommended model" in current_text and self.recommended_model:
            self.status_label.config(text=get_text(lang, "status_recommended_model", model=self.recommended_model))
        elif "Could not detect RAM" in current_text:
            self.status_label.config(text=get_text(lang, "status_ram_detection_failed"))
        elif "Model changed to" in current_text and self.selected_model_var.get():
            self.status_label.config(text=get_text(lang, "status_model_changed", model=self.selected_model_var.get()))
        elif "Loading model" in current_text and self.selected_model_var.get():
            self.status_label.config(text=get_text(lang, "status_loading_model", model=self.selected_model_var.get()))
        elif "Model" in current_text and "loaded" in current_text and self.selected_model_var.get():
            self.status_label.config(text=get_text(lang, "status_model_loaded", model=self.selected_model_var.get()))
        elif "File selected" in current_text:
            self.status_label.config(text=get_text(lang, "status_file_selected"))
        elif "Transcribing" in current_text:
            self.status_label.config(text=get_text(lang, "status_transcribing"))
        elif "Transcription Complete" in current_text:
            # Extract time from the status message if possible
            import re
            time_match = re.search(r"\((\d+\.\d+)s\)", current_text)
            time_value = float(time_match.group(1)) if time_match else 0.0
            self.status_label.config(text=get_text(lang, "status_transcription_complete", time=time_value))
        elif "Transcription Failed" in current_text:
            self.status_label.config(text=get_text(lang, "status_transcription_failed"))
        elif "Error loading model" in current_text and self.selected_model_var.get():
            self.status_label.config(text=get_text(lang, "status_error_loading_model", model=self.selected_model_var.get()))
        else:
            # Default status message
            self.status_label.config(text=get_text(lang, "status_select_model"))
    
    def get_system_ram_gb(self):
        """Gets total system physical RAM in Gigabytes."""
        try:
            ram_bytes = psutil.virtual_memory().total
            ram_gb = ram_bytes / (1024**3)
            return ram_gb
        except Exception as e:
            print(f"Error getting system RAM: {e}")
            messagebox.showwarning(get_text(self.language.get(), "dialog_ram_detection_error").split("\n")[0], 
                                  get_text(self.language.get(), "dialog_ram_detection_error", error=str(e)))
            return 0 # Indicate failure

    def recommend_model(self, ram_gb):
        """Recommends a Whisper model based on available RAM."""
        if ram_gb <= 0:
            return "tiny" # Default fallback if RAM detection failed

        # Try to find the largest model that fits within RAM constraints
        # Iterate from largest requirement downwards
        sorted_requirements = sorted(MODEL_RAM_REQUIREMENTS.items(), key=lambda item: item[1], reverse=True)

        # Add some buffer (e.g., 1-2 GB) for OS and other apps
        available_ram_for_model = ram_gb - 1.5 # Adjust buffer as needed

        recommended = "tiny" # Default to smallest
        for model, req_ram in sorted_requirements:
            if available_ram_for_model >= req_ram and model in ALL_AVAILABLE_MODELS:
                 recommended = model
                 break # Found the best fit

        # If even tiny doesn't fit (low RAM system), still recommend tiny
        if available_ram_for_model < MODEL_RAM_REQUIREMENTS.get("tiny", 2) and "tiny" in ALL_AVAILABLE_MODELS:
             recommended = "tiny"
        elif recommended not in ALL_AVAILABLE_MODELS and "tiny" in ALL_AVAILABLE_MODELS:
             # Fallback if calculated recommendation isn't actually available
             recommended = "tiny"
        elif not ALL_AVAILABLE_MODELS:
             messagebox.showerror(get_text(self.language.get(), "dialog_model_error"), 
                                get_text(self.language.get(), "dialog_no_whisper_models"))
             return None

        print(f"System RAM: {ram_gb:.1f} GB, Available for model (estimated): {available_ram_for_model:.1f} GB -> Recommended: {recommended}")
        return recommended


    def update_widget_states(self):
        """Central function to enable/disable widgets based on current state."""
        lang = self.language.get()
        
        # Model loading state
        if self.is_loading_model:
            self.load_button.config(state=tk.DISABLED, text=get_text(lang, "loading"))
            self.model_option_menu.config(state=tk.DISABLED)
            self.select_button.config(state=tk.DISABLED)
            self.transcribe_button.config(state=tk.DISABLED)
            return # Loading overrides other states

        # Reset load button text if not loading
        self.load_button.config(text=get_text(lang, "load_reload_model"), state=tk.NORMAL)
        self.model_option_menu.config(state=tk.NORMAL)

        # Transcription state
        if self.is_transcribing:
            self.select_button.config(state=tk.DISABLED)
            self.transcribe_button.config(state=tk.DISABLED, text=get_text(lang, "transcribing"))
            self.load_button.config(state=tk.DISABLED) # Don't reload model during transcription
            self.model_option_menu.config(state=tk.DISABLED)
            return # Transcribing overrides other states

        # Reset transcribe button text if not transcribing
        self.transcribe_button.config(text=get_text(lang, "transcribe"))

        # Default states (not loading, not transcribing)
        self.select_button.config(state=tk.NORMAL)

        # Transcribe button requires model loaded AND file selected
        if self.model and self.selected_file_path:
            self.transcribe_button.config(state=tk.NORMAL)
        else:
            self.transcribe_button.config(state=tk.DISABLED)


    def on_model_selection_change(self, selected_model):
        """Called when the user selects a different model in the OptionMenu."""
        print(f"Model selection changed to: {selected_model}")
        # Simple approach: Just update status, require user to click "Load/Reload"
        self.status_label.config(text=get_text(self.language.get(), "status_model_changed", model=selected_model), fg="blue")
        self.model = None # Invalidate the currently loaded model
        self.update_widget_states() # Disable transcribe button until reloaded

        # Optional: Automatically trigger reload (might be slow/unexpected for user)
        # self.load_model()


    def load_model(self):
        """Loads the Whisper model selected in the OptionMenu."""
        if self.is_loading_model or self.is_transcribing:
            return # Avoid concurrent loads/actions

        selected_model_name = self.selected_model_var.get()
        if not selected_model_name:
             messagebox.showerror(get_text(self.language.get(), "dialog_model_error"), 
                                get_text(self.language.get(), "dialog_model_error"))
             return

        self.is_loading_model = True
        self.model = None # Clear previous model
        self.update_widget_states()
        self.status_label.config(text=get_text(self.language.get(), "status_loading_model", model=selected_model_name), fg="orange")
        self.root.update_idletasks()

        threading.Thread(target=self._load_model_task, args=(selected_model_name,), daemon=True).start()

    def _load_model_task(self, model_name):
        """The actual model loading task."""
        try:
            print(f"Attempting to load model: {model_name}")
            loaded_model = whisper.load_model(model_name)
            # Schedule GUI update back on the main thread
            self.root.after(0, self._on_model_loaded, loaded_model, model_name)
        except Exception as e:
            # Schedule error message display back on the main thread
            print(f"Error loading model {model_name}: {e}")
            self.root.after(0, self._on_model_load_error, str(e), model_name)

    def _on_model_loaded(self, loaded_model, model_name):
        """Callback run in the main thread after model is loaded."""
        self.model = loaded_model
        self.is_loading_model = False
        self.status_label.config(text=get_text(self.language.get(), "status_model_loaded", model=model_name), fg="green")
        self.root.title(get_text(self.language.get(), "app_title_with_model", model_name=model_name)) # Update window title
        self.update_widget_states()
        print(f"Whisper model '{model_name}' loaded successfully.")

    def _on_model_load_error(self, error_message, model_name):
        """Callback run in the main thread if model loading fails."""
        self.model = None
        self.is_loading_model = False
        self.status_label.config(text=get_text(self.language.get(), "status_error_loading_model", model=model_name), fg="red")
        self.update_widget_states() # Re-enable widgets
        messagebox.showerror(get_text(self.language.get(), "dialog_model_load_error").split("\n")[0], 
                             get_text(self.language.get(), "dialog_model_load_error", model=model_name, error=error_message))


    def select_file(self):
        """Opens a file dialog to select an audio file."""
        if self.is_transcribing or self.is_loading_model:
            messagebox.showwarning(get_text(self.language.get(), "dialog_busy").split(".")[0], 
                                  get_text(self.language.get(), "dialog_busy"))
            return

        filetypes = (
            (get_text(self.language.get(), "file_type_audio"), '*.mp3 *.wav *.m4a *.flac *.ogg *.aac *.opus *.mpga'), # Added mpga
            (get_text(self.language.get(), "file_type_video"), '*.mp4 *.mov *.avi *.mkv'), # Whisper can often handle video too
            (get_text(self.language.get(), "file_type_all"), '*.*')
        )
        filepath = filedialog.askopenfilename(
            title=get_text(self.language.get(), "file_dialog_title"),
            filetypes=filetypes
        )
        if filepath:
            self.selected_file_path = filepath
            filename = os.path.basename(filepath)
            self.file_label.config(text=filename, foreground="black")
            self.output_text.configure(state='normal')
            self.output_text.delete(1.0, tk.END)
            self.output_text.configure(state='disabled')
            self.status_label.config(text=get_text(self.language.get(), "status_file_selected"), fg="blue")
        else:
            if not self.selected_file_path: # Only reset if no file was previously selected
                 self.file_label.config(text=get_text(self.language.get(), "no_file_selected"), foreground="grey")
                 if self.model:
                     self.status_label.config(text=get_text(self.language.get(), "status_model_loaded_select_file", model=self.selected_model_var.get()), fg="blue")
                 else:
                     self.status_label.config(text=get_text(self.language.get(), "status_load_model_or_select_file"), fg="blue")

        self.update_widget_states() # Update button states based on file selection


    def start_transcription_thread(self):
        """Starts the transcription process in a separate thread."""
        if not self.selected_file_path:
            messagebox.showwarning(get_text(self.language.get(), "dialog_no_file").split(".")[0], 
                                  get_text(self.language.get(), "dialog_no_file"))
            return
        if not self.model:
             messagebox.showerror(get_text(self.language.get(), "dialog_model_not_loaded").split(".")[0], 
                                get_text(self.language.get(), "dialog_model_not_loaded"))
             return
        if self.is_transcribing or self.is_loading_model:
             messagebox.showwarning(get_text(self.language.get(), "dialog_operation_in_progress").split(".")[0], 
                                  get_text(self.language.get(), "dialog_operation_in_progress"))
             return

        self.is_transcribing = True
        self.update_widget_states() # Disable buttons etc.
        self.status_label.config(text=get_text(self.language.get(), "status_transcribing"), fg="orange")
        self.output_text.configure(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, get_text(self.language.get(), "transcription_in_progress", model=self.selected_model_var.get()))
        self.output_text.configure(state='disabled')
        self.root.update_idletasks()

        threading.Thread(target=self._perform_transcription, daemon=True).start()

    def _perform_transcription(self):
        """The actual transcription work done in the background thread."""
        try:
            start_time = time.time()
            current_model = self.model # Use the model stored in the instance
            file_to_transcribe = self.selected_file_path
            print(f"Starting transcription for: {file_to_transcribe}")

            # --- Perform Transcription ---
            # fp16=False is generally safer for CPU and potentially Apple Silicon MPS
            # You might expose options like language detection later
            result = current_model.transcribe(file_to_transcribe, fp16=False)
            # ---------------------------

            end_time = time.time()
            elapsed_time = end_time - start_time
            transcription_text = result["text"]

            # Schedule GUI update back on the main thread
            self.root.after(0, self._update_gui_with_result, transcription_text, elapsed_time)

        except Exception as e:
            # Schedule error display back on the main thread
            error_message = f"Transcription Error: {e}"
            print(error_message) # Also print to console for debugging
            self.root.after(0, self._update_gui_with_error, error_message)
        finally:
            # Ensure state is reset even if errors occur (scheduled for main thread)
             self.root.after(0, self._reset_transcription_state)


    def _update_gui_with_result(self, text, elapsed_time):
        """Updates the GUI text area with the result (runs in main thread)."""
        self.output_text.configure(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.configure(state='disabled')
        self.status_label.config(text=get_text(self.language.get(), "status_transcription_complete", time=elapsed_time), fg="green")

    def _update_gui_with_error(self, error_message):
        """Updates the GUI with an error message (runs in main thread)."""
        self.output_text.configure(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, get_text(self.language.get(), "transcription_error", error=error_message))
        self.output_text.configure(state='disabled')
        self.status_label.config(text=get_text(self.language.get(), "status_transcription_failed"), fg="red")
        messagebox.showerror(get_text(self.language.get(), "dialog_transcription_error").split(":")[0], error_message)


    def _reset_transcription_state(self):
        """Resets buttons and status after transcription (runs in main thread)."""
        self.is_transcribing = False
        self.update_widget_states() # Re-enable relevant widgets


# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    # Optional: Apply a theme for a slightly more modern look on macOS
    style = ttk.Style(root)
    try:
        # 'aqua' is the default macOS theme and usually works well
        style.theme_use('aqua')
    except tk.TclError:
        print(get_text("en", "theme_not_available")) # Use English for console messages

    app = WhisperGUI(root)
    root.mainloop()