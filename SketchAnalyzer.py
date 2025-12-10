"""
Sketch Analyzer - Uses Qwen2-VL-2B model to analyze sketches
Based on official Qwen2-VL example code
"""

import base64
from io import BytesIO
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from PIL import Image
import torch

# Global model cache (shared across workers)
_model_cache = None
_processor_cache = None

class SketchAnalyzerWorker(QThread):
    """Worker thread for running the model inference."""
    
    finished = pyqtSignal(str)  # story
    error = pyqtSignal(str)  # error message
    status = pyqtSignal(str)  # status update
    
    def __init__(self, image_base64, prompt):
        super().__init__()
        self.image_base64 = image_base64
        self.prompt = prompt
    
    def run(self):
        """Run the analysis in a separate thread."""
        try:
            self.status.emit("Loading model...")
            
            # Import here to avoid blocking main thread during import
            from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
            from qwen_vl_utils import process_vision_info
            
            global _model_cache, _processor_cache
            
            # Load model if not already cached (shared across workers)
            if _model_cache is None:
                model_name = "Qwen/Qwen2-VL-2B-Instruct"
                
                self.status.emit("Downloading/loading model (first time may take a while)...")
                _processor_cache = AutoProcessor.from_pretrained(
                    model_name,
                    trust_remote_code=True
                )
                
                self.status.emit("Loading model into memory...")
                _model_cache = Qwen2VLForConditionalGeneration.from_pretrained(
                    model_name,
                    device_map="auto",
                    trust_remote_code=True,
                    load_in_4bit=True  # Critical for low RAM
                )
            
            model = _model_cache
            processor = _processor_cache
            
            # Decode base64 image
            self.status.emit("Processing image...")
            image_data = base64.b64decode(self.image_base64)
            image = Image.open(BytesIO(image_data)).convert("RGB")
            
            # Format input (Qwen2-VL uses conversation-style input)
            # Match official example format exactly
            # messages = [
            #     {"role": "system", "content": ""}, 
            #     {
            #         "role": "user",
            #         "content": [
            #             {"type": "image", "image": image},
            #             {"type": "text", "text": self.prompt}
            #         ]
            #     }
            # ]

            messages = [
                {
                    "role": "system",
                    "content": "You are “Drawlingo”, a friendly art and language teacher for English-speaking children learning German.\n\nAlways speak to the child directly in a warm, simple way.\n\nFor EVERY answer, follow EXACTLY this 3-line structure:\n\n1) A short praise + English description of what the child drew, in English.\n2) On a single line: English noun, space, comma, space, then the German noun with a capital letter. Example: \"Tree, Baum.\"\n3) One short sentence in simple German that describes the drawing, talking to the child. Example: \"Du hast einen schönen Baum gemalt!\"\n\nRules:\n- Use ONLY English and German.\n- Do not explain grammar.\n- Do not translate the German sentence back to English.\n- No bullet points, no numbering in the output. Just three plain lines of text.\n- If there are several objects, pick ONE main object to teach."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image},
                        {"type": "text", "text": "Talk to the child following the 3-line structure."}
                    ]
                }
            ]

            
            # Prepare inputs - following official example
            self.status.emit("Preparing inputs...")
            text = processor.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            image_inputs, _ = process_vision_info(messages)
            
            # Determine device (CUDA if available, else CPU)
            device = "cuda" if torch.cuda.is_available() else "cpu"
            
            inputs = processor(
                text=[text],
                images=image_inputs,
                return_tensors="pt"
            ).to(device)
            
            # Generate
            self.status.emit("Generating story...")
            with torch.no_grad():
                output = model.generate(**inputs, max_new_tokens=500, temperature=0.7)
            
            # Decode - match official example exactly
            result = processor.batch_decode(output, skip_special_tokens=True)[0]
            story = result.split("ASSISTANT:")[-1].strip()
            
            # Fallback if ASSISTANT: marker not found
            if not story:
                story = result.strip()
            
            self.status.emit("Story generated successfully!")
            self.finished.emit(story)
            
        except ImportError as e:
            error_msg = (
                f"Missing Python dependencies. Please install:\n"
                f"pip install transformers accelerate torch torchvision pillow bitsandbytes qwen-vl-utils\n"
                f"Error: {str(e)}"
            )
            self.error.emit(error_msg)
        except Exception as e:
            error_msg = f"Analysis failed: {str(e)}"
            self.error.emit(error_msg)


class SketchAnalyzer(QObject):
    """Analyzer class that manages sketch analysis using Qwen2-VL model."""
    
    analysisComplete = pyqtSignal(str)  # story
    analysisError = pyqtSignal(str)  # error message
    statusUpdate = pyqtSignal(str)  # status update
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
    
    def analyzeSketch(self, pixmap):
        """Analyze a sketch and generate a story."""
        # Convert QPixmap to base64
        image_base64 = self.pixmapToBase64(pixmap)
        if not image_base64:
            self.analysisError.emit("Failed to encode image.")
            return
        
        # Generate prompt
        prompt = self.generatePrompt()
        # INSERT_YOUR_CODE
        # Get the user-input prompt from the UI, if available; fallback to generatePrompt()
        parent_widget = self.parent()
        if parent_widget and hasattr(parent_widget, "getCustomPrompt"):
            user_prompt = parent_widget.getCustomPrompt()
            if user_prompt and user_prompt.strip():
                prompt = user_prompt.strip()
            else:
                prompt = self.generatePrompt()
        else:
            prompt = self.generatePrompt()

        
        # Cancel any existing worker
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        
        # Create and start worker thread
        self.worker = SketchAnalyzerWorker(image_base64, prompt)
        self.worker.finished.connect(self.analysisComplete.emit)
        self.worker.error.connect(self.analysisError.emit)
        self.worker.status.connect(self.statusUpdate.emit)
        self.worker.start()
    
    def pixmapToBase64(self, pixmap):
        """Convert QPixmap to base64 string."""
        from PyQt6.QtCore import QBuffer, QIODevice
        
        byte_array = QBuffer()
        byte_array.open(QIODevice.OpenModeFlag.WriteOnly)
        
        if not pixmap.save(byte_array, "PNG"):
            return None
        
        data = byte_array.data()
        return base64.b64encode(data).decode('utf-8')
    
    def generatePrompt(self):
        """Generate the prompt for story generation."""
        return (
            "Describe the sketch in easy English in 3 short sentences."
            "Then translate the English sentences to German."
            "Do not add any other response."
        )
        # return (
        #     "Use simple sentences in English to describe the objects in the sketch."
        #     "Example: This is a dog. The dog loves the ball."
        #     "Format your response as:\n\n"
        #     "English: This/These is/are {amount} {object}\n\n"
        #     "Translate the sentence into German for German learners.\n\n"
        #     "German: Das/Die/Der/Diese/Dieser ist/sind {amount} {object}\n\n"
        # )

