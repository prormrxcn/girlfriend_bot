
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import datetime
import threading
from PIL import Image, ImageTk
import os
import random

class ChatbotUI:
    def __init__(self, chatbot_instance):
        self.chatbot = chatbot_instance
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.setup_layout()
        self.bind_events()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("💖 Deepanshi - Your Virtual Girlfriend")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Set window icon (if available)
        try:
            icon = tk.PhotoImage(file="icon.png")
            self.root.iconphoto(False, icon)

        except:
            pass
        
        # Configure colors
        self.colors = {
            'bg_main': '#ffeef5',        # Light pink background
            'bg_chat': '#ffffff',        # White chat area
            'bg_input': '#f8f9fa',       # Light gray input
            'accent': '#ff69b4',         # Hot pink accent
            'text_user': '#2c3e50',      # Dark blue for user
            'text_bot': '#e91e63',       # Pink for bot
            'border': '#f0f0f0',         # Light border
            'button_bg': '#ff1493',      # Deep pink button
            'button_fg': '#ffffff'       # White button text
        }
        
        self.root.configure(bg=self.colors['bg_main'])
        
    def setup_styles(self):
        """Configure ttk styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure button style
        self.style.configure(
            'Pink.TButton',
            background=self.colors['button_bg'],
            foreground=self.colors['button_fg'],
            borderwidth=0,
            focuscolor='none',
            padding=(10, 5)
        )
        
        self.style.map('Pink.TButton',
            background=[('active', '#ff1493'), ('pressed', '#dc143c')]
        )
        
        # Configure entry style
        self.style.configure(
            'Pink.TEntry',
            fieldbackground=self.colors['bg_input'],
            borderwidth=1,
            focuscolor=self.colors['accent']
        )
        
    def create_widgets(self):
        """Create all UI widgets"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg_main'])
        
        # Header frame
        self.header_frame = tk.Frame(self.main_frame, bg=self.colors['accent'], height=60)
        self.header_frame.pack_propagate(False)
        
        # Header content
        self.header_label = tk.Label(
            self.header_frame,
            text="💖 Deepanshi - Your Virtual Girlfriend 💖",
            font=('Arial', 16, 'bold'),
            fg=self.colors['button_fg'],
            bg=self.colors['accent']
        )
        
        self.status_label = tk.Label(
            self.header_frame,
            text="Online • Ready to chat",
            font=('Arial', 10),
            fg=self.colors['button_fg'],
            bg=self.colors['accent']
        )
        
        # Chat area frame
        self.chat_frame = tk.Frame(self.main_frame, bg=self.colors['bg_main'])
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=('Arial', 11),
            bg=self.colors['bg_chat'],
            fg=self.colors['text_user'],
            borderwidth=1,
            relief='solid',
            selectbackground=self.colors['accent'],
            selectforeground=self.colors['button_fg']
        )
        
        # Input frame
        self.input_frame = tk.Frame(self.main_frame, bg=self.colors['bg_main'])
        
        # Input field
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(
            self.input_frame,
            textvariable=self.input_var,
            font=('Arial', 12),
            style='Pink.TEntry',
            width=50
        )
        
        # Send button
        self.send_button = ttk.Button(
            self.input_frame,
            text="Send 💕",
            command=self.send_message,
            style='Pink.TButton'
        )
        
        # Control buttons frame
        self.control_frame = tk.Frame(self.main_frame, bg=self.colors['bg_main'])
        
        # Control buttons
        self.topic_button = ttk.Button(
            self.control_frame,
            text="💭 Topic",
            command=self.suggest_topic,
            style='Pink.TButton'
        )
        
        self.clear_button = ttk.Button(
            self.control_frame,
            text="🗑️ Clear",
            command=self.clear_chat,
            style='Pink.TButton'
        )
        
        self.help_button = ttk.Button(
            self.control_frame,
            text="❓ Help",
            command=self.show_help,
            style='Pink.TButton'
        )
        
        # Typing indicator
        self.typing_label = tk.Label(
            self.chat_frame,
            text="",
            font=('Arial', 9, 'italic'),
            fg=self.colors['text_bot'],
            bg=self.colors['bg_main']
        )
        
    def setup_layout(self):
        """Arrange all widgets"""
        # Main frame
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        self.header_label.pack(pady=(10, 0))
        self.status_label.pack(pady=(0, 10))
        
        # Chat area
        self.chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.typing_label.pack(fill=tk.X, padx=5)
        
        # Input area
        self.input_frame.pack(fill=tk.X, pady=(0, 10))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.send_button.pack(side=tk.RIGHT)
        
        # Control buttons
        self.control_frame.pack(fill=tk.X)
        self.topic_button.pack(side=tk.LEFT, padx=(0, 5))
        self.clear_button.pack(side=tk.LEFT, padx=(0, 5))
        self.help_button.pack(side=tk.LEFT)
        
    def bind_events(self):
        """Bind keyboard and window events"""
        self.root.bind('<Return>', lambda e: self.send_message())
        self.root.bind('<Control-Return>', lambda e: self.suggest_topic())
        self.root.bind('<Control-l>', lambda e: self.clear_chat())
        self.input_entry.focus_set()
        
    def add_message(self, sender, message, color=None):
        """Add a message to the chat display"""
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        # Configure text tags
        if color:
            tag_name = f"color_{color}"
            self.chat_display.tag_configure(tag_name, foreground=color)
        else:
            tag_name = "default"
            
        # Insert message
        self.chat_display.config(state=tk.NORMAL)
        
        if sender == "You":
            self.chat_display.insert(tk.END, f"[{timestamp}] You: ", "user_tag")
            self.chat_display.insert(tk.END, f"{message}\n\n", "user_msg")
        else:
            self.chat_display.insert(tk.END, f"[{timestamp}] 💖 Deepanshi: ", "bot_tag")
            self.chat_display.insert(tk.END, f"{message}\n\n", "bot_msg")
        
        # Configure tags
        self.chat_display.tag_configure("user_tag", foreground=self.colors['text_user'], font=('Arial', 11, 'bold'))
        self.chat_display.tag_configure("user_msg", foreground=self.colors['text_user'], font=('Arial', 11))
        self.chat_display.tag_configure("bot_tag", foreground=self.colors['text_bot'], font=('Arial', 11, 'bold'))
        self.chat_display.tag_configure("bot_msg", foreground=self.colors['text_bot'], font=('Arial', 11))
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def show_typing_indicator(self, show=True):
        """Show/hide typing indicator"""
        if show:
            self.typing_label.config(text="💖 Deepanshi is typing...")
            self.typing_label.after(100, self.animate_typing)
        else:
            self.typing_label.config(text="")
            
    def animate_typing(self):
        """Animate typing indicator"""
        current_text = self.typing_label.cget("text")
        if "typing..." in current_text:
            if current_text.endswith("..."):
                self.typing_label.config(text="💖 Deepanshi is typing")
            elif current_text.endswith(".."):
                self.typing_label.config(text="💖 Deepanshi is typing...")
            elif current_text.endswith("."):
                self.typing_label.config(text="💖 Deepanshi is typing..")
            else:
                self.typing_label.config(text="💖 Deepanshi is typing.")
            self.typing_label.after(500, self.animate_typing)
            
    def send_message(self):
        """Send user message and get bot response"""
        user_input = self.input_var.get().strip()
        if not user_input:
            return
            
        # Add user message
        self.add_message("You", user_input)
        self.input_var.set("")
        
        # Show typing indicator
        self.show_typing_indicator(True)
        
        # Get bot response in separate thread
        threading.Thread(target=self.get_bot_response, args=(user_input,), daemon=True).start()
        
    def get_bot_response(self, user_input):
        """Get response from chatbot in separate thread"""
        try:
            response = self.chatbot.get_response(user_input)
            
            # Update UI in main thread
            self.root.after(0, self.display_bot_response, response)
        except Exception as e:
            error_msg = f"Sorry baby, I'm having some technical difficulties right now. Can you try again? 💕"
            self.root.after(0, self.display_bot_response, error_msg)
            
    def display_bot_response(self, response):
        """Display bot response and hide typing indicator"""
        self.show_typing_indicator(False)
        self.add_message("Deepanshi", response)
        
    def suggest_topic(self):
        """Suggest a conversation topic"""
        topic = self.chatbot.suggest_topic()
        self.add_message("Deepanshi", f"💭 {topic}")
        
    def clear_chat(self):
        """Clear the chat display"""
        if messagebox.askyesno("Clear Chat", "Are you sure you want to clear the chat history?"):
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.config(state=tk.DISABLED)
            
            # Reset chatbot history
            self.chatbot.chat_history = []
            
            # Add welcome message
            welcome_msg = self.chatbot.start_conversation()
            self.add_message("Deepanshi", welcome_msg)
            
    def show_help(self):
        """Show help dialog"""
        help_text = """
🌸 Deepanshi Chatbot Help 🌸

Commands:
• Just type normally to chat with Deepanshi
• Press Enter to send messages
• Use the buttons below for quick actions

Buttons:
• 💭 Topic - Get conversation suggestions
• 🗑️ Clear - Clear chat history
• ❓ Help - Show this help message

Keyboard Shortcuts:
• Enter - Send message
• Ctrl+Enter - Suggest topic
• Ctrl+L - Clear chat

Tips:
• Be romantic and sweet - Deepanshi loves affection! 💕
• Ask about her day, feelings, or share yours
• Use pet names like "baby", "jaan", "love"

Have fun chatting! 💖
        """
        
        messagebox.showinfo("Help", help_text)
        
    def start_chat(self):
        """Start the chat with a welcome message"""
        welcome_msg = self.chatbot.start_conversation()
        self.add_message("Deepanshi", welcome_msg)
        
    def run(self):
        """Start the GUI application"""
        self.start_chat()
        self.root.mainloop()

# Additional utility functions for graphics
def create_gradient_background(canvas, width, height, color1, color2):
    """Create a gradient background on a canvas"""
    for i in range(height):
        # Calculate color interpolation
        ratio = i / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, i, width, i, fill=color)

def create_heart_shape(canvas, x, y, size, color):
    """Create a heart shape on canvas"""
    # Heart shape using bezier curves approximation
    points = []
    for i in range(360):
        t = i * 3.14159 / 180
        x_pos = x + size * (16 * (t**3) - 12 * t) / 16
        y_pos = y + size * (13 * t - 5 * t**2 - 2 * t**3) / 16
        points.extend([x_pos, y_pos])
    
    canvas.create_polygon(points, fill=color, outline="")

def animate_hearts(canvas, width, height):
    """Animate floating hearts in the background"""
    hearts = []
    colors = ['#ff69b4', '#ff1493', '#ffc0cb', '#ff91a4']
    
    for i in range(5):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(5, 15)
        color = random.choice(colors)
        speed = random.randint(1, 3)
        hearts.append({'x': x, 'y': y, 'size': size, 'color': color, 'speed': speed})
    
    def move_hearts():
        canvas.delete("heart")
        for heart in hearts:
            heart['y'] -= heart['speed']
            if heart['y'] < -20:
                heart['y'] = height + 20
                heart['x'] = random.randint(0, width)
            
            create_heart_shape(canvas, heart['x'], heart['y'], heart['size'], heart['color'])
        
        canvas.after(100, move_hearts)
    
    move_hearts()