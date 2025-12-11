"""
Main Window - Main UI for Drawlingo application
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QProgressBar, QMessageBox, QApplication, QLineEdit, QButtonGroup
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QTextCursor, QColor
from DrawingCanvas import DrawingCanvas
from SketchAnalyzer import SketchAnalyzer

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.m_centralWidget = None
        self.m_textArea = None
        self.m_canvas = None
        self.m_analyzeButton = None
        self.m_separatorLabel = None
        self.m_progressBar = None
        self.m_statusLabel = None
        self.m_analyzer = None
        self.m_customPromptInput = None
        self.m_penButton = None
        self.m_eraserButton = None
        self.m_toolButtonGroup = None
        
        self.setupUI()
        
        # Initialize analyzer
        self.m_analyzer = SketchAnalyzer(self)
        self.m_analyzer.analysisComplete.connect(self.onAnalysisComplete)
        self.m_analyzer.analysisError.connect(self.onAnalysisError)
        self.m_analyzer.statusUpdate.connect(self.onStatusUpdate)
        
        self.setWindowTitle("Drawlingo - Sketch Language Learning")
        self.resize(1200, 700)
    
    def setupUI(self):
        """Set up the user interface."""
        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(0)
        
        # Left side container (prompt input + text area)
        leftSideWidget = QWidget(self)
        leftSideLayout = QVBoxLayout(leftSideWidget)
        leftSideLayout.setContentsMargins(0, 0, 0, 0)
        leftSideLayout.setSpacing(10)
        
        # Custom prompt input
        promptLabel = QLabel("Custom Prompt (optional):", self)
        promptLabel.setStyleSheet(
            "QLabel {"
            "    font-size: 13px;"
            "    font-weight: bold;"
            "    color: white;"
            "}"
        )
        
        self.m_customPromptInput = QLineEdit(self)
        self.m_customPromptInput.setPlaceholderText("Enter a custom prompt for the story generation (leave empty to use default)...")
        self.m_customPromptInput.setStyleSheet(
            "QLineEdit {"
            "    font-size: 13px;"
            "    padding: 8px;"
            "    border: 2px solid #e0e0e0;"
            "    border-radius: 6px;"
            "    background-color: #000000;"
            "    color: #ffffff;"
            "}"
            "QLineEdit:focus {"
            "    border: 2px solid #4CAF50;"
            "}"
        )
        
        leftSideLayout.addWidget(promptLabel)
        leftSideLayout.addWidget(self.m_customPromptInput)
        
        # Text area on the left (for generated story)
        self.m_textArea = QTextEdit(self)
        self.m_textArea.setReadOnly(True)
        self.m_textArea.setPlaceholderText("Your story will appear here...")
        self.m_textArea.setStyleSheet(
            "QTextEdit {"
            "    font-size: 16px;"
            "    padding: 15px;"
            "    border: 2px solid #e0e0e0;"
            "    border-radius: 8px;"
            "    background-color: #000000;"
            "    color: #ffffff;"
            "}"
        )
        leftSideLayout.addWidget(self.m_textArea, 1)
        
        # Separator with arrow button
        separatorWidget = QWidget(self)
        separatorWidget.setFixedWidth(80)
        separatorLayout = QVBoxLayout(separatorWidget)
        separatorLayout.setContentsMargins(0, 0, 0, 0)
        separatorLayout.setSpacing(0)
        
        # Vertical line
        self.m_separatorLabel = QLabel(self)
        self.m_separatorLabel.setFixedWidth(2)
        self.m_separatorLabel.setStyleSheet("background-color: #cccccc;")
        
        # Arrow button pointing from canvas to text area
        self.m_analyzeButton = QPushButton("←", self)
        self.m_analyzeButton.setFixedSize(50, 50)
        self.m_analyzeButton.setStyleSheet(
            "QPushButton {"
            "    font-size: 24px;"
            "    font-weight: bold;"
            "    background-color: #4CAF50;"
            "    color: white;"
            "    border: none;"
            "    border-radius: 25px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #45a049;"
            "}"
            "QPushButton:pressed {"
            "    background-color: #3d8b40;"
            "}"
            "QPushButton:disabled {"
            "    background-color: #cccccc;"
            "}"
        )
        self.m_analyzeButton.clicked.connect(self.onAnalyzeButtonClicked)
        
        separatorLayout.addStretch()
        separatorLayout.addWidget(self.m_analyzeButton, 0, Qt.AlignmentFlag.AlignCenter)
        separatorLayout.addStretch()
        
        # Right side container (toolbar + canvas)
        rightSideWidget = QWidget(self)
        rightSideLayout = QVBoxLayout(rightSideWidget)
        rightSideLayout.setContentsMargins(0, 0, 0, 0)
        rightSideLayout.setSpacing(10)
        
        # Create canvas FIRST before toolbar buttons that reference it
        self.m_canvas = DrawingCanvas(self)
        self.m_canvas.setMinimumSize(400, 400)
        self.m_canvas.setStyleSheet(
            "DrawingCanvas {"
            "    border: 2px solid #e0e0e0;"
            "    border-radius: 8px;"
            "    background-color: white;"
            "}"
        )
        
        # Toolbar for drawing tools
        toolbarLayout = QHBoxLayout()
        toolbarLayout.setSpacing(5)
        
        # Tool selection label
        toolLabel = QLabel("Tools:", self)
        toolLabel.setStyleSheet("QLabel { font-size: 12px; font-weight: bold; }")
        toolbarLayout.addWidget(toolLabel)
        
        # Pen button
        self.m_penButton = QPushButton("✏️ Pen", self)
        self.m_penButton.setCheckable(True)
        self.m_penButton.setChecked(True)
        self.m_penButton.setStyleSheet(
            "QPushButton {"
            "    padding: 6px 12px;"
            "    font-size: 12px;"
            "    border: 2px solid #cccccc;"
            "    border-radius: 4px;"
            "    background-color: white;"
            "    color: #333333;"
            "}"
            "QPushButton:checked {"
            "    background-color: #4CAF50;"
            "    color: white;"
            "    border-color: #4CAF50;"
            "}"
            "QPushButton:hover {"
            "    background-color: #f0f0f0;"
            "}"
        )
        self.m_penButton.clicked.connect(lambda: self.m_canvas.setTool(DrawingCanvas.TOOL_PEN))
        
        # Eraser button
        self.m_eraserButton = QPushButton("🧹 Eraser", self)
        self.m_eraserButton.setCheckable(True)
        self.m_eraserButton.setStyleSheet(
            "QPushButton {"
            "    padding: 6px 12px;"
            "    font-size: 12px;"
            "    border: 2px solid #cccccc;"
            "    border-radius: 4px;"
            "    background-color: white;"
            "    color: #333333;"
            "}"
            "QPushButton:checked {"
            "    background-color: #4CAF50;"
            "    color: white;"
            "    border-color: #4CAF50;"
            "}"
            "QPushButton:hover {"
            "    background-color: #f0f0f0;"
            "}"
        )
        self.m_eraserButton.clicked.connect(lambda: self.m_canvas.setTool(DrawingCanvas.TOOL_ERASER))
        
        # Tool button group (mutually exclusive)
        self.m_toolButtonGroup = QButtonGroup(self)
        self.m_toolButtonGroup.addButton(self.m_penButton, DrawingCanvas.TOOL_PEN)
        self.m_toolButtonGroup.addButton(self.m_eraserButton, DrawingCanvas.TOOL_ERASER)
        self.m_toolButtonGroup.buttonClicked.connect(self.onToolChanged)
        
        toolbarLayout.addWidget(self.m_penButton)
        toolbarLayout.addWidget(self.m_eraserButton)
        toolbarLayout.addStretch()
        
        # Color selection label
        colorLabel = QLabel("Colors:", self)
        colorLabel.setStyleSheet("QLabel { font-size: 12px; font-weight: bold; }")
        toolbarLayout.addWidget(colorLabel)
        
        # Color buttons
        colors = [
            ("Black", Qt.GlobalColor.black),
            ("Red", Qt.GlobalColor.red),
            ("Blue", Qt.GlobalColor.blue),
            ("Green", Qt.GlobalColor.green),
            ("Yellow", Qt.GlobalColor.yellow),
            ("Orange", QColor(255, 165, 0)),
            ("Purple", QColor(128, 0, 128)),
            ("Pink", QColor(255, 192, 203)),
        ]
        
        self.m_colorButtons = []
        for (color_name, color) in colors:
            colorBtn = QPushButton("", self)
            colorBtn.setFixedSize(30, 30)
            colorBtn.setCheckable(True)
            if color == Qt.GlobalColor.black:
                colorBtn.setChecked(True)
            # Convert color to QColor for name() method
            qcolor = QColor(color) if not isinstance(color, QColor) else color
            colorBtn.setStyleSheet(
                f"QPushButton {{"
                f"    background-color: {qcolor.name()};"
                f"    border: 2px solid #cccccc;"
                f"    border-radius: 15px;"
                f"}}"
                f"QPushButton:checked {{"
                f"    border: 3px solid #4CAF50;"
                f"}}"
                f"QPushButton:hover {{"
                f"    border: 2px solid #333333;"
                f"}}"
            )
            colorBtn.clicked.connect(lambda checked, c=color: self.m_canvas.setColor(c))
            self.m_colorButtons.append(colorBtn)
            toolbarLayout.addWidget(colorBtn)
        
        toolbarLayout.addStretch()
        
        # Clear button
        clearButton = QPushButton("🗑️ Clear", self)
        clearButton.setStyleSheet(
            "QPushButton {"
            "    padding: 6px 12px;"
            "    font-size: 12px;"
            "    border: 2px solid #f44336;"
            "    border-radius: 4px;"
            "    background-color: white;"
            "    color: #f44336;"
            "}"
            "QPushButton:hover {"
            "    background-color: #f44336;"
            "    color: white;"
            "}"
        )
        clearButton.clicked.connect(self.m_canvas.clearCanvas)
        toolbarLayout.addWidget(clearButton)
        
        rightSideLayout.addLayout(toolbarLayout)
        rightSideLayout.addWidget(self.m_canvas, 1)
        
        # Progress bar with text
        self.m_progressBar = QProgressBar(self)
        self.m_progressBar.setVisible(False)
        self.m_progressBar.setTextVisible(True)
        self.m_progressBar.setFormat("%p% - %v")
        self.m_progressBar.setStyleSheet(
            "QProgressBar {"
            "    border: 1px solid #cccccc;"
            "    border-radius: 4px;"
            "    background-color: #f0f0f0;"
            "    text-align: center;"
            "    font-size: 12px;"
            "    color: #333333;"
            "    height: 25px;"
            "}"
            "QProgressBar::chunk {"
            "    background-color: #4CAF50;"
            "    border-radius: 3px;"
            "}"
        )
        
        # Status label for detailed status messages
        self.m_statusLabel = QLabel(self)
        self.m_statusLabel.setVisible(False)
        self.m_statusLabel.setStyleSheet(
            "QLabel {"
            "    background-color: #e3f2fd;"
            "    border: 1px solid #90caf9;"
            "    border-radius: 4px;"
            "    padding: 8px;"
            "    font-size: 13px;"
            "    color: #1976d2;"
            "    min-height: 20px;"
            "}"
        )
        self.m_statusLabel.setWordWrap(True)
        self.m_statusLabel.setText("Ready")
        
        # Add widgets to main layout
        mainLayout.addWidget(leftSideWidget, 1)
        mainLayout.addWidget(separatorWidget, 0)
        mainLayout.addWidget(rightSideWidget, 1)
        
        # Add progress bar and status label at the bottom
        outerLayout = QVBoxLayout()
        outerLayout.setContentsMargins(0, 0, 0, 0)
        outerLayout.addLayout(mainLayout)
        outerLayout.addWidget(self.m_statusLabel)
        outerLayout.addWidget(self.m_progressBar)
        
        self.m_centralWidget = QWidget()
        self.m_centralWidget.setLayout(outerLayout)
        self.setCentralWidget(self.m_centralWidget)
    
    def onAnalyzeButtonClicked(self):
        """Handle analyze button click."""
        if not self.m_canvas.hasDrawing():
            QMessageBox.information(self, "No Drawing", "Please draw something on the canvas first!")
            return
        
        self.m_analyzeButton.setEnabled(False)
        self.m_progressBar.setVisible(True)
        self.m_progressBar.setRange(0, 0)  # Indeterminate progress
        self.m_progressBar.setFormat("Analyzing...")
        self.m_statusLabel.setVisible(True)
        self.m_statusLabel.setText("🔄 Preparing to analyze your drawing...")
        self.m_textArea.clear()
        self.m_textArea.setPlainText(
            "Analyzing your drawing...\n\n"
            "Please wait, this may take a while on the first run (model download and loading)."
        )
        
        sketch = self.m_canvas.getSketch()
        self.m_analyzer.analyzeSketch(sketch)
    
    def onAnalysisComplete(self, story: str):
        """Handle successful analysis."""
        self.m_progressBar.setVisible(False)
        self.m_statusLabel.setText("✅ Story generated successfully!")
        self.m_analyzeButton.setEnabled(True)
        
        # Display text immediately in the left text area
        self.m_textArea.setPlainText(story)
        self.m_textArea.moveCursor(QTextCursor.MoveOperation.Start)
        QApplication.processEvents()  # Ensure UI updates immediately
        
        # Extract English and German text and read them
        # Try multiple parsing strategies for different formats
        englishText = ""
        germanText = ""
        
        
        # Read English first, then German (text is already visible)
        if englishText:
            self.speakText(englishText, "en")
            # Schedule German speech after a delay
            if germanText:
                QTimer.singleShot(3000, lambda: self.speakText(germanText, "de"))
        elif germanText:
            self.speakText(germanText, "de")
    
    def onAnalysisError(self, error: str):
        """Handle analysis error."""
        self.m_progressBar.setVisible(False)
        self.m_analyzeButton.setEnabled(True)
        
        # Check if it's a "model loading" error - show as info, not critical
        if "loading" in error.lower() or "503" in error:
            self.m_statusLabel.setText("⏳ Model is loading... Please wait and try again.")
            QMessageBox.information(
                self,
                "Model is Loading",
                error + "\n\nTip: Wait a moment and click the arrow button again."
            )
            self.m_textArea.setPlainText("Status: " + error + "\n\nPlease wait and try again.")
        elif "timeout" in error.lower():
            self.m_statusLabel.setText("⏱️ Request timeout - The process took too long. Please try again.")
            QMessageBox.warning(self, "Timeout", error)
            self.m_textArea.setPlainText("Error: " + error)
        else:
            self.m_statusLabel.setText("❌ Error: " + error[:100])
            QMessageBox.critical(self, "Analysis Error", "Failed to analyze sketch: " + error)
            self.m_textArea.setPlainText("Error: " + error)
    
    def onStatusUpdate(self, status: str):
        """Handle status updates."""
        self.m_statusLabel.setVisible(True)
        
        # Remove emoji prefix if already present to avoid duplication
        cleanStatus = status
        if any(cleanStatus.startswith(prefix) for prefix in ["🔄 ", "📤 ", "⏳ ", "⚙️ ", "✅ ", "❌ "]):
            self.m_statusLabel.setText(cleanStatus)
        else:
            # Add emoji based on status type
            if "Sending" in status or "sending" in status:
                self.m_statusLabel.setText("📤 " + status)
            elif "Waiting" in status or "waiting" in status:
                self.m_statusLabel.setText("⏳ " + status)
            elif "Receiving" in status or "receiving" in status:
                self.m_statusLabel.setText("📥 " + status)
            elif "Processing" in status or "processing" in status:
                self.m_statusLabel.setText("⚙️ " + status)
            elif "loading" in status.lower() or "Loading" in status:
                self.m_statusLabel.setText("⏳ " + status)
            else:
                self.m_statusLabel.setText("🔄 " + status)
        
        # Update progress bar text
        if "Sending" in status or "sending" in status:
            self.m_progressBar.setFormat("📤 Sending...")
        elif "Waiting" in status or "waiting" in status:
            self.m_progressBar.setFormat("⏳ Waiting...")
        elif "Receiving" in status or "receiving" in status:
            # Extract percentage if present
            import re
            match = re.search(r'(\d+)%', status)
            if match:
                self.m_progressBar.setFormat("📥 Receiving " + match.group(1) + "%")
            else:
                self.m_progressBar.setFormat("📥 Receiving...")
        elif "Processing" in status or "processing" in status:
            self.m_progressBar.setFormat("⚙️ Processing...")
        elif "loading" in status.lower() or "Loading" in status:
            self.m_progressBar.setFormat("⏳ Loading model...")
        else:
            self.m_progressBar.setFormat("🔄 " + status[:20])
        
        # Also update text area for detailed info
        currentText = self.m_textArea.toPlainText()
        if currentText.startswith("Analyzing") or currentText.startswith("Status:"):
            self.m_textArea.setPlainText("Status: " + status)
    
    def speakText(self, text: str, language: str):
        """Speak text using text-to-speech."""
        if not TTS_AVAILABLE:
            return
        
        try:
            engine = pyttsx3.init()
            
            # Set language/voice
            voices = engine.getProperty('voices')
            if language == "de":
                # Try to find German voice
                for voice in voices:
                    if 'german' in voice.name.lower() or 'de' in voice.id.lower():
                        engine.setProperty('voice', voice.id)
                        break
            else:
                # Try to find English voice
                for voice in voices:
                    if 'english' in voice.name.lower() or 'en' in voice.id.lower():
                        engine.setProperty('voice', voice.id)
                        break
            
            # Set speech rate (words per minute)
            # Default is usually 200, range is typically 50-300
            # Lower values = slower, higher values = faster
            engine.setProperty('rate', 150)
            
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            # TTS failed, but don't show error to user
            print(f"TTS error: {e}")
    
    def getCustomPrompt(self):
        """Get the custom prompt from the input field."""
        if self.m_customPromptInput:
            return self.m_customPromptInput.text()
        return ""
    
    def onToolChanged(self, button):
        """Handle tool selection change."""
        tool_id = self.m_toolButtonGroup.id(button)
        self.m_canvas.setTool(tool_id)

