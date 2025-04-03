# translations.py
# Contains all text strings for the Whisper GUI application in multiple languages

# Available languages
AVAILABLE_LANGUAGES = {
    "en": "English",
    "it": "Italiano"
}

# All UI strings organized by language
TRANSLATIONS = {
    "en": {
        # Window titles
        "app_title": "Simple Whisper GUI (Auto-Detect Model)",
        "app_title_with_model": "Simple Whisper GUI (Model: {model_name})",
        
        # Model selection
        "select_model": "Select Whisper Model:",
        "ram_info": "System RAM: {ram_gb:.1f} GB",
        "ram_info_with_recommendation": "System RAM: {ram_gb:.1f} GB (Recommended: {model})",
        "ram_info_no_recommendation": "System RAM: {ram_gb:.1f} GB (Could not recommend model)",
        
        # File selection
        "select_audio_file": "Select Audio File",
        "no_file_selected": "No file selected",
        
        # Action buttons
        "load_reload_model": "Load/Reload Model",
        "loading": "Loading...",
        "transcribe": "Transcribe",
        "transcribing": "Transcribing...",
        
        # Status messages
        "status_select_model": "Status: Select a model and click Load/Reload",
        "status_recommended_model": "Status: Recommended model '{model}'. Click 'Load/Reload Model'.",
        "status_ram_detection_failed": "Status: Could not detect RAM. Select model manually and load.",
        "status_model_changed": "Status: Model changed to '{model}'. Click 'Load/Reload Model'.",
        "status_loading_model": "Status: Loading model '{model}'...",
        "status_model_loaded": "Status: Model '{model}' loaded. Ready.",
        "status_model_loaded_select_file": "Status: Model '{model}' loaded. Select file.",
        "status_load_model_or_select_file": "Status: Load model or select file.",
        "status_file_selected": "Status: File selected. Ready to transcribe.",
        "status_transcribing": "Status: Transcribing...",
        "status_transcription_complete": "Status: Transcription Complete ({time:.2f}s)",
        "status_transcription_failed": "Status: Transcription Failed!",
        "status_error_loading_model": "Status: Error loading model '{model}'!",
        
        # Dialog messages
        "dialog_ram_detection_error": "Could not automatically detect system RAM.\n{error}\nPlease select a model manually.",
        "dialog_model_error": "No model selected!",
        "dialog_no_whisper_models": "No Whisper models found!",
        "dialog_model_load_error": "Failed to load Whisper model '{model}'.\nError: {error}\n\nPlease check network connection, disk space, or try a smaller model.",
        "dialog_busy": "Please wait for the current operation to finish.",
        "dialog_no_file": "Please select an audio file first.",
        "dialog_model_not_loaded": "Whisper model is not loaded. Click 'Load/Reload Model'.",
        "dialog_operation_in_progress": "Another operation is already in progress.",
        "dialog_transcription_error": "Transcription Error: {error}",
        
        # File dialog
        "file_dialog_title": "Select Audio or Video File",
        "file_type_audio": "Audio Files",
        "file_type_video": "Video Files",
        "file_type_all": "All Files",
        
        # Transcription
        "transcription_in_progress": "Transcription in progress with model '{model}'...\n",
        "transcription_error": "Error during transcription:\n\n{error}",
        
        # Theme
        "theme_not_available": "Aqua theme not available, using default.",
        
        # Language selection
        "select_language": "Language:"
    },
    
    "it": {
        # Window titles
        "app_title": "Interfaccia Whisper (Rilevamento Automatico Modello)",
        "app_title_with_model": "Interfaccia Whisper (Modello: {model_name})",
        
        # Model selection
        "select_model": "Seleziona Modello Whisper:",
        "ram_info": "RAM di Sistema: {ram_gb:.1f} GB",
        "ram_info_with_recommendation": "RAM di Sistema: {ram_gb:.1f} GB (Consigliato: {model})",
        "ram_info_no_recommendation": "RAM di Sistema: {ram_gb:.1f} GB (Impossibile consigliare un modello)",
        
        # File selection
        "select_audio_file": "Seleziona File Audio",
        "no_file_selected": "Nessun file selezionato",
        
        # Action buttons
        "load_reload_model": "Carica/Ricarica Modello",
        "loading": "Caricamento...",
        "transcribe": "Trascrivi",
        "transcribing": "Trascrivendo...",
        
        # Status messages
        "status_select_model": "Stato: Seleziona un modello e clicca Carica/Ricarica",
        "status_recommended_model": "Stato: Modello consigliato '{model}'. Clicca 'Carica/Ricarica Modello'.",
        "status_ram_detection_failed": "Stato: Impossibile rilevare la RAM. Seleziona manualmente un modello e caricalo.",
        "status_model_changed": "Stato: Modello cambiato a '{model}'. Clicca 'Carica/Ricarica Modello'.",
        "status_loading_model": "Stato: Caricamento modello '{model}'...",
        "status_model_loaded": "Stato: Modello '{model}' caricato. Pronto.",
        "status_model_loaded_select_file": "Stato: Modello '{model}' caricato. Seleziona file.",
        "status_load_model_or_select_file": "Stato: Carica modello o seleziona file.",
        "status_file_selected": "Stato: File selezionato. Pronto per trascrivere.",
        "status_transcribing": "Stato: Trascrivendo...",
        "status_transcription_complete": "Stato: Trascrizione Completata ({time:.2f}s)",
        "status_transcription_failed": "Stato: Trascrizione Fallita!",
        "status_error_loading_model": "Stato: Errore nel caricamento del modello '{model}'!",
        
        # Dialog messages
        "dialog_ram_detection_error": "Impossibile rilevare automaticamente la RAM di sistema.\n{error}\nSeleziona manualmente un modello.",
        "dialog_model_error": "Nessun modello selezionato!",
        "dialog_no_whisper_models": "Nessun modello Whisper trovato!",
        "dialog_model_load_error": "Impossibile caricare il modello Whisper '{model}'.\nErrore: {error}\n\nControlla la connessione di rete, lo spazio su disco o prova un modello più piccolo.",
        "dialog_busy": "Attendi il completamento dell'operazione corrente.",
        "dialog_no_file": "Seleziona prima un file audio.",
        "dialog_model_not_loaded": "Il modello Whisper non è caricato. Clicca 'Carica/Ricarica Modello'.",
        "dialog_operation_in_progress": "Un'altra operazione è già in corso.",
        "dialog_transcription_error": "Errore di Trascrizione: {error}",
        
        # File dialog
        "file_dialog_title": "Seleziona File Audio o Video",
        "file_type_audio": "File Audio",
        "file_type_video": "File Video",
        "file_type_all": "Tutti i File",
        
        # Transcription
        "transcription_in_progress": "Trascrizione in corso con il modello '{model}'...\n",
        "transcription_error": "Errore durante la trascrizione:\n\n{error}",
        
        # Theme
        "theme_not_available": "Tema Aqua non disponibile, usando il tema predefinito.",
        
        # Language selection
        "select_language": "Lingua:"
    }
}


def get_text(language_code, key, **kwargs):
    """
    Get a translated string for the given language and key.
    Supports format string parameters through kwargs.
    Falls back to English if the key or language is not found.
    """
    # Default to English if language not available
    if language_code not in TRANSLATIONS:
        language_code = "en"
        
    # Get the translations dictionary for the language
    translations = TRANSLATIONS[language_code]
    
    # Get the string, defaulting to English if not found
    text = translations.get(key, TRANSLATIONS["en"].get(key, f"Missing translation: {key}"))
    
    # Apply any format string parameters
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError as e:
            print(f"Warning: Missing format parameter {e} for key '{key}'")
    
    return text